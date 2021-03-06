from time import sleep

import pytest
from selenium.webdriver.common.by import By


@pytest.mark.usefixtures('chrome_driver', 'run_app')
class TestAppBrowser:
    """ Class containing Selenium tests.
    This does not need to be a python class, it is written this way to give you an example of a test class.
    """

    def test_app_is_running(self, app):
        """
        GIVEN: that the app is running
        WHEN: the home page title is displayed
        THEN: it should be starting a business
        """
        sleep(5)
        self.driver.get('http://127.0.0.1:5000/')
        assert self.driver.title == 'Starting a Business'

    def test_dash_works_bubble_chart(self, app):
        """
        GIVEN: that the app is running
        WHEN: the bubble chart page title is displayed
        THEN: it should be bubble chart
        """
        sleep(5)
        self.driver.get('http://127.0.0.1:5000/bubble_chart')
        sleep(10)
        assert self.driver.title == 'Bubble Chart'

    def test_dash_works_choropleth_map(self, app):
        """
        GIVEN: that the app is running
        WHEN: the choropleth page title is displayed
        THEN: it should be choropleth
        """
        sleep(5)
        self.driver.get('http://127.0.0.1:5000/choropleth_map')
        sleep(10)
        assert self.driver.title == 'Choropleth Map'

    def test_full_experience(self, app):
        """
        Test simulates the interaction of a new user on the page: home -> sign-up -> home -> log in -> profile.

        GIVEN: that the app is running
        WHEN: the user interacts with it
        THEN: it working regularly
        """
        sleep(5)
        self.driver.get('http://127.0.0.1:5000/')
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.ID, "nav-signup").click()
        self.driver.implicitly_wait(5)
        assert self.driver.title == "Sign Up"

        # Creating example user inputs

        first_name = "John"
        last_name = "Doe"
        email = "random_email@email.com"
        password = "password123"
        password_repeat = "password123"
        account_type = "Professional"

        self.driver.find_element(By.ID, "first_name").send_keys(first_name)
        self.driver.find_element(By.ID, "last_name").send_keys(last_name)
        self.driver.find_element(By.ID, "email").send_keys(email)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "password_repeat").send_keys(password_repeat)
        self.driver.find_element(By.ID, "account_type").send_keys(account_type)
        self.driver.find_element(By.ID, "submit_reg").click()
        self.driver.implicitly_wait(5)
        assert self.driver.title == 'Starting a Business'
        self.driver.find_element(By.ID, "nav-log_in").click()
        self.driver.implicitly_wait(5)
        assert self.driver.title == "Login"
        self.driver.find_element(By.ID, "email").send_keys(email)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "submit_login").click()
        self.driver.implicitly_wait(5)
        assert self.driver.title == 'Starting a Business'
        self.driver.find_element(By.ID, "nav-profile").click()
        self.driver.implicitly_wait(5)
        assert self.driver.find_element(By.ID, "profile-email").text == email
        assert self.driver.find_element(By.ID, "profile-name").text == first_name + " " + last_name
