from datetime import date, datetime
import time
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from functional_tests.base import FunctionalTest, PASSWORD, USERNAME

MAX_WAIT = 10


class MonthlyPageTest(FunctionalTest):
    def test_create_constant_income(self):

        self.browser.get(self.live_server_url + "/monthly")
        login_field = self.browser.find_element(By.ID, "id_username")
        self.assertEqual(login_field.get_attribute("placeholder"), "Login")
        password_field = self.browser.find_element(By.ID, "id_password")
        self.assertEqual(password_field.get_attribute("placeholder"), "Password")

        # авторизуемся
        login_field.send_keys(USERNAME)
        password_field.send_keys(PASSWORD)
        password_field.send_keys(Keys.ENTER)

        # автоматический редирект на текущий месяц
        # перехожу на месяц, вижу табличку с тратами пустыми, графики (бублик с категориями трат и график с изменением)
        table_ = self.browser.find_element(By.ID, "table_")
        donut_graph = self.browser.find_element(By.ID, "donut_graph")
        expenses_graph = self.browser.find_element(By.ID, "expenses_graph")

        # пустые доходы и постоянные расходы, свободные деньге
        free_money = self.browser.find_element(By.ID, "free_money").text
        total_incomes = self.browser.find_element(By.ID, "total_incomes").text
        total_expenses = self.browser.find_element(By.ID, "total_expenses").text
        # self.assertEqual(free_money, "0,00")
        self.assertEqual(total_expenses, "0,00")
        self.assertEqual(total_incomes, "0,00")

        # добавляю обычную трату на первое число с названием котлетка за 100 рублей
        self.add_usual_expense("котлетка", 100, 1)
        # добавыляю обычную трату на второе число с названием рыба за 200 рублей
        self.add_usual_expense("рыба", 200, 2)

        # вижу, что они обе есть в таблице
        self.browser.get(self.live_server_url + "/monthly")
        found_1 = self.browser.page_source.find("котлетка")
        found_2 = self.browser.page_source.find("рыба")
        self.assertNotEqual(found_1, -1)
        self.assertNotEqual(found_2, -1)

        # внизу отображается сумма
        total_sum_of_expenses = self.browser.find_element(
            By.ID, "total_sum_of_expenses"
        ).text
        self.assertEqual(total_sum_of_expenses, "300,00")

        # добавляю свободные деньги, 5к в месяц
        # в таблице меняется остаток после трат
        # добавляю постоянную трату связь за 500 рублей на 2020 1 февраля
        # добавляю пост доход 1000 рублёу на 1 апреля 2020
        # жму на монсли, открывается июнь 2021
        # инком 1000, трата 500
        # жму на март инком 0 трата 500
        # жму на январь инком 0 трата 0
