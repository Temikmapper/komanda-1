from datetime import date, datetime
import time
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from functional_tests.base import FunctionalTest, PASSWORD, USERNAME

MAX_WAIT = 10

class ConstantIncomeTest(FunctionalTest):
    def test_create_constant_income(self):

        self.browser.get(self.live_server_url + "/incomes/add_constant")
        login_field = self.browser.find_element(By.ID, "id_username")
        self.assertEqual(login_field.get_attribute("placeholder"), "Login")
        password_field = self.browser.find_element(By.ID, "id_password")
        self.assertEqual(password_field.get_attribute("placeholder"), "Password")

        # авторизуемся
        login_field.send_keys(USERNAME)
        password_field.send_keys(PASSWORD)
        password_field.send_keys(Keys.ENTER)

        # заходим на добавлние
        self.browser.get(self.live_server_url + "/incomes/add_constant")
        # вводим название, начало и значение (зарплата, 11.03.2022, 95000)
        income_date_field = self.browser.find_element(By.ID, "id_start_date")
        income_name = self.browser.find_element(By.ID, "id_name")
        self.assertEqual(income_name.get_attribute("placeholder"), "Name of income")
        income_value_field = self.browser.find_element(By.ID, "id_value")
        self.assertEqual(income_value_field.get_attribute("placeholder"), "Value")

        income_date_field.clear()
        income_date_field.send_keys("11.03.2022")
        income_name.send_keys("Зарплата")
        income_value_field.send_keys("95000")

        self.browser.find_element(By.ID, "income_save_btn").click()
        # редирект на "все" постоянные доходы
        # видим, что они появились, где указана дата начала, дата конца
        income_item = self.browser.find_element(By.ID, "income_item")

        start_date = income_item.find_element(By.ID, "start_date").text
        finish_date = income_item.find_element(By.ID, "finish_date").text
        income_value = income_item.find_element(By.ID, "income_value").text
        income_name = income_item.find_element(By.ID, "income_name").text

        self.assertEqual(start_date, "11.03.2022")
        self.assertEqual(finish_date, "10.03.2024")
        self.assertEqual(income_value, "95000,00")
        self.assertEqual(income_name, "Зарплата")

        # заходим на просмотр, видим историю, (1 пункт: когда она была создана)
        self.browser.find_element(By.ID, "income_view_btn").click()
        income_title = self.browser.find_element(By.ID, "income_name_title").text
        self.assertEqual(income_title, "Зарплата")
        income_history = self.browser.find_element(By.CLASS_NAME, "timeline")
        history_items = income_history.find_elements(By.CLASS_NAME, "timeline-item")
        self.assertEqual(len(history_items), 1)

        # переходим по ссылке на все постоянные доходы
        self.browser.get(self.live_server_url + "/incomes/constant/all")

        # тык на изменить, меняем дату конца на 14.07.2022
        self.browser.find_element(By.ID, "income_edit_link").click()
        income_date_field = self.browser.find_element(By.ID, "id_finish_date")
        income_date_field.clear()
        income_date_field.send_keys("14.07.2022")
        self.browser.find_element(By.ID, "income_save_btn").click()

        # открывается список всех доходов, видим изменение

        start_date = self.browser.find_element(By.ID, "start_date").text
        finish_date = self.browser.find_element(By.ID, "finish_date").text
        income_value = self.browser.find_element(By.ID, "income_value").text
        income_name = self.browser.find_element(By.ID, "income_name").text

        self.assertEqual(start_date, "11.03.2022")
        self.assertEqual(finish_date, "14.07.2022")
        self.assertEqual(income_value, "95000,00")
        self.assertEqual(income_name, "Зарплата")

        # добавляем доход "реп" создана 01.01.2018 5000
        self.browser.find_element(By.ID, "add_income_btn").click()
        income_date_field = self.browser.find_element(By.ID, "id_start_date")
        income_name = self.browser.find_element(By.ID, "id_name")
        income_value_field = self.browser.find_element(By.ID, "id_value")

        income_date_field.clear()
        income_date_field.send_keys("01.01.2018")
        income_name.send_keys("Реп")
        income_value_field.send_keys("5000")
        self.browser.find_element(By.ID, "income_save_btn").click()

        # тык на "все", она внизу блеклым цветом в поле "архив"
        archived = self.browser.find_element(By.ID, "outdated_income_item")

        # тык на изменение у неё, меняем поле конец 01.01.2030
        archived.find_element(By.ID, "income_edit_link").click()
        income_date_field = self.browser.find_element(By.ID, "id_finish_date")
        income_date_field.clear()
        income_date_field.send_keys("01.01.2030")
        self.browser.find_element(By.ID, "income_save_btn").click()

        # возвращаемся, видим, что она в актуальных, тык на бамп
        incomes = self.browser.find_elements(By.ID, "income_item")
        self.assertEqual(len(incomes), 2)

        incomes[1].find_element(By.ID, "income_bump_btn").click()
        # бампаем её до 5500

        bump_date_field = self.browser.find_element(By.ID, "id_date")
        bump_value = self.browser.find_element(By.ID, "id_value")

        bump_date_field.send_keys("10.03.2021")
        bump_value.send_keys("5500")
        self.browser.find_element(By.ID, "income_save_btn").click()

        # возвращемся, всё ок, два дохода
        incomes = self.browser.find_elements(By.ID, "income_item")
        self.assertEqual(len(incomes), 2)
        updated_expence = incomes[1].find_element(By.ID, "income_value").text
        self.assertEqual(updated_expence, "5500,00")

        #удаляем доход
        incomes[1].find_element(By.ID, "delete_btn").click()
        incomes = self.browser.find_elements(By.ID, "income_item")
        self.assertEqual(len(incomes), 1)

