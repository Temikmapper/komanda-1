from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.keys import Keys
from functional_tests.base import FunctionalTest, PASSWORD, USERNAME

MAX_WAIT = 10


class NewVisitorTest(FunctionalTest):
    def test_start_goals(self):

        # заходим на страницу целей, видим страничку для авторизации
        self.browser.get(self.live_server_url + "/goals")
        login_field = self.browser.find_element(By.ID, "id_username")
        self.assertEqual(login_field.get_attribute("placeholder"), "Login")
        password_field = self.browser.find_element(By.ID, "id_password")
        self.assertEqual(password_field.get_attribute("placeholder"), "Password")

        # авторизуемся
        login_field.send_keys(USERNAME)
        password_field.send_keys(PASSWORD)
        password_field.send_keys(Keys.ENTER)

        # редирект к целям
        goals_title = self.browser.find_element(By.ID, "goals_title").text
        self.assertEqual(goals_title, "All goals")

        # целей нет
        goals_boxes = self.browser.find_elements(By.ID, "goal_container")
        self.assertEqual(len(goals_boxes), 0)

        # тык на кнопку добавить цель
        self.browser.find_element(By.ID, "add_goal_btn").click()
        add_goal_title = self.browser.find_element(By.ID, "add_goal_title").text
        self.assertEqual(add_goal_title, "Add Goal")

        # добавляем цель: дом за 20 тыщ к 1 января 2030 года
        goal_name_field = self.browser.find_element(By.ID, "id_name")
        goal_price_field = self.browser.find_element(By.ID, "id_value")
        goal_date_field = self.browser.find_element(By.ID, "id_date")

        self.assertEqual(goal_name_field.get_attribute("placeholder"), "Name")
        self.assertEqual(goal_price_field.get_attribute("placeholder"), "Price")

        goal_name_field.send_keys("House")
        goal_date_field.send_keys("01.01.2030")
        goal_price_field.send_keys("20000.00")

        self.browser.find_element(By.ID, "goal_save_btn").click()
        # редирект к целям

        goals_boxes = self.browser.find_elements(By.ID, "goal_container")
        self.assertEqual(len(goals_boxes), 1)
        goal_house_title = goals_boxes[0].find_element_by_tag_name("h1").text
        self.assertEqual(goal_house_title, "House")
        goal_house_subtitles = goals_boxes[0].find_elements(By.TAG_NAME, "h2")
        goal_house_ending = goal_house_subtitles[0].text
        self.assertEqual(goal_house_ending, "Ending 1 января 2030 г.")
        goal_house_percent = goal_house_subtitles[1].text
        self.assertEqual(goal_house_percent, "0,00 %")
        goal_house_left = goal_house_subtitles[2].text
        self.assertEqual(goal_house_left, "Left 20000,00 of 20000,00")

        # добавляем цель: машина за 30 тыщ к 1 января 2025 года
        self.browser.find_element(By.ID, "add_goal_btn").click()
        self.browser.find_element(By.ID, "id_name").send_keys("Car")
        self.browser.find_element(By.ID, "id_value").send_keys("30000.00")
        self.browser.find_element(By.ID, "id_date").send_keys("01.01.2025")
        self.browser.find_element(By.ID, "goal_save_btn").click()

        # редирект к целям
        goals_boxes = self.browser.find_elements(By.ID, "goal_container")
        self.assertEqual(len(goals_boxes), 2)

        # бампаем цель: +5000 1-го января 2021
        # goals_boxes[0].find_element(By.ID, "goal_bump_btn").click()
        self.browser.find_element(By.ID, "goal_bump_btn").click()
        self.browser.find_element(By.ID, "id_value").send_keys("5000.00")
        self.browser.find_element(By.ID, "id_date").send_keys("01.01.2021")
        self.browser.find_element(By.ID, "goal_save_btn").click()

        # редирект к целям
        # вижу изменение: 25%, осталось 15к у дома
        goals_boxes = self.browser.find_elements(By.ID, "goal_container")
        goal_house_title = goals_boxes[0].find_element_by_tag_name("h1").text
        self.assertEqual(goal_house_title, "House")
        goal_house_subtitles = goals_boxes[0].find_elements(By.TAG_NAME, "h2")
        goal_house_ending = goal_house_subtitles[0].text
        self.assertEqual(goal_house_ending, "Ending 1 января 2030 г.")
        goal_house_percent = goal_house_subtitles[1].text
        self.assertEqual(goal_house_percent, "25,00 %")
        goal_house_left = goal_house_subtitles[2].text
        self.assertEqual(goal_house_left, "Left 15000,00 of 20000,00")

        # тык на "посмотреть цель"
        # вижу историю из 2-х событий: бамп 1-го января 21-го, создание сегодня
        goals_boxes[0].find_element(By.ID, "goal_view_btn").click()
        goal_title = self.browser.find_element(By.ID, "goal_name_title").text
        self.assertEqual(goal_title, "House")
        goal_history = self.browser.find_element(By.CLASS_NAME, "timeline")
        history_items = goal_history.find_elements(By.CLASS_NAME, "timeline-item")
        self.assertEqual(len(history_items), 2)

        bump_item = history_items[0]
        bump_date = bump_item.find_element(By.ID, "event_date").text
        self.assertEqual(bump_date, "1 ЯНВАРЯ 2021 Г.")
        bump_value = bump_item.find_element(By.ID, "event_value").text
        self.assertEqual(bump_value, "5000,00")

        # тык на все цели
        self.browser.find_element(By.ID, "main_menu_goals_btn").click()

        # тык на "изменить цель" у машины
        goals_boxes = self.browser.find_elements(By.ID, "goal_container")
        goals_boxes[1].find_element(By.ID, "goal_edit_link").click()

        # меняю цель: машина 30к -> 10к
        self.browser.find_element(By.ID, "id_value").clear()
        self.browser.find_element(By.ID, "id_value").send_keys("10000")
        self.browser.find_element(By.ID, "goal_save_btn").click()

        # редирект на саму цель, вижу, что изменилось значение у цели
        goal_title = self.browser.find_element(By.ID, "goal_name_title").text
        self.assertEqual(goal_title, "Car")

        # тык на все цели, там може всё изменилось
        self.browser.find_element(By.ID, "main_menu_goals_btn").click()
        goals_boxes = self.browser.find_elements(By.ID, "goal_container")
        goal_left = goals_boxes[1].find_element(By.ID, "goal_left").text
        self.assertEqual(goal_left, "Left 10000,00 of 10000,00")
