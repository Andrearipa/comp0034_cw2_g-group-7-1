from time import sleep

import pytest
from selenium.webdriver.common.by import By



@pytest.mark.usefixtures('chrome_driver', 'run_app')
class TestAppBrowser:
    """Class containing Selenium tests.
    This does not need to be a python class, it is written this way to give you an example of a test class.
    """

    def test_app_is_running(self, app):
        """ Check the app is running"""
        sleep(5)
        self.driver.get('http://127.0.0.1:5000/')
        assert self.driver.title == 'Home'