# class UsualExpenseTest(FunctionalTest):
#     def test_create_income(self):
#         # заходим на страничку с авторизацией
#         self.browser.get(self.live_server_url + "/incomes/add")
#         login_field = self.browser.find_element(By.ID, "id_username")
#         self.assertEqual(login_field.get_attribute("placeholder"), "Login")
#         password_field = self.browser.find_element(By.ID, "id_password")
#         self.assertEqual(password_field.get_attribute("placeholder"), "Password")

#         # авторизуемся
#         login_field.send_keys(USERNAME)
#         password_field.send_keys(PASSWORD)
#         password_field.send_keys(Keys.ENTER)

#         # видим поле для добавления траты:
#         # дата (по умолчанию сегодня)
#         income_date_field = self.browser.find_element(By.ID, "id_date")
#         self.assertEqual(
#             income_date_field.get_attribute("value"), str(datetime.today().date())
#         )

#         # категория
#         income_category_select = Select(
#             self.browser.find_element(By.ID, "id_category")
#         )
#         self.assertEqual(
#             income_category_select.first_selected_option.text, "---------"
#         )

#         # сумма
#         income_value_field = self.browser.find_element(By.ID, "id_value")
#         self.assertEqual(income_value_field.get_attribute("placeholder"), "Amount")

#         # кнопка добавить
#         save_btn = self.browser.find_element(By.ID, "income_save_btn")
#         self.assertEqual(save_btn.text, "Save")

#         # т.к. категории пустые ищем поле для ввода категорий
#         category_add_field = self.browser.find_element(By.ID, "category_add_field")
#         self.assertEqual(
#             category_add_field.get_attribute("placeholder"), "Enter category"
#         )

#         # вводим "сельдь"
#         category_add_field.send_keys("сельдь")
#         category_add_field.send_keys(Keys.ENTER)

#         # страничка перегружается и мы видим, что она появилась в списке категорий внизу, а также в селекте
#         income_category_select = Select(
#             self.browser.find_element(By.ID, "id_category")
#         )
#         options_list = [option.text for option in income_category_select.options]
#         self.assertTrue("сельдь" in options_list)

#         category_list_item = self.browser.find_element(By.ID, "categories-list-item")
#         self.assertEqual("сельдь", category_list_item.text)

#         # добавляем трату 1 января 2021 сельдь за 134 рубля
#         income_date_field = self.browser.find_element(By.ID, "id_date")
#         income_category_select = Select(
#             self.browser.find_element(By.ID, "id_category")
#         )
#         income_value_field = self.browser.find_element(By.ID, "id_value")

#         income_date_field.clear()
#         income_date_field.send_keys("01.01.2022")
#         income_category_select.select_by_visible_text("сельдь")
#         income_value_field.send_keys("134")

#         self.browser.find_element(By.ID, "income_save_btn").click()

#         # (в дальнейшем можно добавить 10 последних добавленных трат)
#         recent_10_incomes = self.browser.find_element(By.ID, "recent_incomes_box")
#         income_items = recent_10_incomes.find_elements(By.ID, "income_item")
#         self.assertEqual(len(income_items), 1)

#         income_category = self.browser.find_element(
#             By.ID, "income_item_category"
#         ).text
#         income_value = self.browser.find_element(By.ID, "income_item_value").text
#         income_date = self.browser.find_element(By.ID, "income_item_date").text

#         self.assertEqual(income_category, "сельдь")
#         self.assertEqual(income_value, "134,00 ₽")
#         self.assertEqual(income_date, "01.01.2022")

#         # с удалением категории всплывает подтверждение и уцдаляется трата
#         self.browser.find_element(By.ID, "category_del_btn").click()
#         Alert(self.browser).accept()
#         recent_10_incomes = self.browser.find_element(By.ID, "recent_incomes_box")
#         income_items = recent_10_incomes.find_elements(By.ID, "income_item")
#         # self.assertEqual(len(income_items), 0) нестабильно работает

