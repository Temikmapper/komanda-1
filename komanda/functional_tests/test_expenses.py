from datetime import date, datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
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
        # проверяем на странице All (потом скрою, осталвлю только 10 последних)
