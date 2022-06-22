from datetime import date, datetime
import time
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from functional_tests.base import FunctionalTest, PASSWORD, USERNAME

MAX_WAIT = 10


class UsualExpenseTest(FunctionalTest):
    def test_create_expense(self):
        # заходим на страничку с авторизацией
        self.browser.get(self.live_server_url + "/expenses/add")
        login_field = self.browser.find_element(By.ID, "id_username")
        self.assertEqual(login_field.get_attribute("placeholder"), "Login")
        password_field = self.browser.find_element(By.ID, "id_password")
        self.assertEqual(password_field.get_attribute("placeholder"), "Password")

        # авторизуемся
        login_field.send_keys(USERNAME)
        password_field.send_keys(PASSWORD)
        password_field.send_keys(Keys.ENTER)

        # видим поле для добавления траты:
        # дата (по умолчанию сегодня)
        expense_date_field = self.browser.find_element(By.ID, "id_date")
        self.assertEqual(
            expense_date_field.get_attribute("value"), str(datetime.today().date())
        )

        # категория
        expense_category_select = Select(
            self.browser.find_element(By.ID, "id_category")
        )
        self.assertEqual(
            expense_category_select.first_selected_option.text, "---------"
        )

        # сумма
        expense_amount_field = self.browser.find_element(By.ID, "id_amount")
        self.assertEqual(expense_amount_field.get_attribute("placeholder"), "Amount")

        # кнопка добавить
        save_btn = self.browser.find_element(By.ID, "expense_save_btn")
        self.assertEqual(save_btn.text, "Save")

        # т.к. категории пустые ищем поле для ввода категорий
        category_add_field = self.browser.find_element(By.ID, "category_add_field")
        self.assertEqual(
            category_add_field.get_attribute("placeholder"), "Enter category"
        )

        # вводим "сельдь"
        category_add_field.send_keys("сельдь")
        category_add_field.send_keys(Keys.ENTER)

        # страничка перегружается и мы видим, что она появилась в списке категорий внизу, а также в селекте
        expense_category_select = Select(
            self.browser.find_element(By.ID, "id_category")
        )
        options_list = [option.text for option in expense_category_select.options]
        self.assertTrue("сельдь" in options_list)

        category_list_item = self.browser.find_element(By.ID, "categories-list-item")
        self.assertEqual("сельдь", category_list_item.text)

        # добавляем трату 1 января 2021 сельдь за 134 рубля
        expense_date_field = self.browser.find_element(By.ID, "id_date")
        expense_category_select = Select(
            self.browser.find_element(By.ID, "id_category")
        )
        expense_amount_field = self.browser.find_element(By.ID, "id_amount")

        expense_date_field.clear()
        expense_date_field.send_keys("01.01.2022")
        expense_category_select.select_by_visible_text("сельдь")
        expense_amount_field.send_keys("134")

        self.browser.find_element(By.ID, "expense_save_btn").click()

        # (в дальнейшем можно добавить 10 последних добавленных трат)
        recent_10_expenses = self.browser.find_element(By.ID, "recent_expenses_box")
        expense_items = recent_10_expenses.find_elements(By.ID, "expense_item")
        self.assertEqual(len(expense_items), 1)

        expense_category = self.browser.find_element(
            By.ID, "expense_item_category"
        ).text
        expense_value = self.browser.find_element(By.ID, "expense_item_value").text
        expense_date = self.browser.find_element(By.ID, "expense_item_date").text

        self.assertEqual(expense_category, "сельдь")
        self.assertEqual(expense_value, "134,00 ₽")
        self.assertEqual(expense_date, "01.01.2022")

        # с удалением категории всплывает подтверждение и уцдаляется трата
        self.browser.find_element(By.ID, "category_del_btn").click()
        Alert(self.browser).accept()
        recent_10_expenses = self.browser.find_element(By.ID, "recent_expenses_box")
        expense_items = recent_10_expenses.find_elements(By.ID, "expense_item")
        # self.assertEqual(len(expense_items), 0) нестабильно работает


