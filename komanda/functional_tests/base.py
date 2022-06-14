from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time
import os
MAX_WAIT = 10
USERNAME = 'test_user'
PASSWORD = '12345'

from django.contrib.auth import get_user_model

from goals.models import Goals

User = get_user_model()

class FunctionalTest(StaticLiveServerTestCase):
    '''functional test'''  

    def wait(fn):
        def modified_fn(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    return fn(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.time() - start_time > MAX_WAIT:
                        raise e
                    time.sleep(0.5)
        return modified_fn

    def setUp(self):
        s = Service('C:/Users/7NR_Operator_21/Desktop/msedgedriver.exe')
        self.browser = webdriver.Edge(service=s)
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
        
        self.user = User.objects.create_user(username=USERNAME,
                                             email=None,
                                             password=PASSWORD)

    def tearDown(self):
        self.browser.quit()