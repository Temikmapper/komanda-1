from datetime import date
from decimal import Decimal
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time
import os
from django.contrib.auth import get_user_model

from expenses.models import Categories, UsualExpenses

MAX_WAIT = 20
USERNAME = "test_user"
PASSWORD = "12345"


User = get_user_model()


class FunctionalTest(StaticLiveServerTestCase):
    """functional test"""

    def wait(fn):
        print("*" * 50)
        start_time = time.time()
        print("+" * 50)
        while True:
            try:
                return fn
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                print("waiting...")
                time.sleep(0.5)

    def setUp(self):
        s = Service("C:/Users/7NR_Operator_21/Desktop/msedgedriver.exe")
        self.browser = webdriver.Edge(service=s)
        staging_server = os.environ.get("STAGING_SERVER")
        if staging_server:
            self.live_server_url = "http://" + staging_server

        self.user = User.objects.create_user(
            username=USERNAME, email=None, password=PASSWORD
        )

    def tearDown(self):
        self.browser.quit()

    def add_usual_expense(self, category, value, day):
        date_ = date(date.today().year, date.today().month, day)
        category_ = Categories.objects.create(name=category)
        UsualExpenses.objects.create(
            date=date_, category=category_, amount=Decimal(value)
        )

    # def add_free_money(self, value, date)