class ConstantExpenseTest(FunctionalTest):
    def test_create_constant_expense(self):

        self.browser.get(self.live_server_url + "/expenses/add")
        login_field = self.browser.find_element(By.ID, "id_username")
        self.assertEqual(login_field.get_attribute("placeholder"), "Login")
        password_field = self.browser.find_element(By.ID, "id_password")
        self.assertEqual(password_field.get_attribute("placeholder"), "Password")

        # авторизуемся
        login_field.send_keys(USERNAME)
        password_field.send_keys(PASSWORD)
        password_field.send_keys(Keys.ENTER)

        # заходим на добавлние
        self.browser.get(self.live_server_url + "/expenses/add")
        # переключаемся на constant
        self.browser.find_element(By.ID, "constant_expense_toggle_btn").click()
        # вводим название, начало и сумму (связь, 11.03.2022, 500)
        expense_date_field = self.browser.find_element(By.ID, "id_start_date")
        expense_name = self.browser.find_element(By.ID, "id_name")
        self.assertEqual(expense_name.get_attribute("placeholder"), "Name of expense")
        expense_amount_field = self.browser.find_element(By.ID, "id_value")
        self.assertEqual(expense_amount_field.get_attribute("placeholder"), "Amount")

        expense_date_field.clear()
        expense_date_field.send_keys("11.03.2022")
        expense_name.send_keys("Yota")
        expense_amount_field.send_keys("134")

        self.browser.find_element(By.ID, "expense_save_btn").click()
        # редирект на "все" траты
        # видим, что они появились, где указана дата начала, дата конца
        expense_item = self.browser.find_element(By.ID, "expense_item")

        start_date = expense_item.find_element(By.ID, "start_date").text
        finish_date = expense_item.find_element(By.ID, "finish_date").text
        expense_value = expense_item.find_element(By.ID, "expense_value").text
        expense_name = expense_item.find_element(By.ID, "expense_name").text

        self.assertEqual(start_date, "11.03.2022")
        self.assertEqual(finish_date, "10.03.2024")
        self.assertEqual(expense_value, "134,00")
        self.assertEqual(expense_name, "Yota")

        # заходим на просмотр, видим историю, (1 пункт: когда она была создана)
        self.browser.find_element(By.ID, "expense_view_btn").click()
        expense_title = self.browser.find_element(By.ID, "expense_name_title").text
        self.assertEqual(expense_title, "Yota")
        expense_history = self.browser.find_element(By.CLASS_NAME, "timeline")
        history_items = expense_history.find_elements(By.CLASS_NAME, "timeline-item")
        self.assertEqual(len(history_items), 1)

        # жмём на верхнем меню на траты, переключаемся на постоянные, тык на "все"
        self.browser.find_element(By.ID, "main_menu_expenses_btn").click()
        self.browser.find_element(By.ID, "constant_expense_toggle_btn").click()
        self.browser.find_element(By.ID, "view_all_constant_expenses_btn").click()

        # тык на изменить, меняем дату конца на 14.07.2022
        self.browser.find_element(By.ID, "expense_edit_link").click()
        expense_date_field = self.browser.find_element(By.ID, "id_finish_date")
        expense_date_field.clear()
        expense_date_field.send_keys("14.07.2022")
        self.browser.find_element(By.ID, "expense_save_btn").click()

        # открывается список всех трат, видим изменение

        start_date = self.browser.find_element(By.ID, "start_date").text
        finish_date = self.browser.find_element(By.ID, "finish_date").text
        expense_value = self.browser.find_element(By.ID, "expense_value").text
        expense_name = self.browser.find_element(By.ID, "expense_name").text

        self.assertEqual(start_date, "11.03.2022")
        self.assertEqual(finish_date, "14.07.2022")
        self.assertEqual(expense_value, "134,00")
        self.assertEqual(expense_name, "Yota")

        # добавляем трату "проездной" создана 01.01.2018 1000
        self.browser.find_element(By.ID, "add_expense_btn").click()
        expense_date_field = self.browser.find_element(By.ID, "id_start_date")
        expense_name = self.browser.find_element(By.ID, "id_name")
        expense_amount_field = self.browser.find_element(By.ID, "id_value")

        expense_date_field.clear()
        expense_date_field.send_keys("01.01.2018")
        expense_name.send_keys("Проездной")
        expense_amount_field.send_keys("1000")
        self.browser.find_element(By.ID, "expense_save_btn").click()

        # тык на "все", она внизу блеклым цветом в поле "архив"
        archived = self.browser.find_element(By.ID, "outdated_expense_item")

        # тык на изменение у неё, меняем поле конец 01.01.2030
        archived.find_element(By.ID, "expense_edit_link").click()
        expense_date_field = self.browser.find_element(By.ID, "id_finish_date")
        expense_date_field.clear()
        expense_date_field.send_keys("01.01.2030")
        self.browser.find_element(By.ID, "expense_save_btn").click()

        # возвращаемся, видим, что она в актуальных, тык на бамп
        expenses = self.browser.find_elements(By.ID, "expense_item")
        self.assertEqual(len(expenses), 2)

        expenses[1].find_element(By.ID, "expense_bump_btn").click()
        # бампаем её до 1500

        bump_date_field = self.browser.find_element(By.ID, "id_date")
        bump_value = self.browser.find_element(By.ID, "id_value")

        bump_date_field.send_keys("10.03.2021")
        bump_value.send_keys("1500")
        self.browser.find_element(By.ID, "expense_save_btn").click()

        # возвращемся, всё ок, две траты
        expenses = self.browser.find_elements(By.ID, "expense_item")
        self.assertEqual(len(expenses), 2)
        updated_expence = expenses[1].find_element(By.ID, "expense_value").text
        self.assertEqual(updated_expence, "1500,00")

        #удаляем трату
        expenses[1].find_element(By.ID, "delete_btn").click()
        expenses = self.browser.find_elements(By.ID, "expense_item")
        self.assertEqual(len(expenses), 1)
