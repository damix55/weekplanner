import unittest
import yaml
import requests
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

config_path = os.path.join(os.path.dirname(__file__), 'config.yml')

with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

class LoginTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('log-level=3')
        self.driver = webdriver.Chrome(options=options)

        self.email = "test@test.test"
        self.password = "test000"

        self.wait_interval = 5

    @classmethod
    def tearDownClass(self):
        self.driver.close()  


    def test_login_correct_credentials(self):
        self.driver.get(config['react']+'/login')

        # login user with correct credentials
        email_field = self.driver.find_element_by_id("email")
        password_field = self.driver.find_element_by_id("password")

        email_field.send_keys(self.email)
        password_field.send_keys(self.password)

        submit_button = self.driver.find_element_by_id("submit")
        submit_button.click()

        time.sleep(self.wait_interval)

        assert(self.driver.find_element_by_id("add-button"))

        access_token = self.driver.execute_script("return window.localStorage.getItem('access_token');")
        refresh_token = self.driver.execute_script("return window.localStorage.getItem('refresh_token');")
        assert access_token != ''
        assert refresh_token != ''
        
        logout_link = self.driver.find_element_by_id("logout")
        logout_link.click()

    def test_login_wrong_email(self):
        self.driver.get(config['react']+'/login')

        # login user with wrong email
        email_field = self.driver.find_element_by_id("email")
        password_field = self.driver.find_element_by_id("password")

        wrong_email = self.email + "0"

        email_field.send_keys(wrong_email)
        password_field.send_keys(self.password)

        submit_button = self.driver.find_element_by_id("submit")
        submit_button.click()

        time.sleep(self.wait_interval)

        no_user_error = self.driver.find_element_by_id("no_user_error").get_attribute('innerText')

        assert no_user_error == "No active account found with the given credentials"

    def test_login_wrong_password(self):
        self.driver.get(config['react']+'/login')

        # login user with wrong password
        email_field = self.driver.find_element_by_id("email")
        password_field = self.driver.find_element_by_id("password")

        wrong_password = self.password + "0"

        email_field.send_keys(self.email)
        password_field.send_keys(wrong_password)

        submit_button = self.driver.find_element_by_id("submit")
        submit_button.click()

        time.sleep(self.wait_interval)

        no_user_error = self.driver.find_element_by_id("no_user_error").get_attribute('innerText')

        assert no_user_error == "No active account found with the given credentials"

    def test_login_empty_fields(self):
        self.driver.get(config['react']+'/login')

        email_field = self.driver.find_element_by_id("email")
        password_field = self.driver.find_element_by_id("password")

        email_field.send_keys("")
        password_field.send_keys("")

        submit_button = self.driver.find_element_by_id("submit")
        submit_button.click()

        time.sleep(self.wait_interval)

        email_error = self.driver.find_element_by_id("email_error").get_attribute('innerText')
        password_error = self.driver.find_element_by_id("password_error").get_attribute('innerText')

        assert email_error == password_error == "This field may not be blank."

    def test_logut(self):
        self.driver.get(config['react']+'/login')

        # login
        email_field = self.driver.find_element_by_id("email")
        password_field = self.driver.find_element_by_id("password")

        email_field.send_keys(self.email)
        password_field.send_keys(self.password)

        submit_button = self.driver.find_element_by_id("submit")
        submit_button.click()

        time.sleep(self.wait_interval)

        # logout
        logout_link = self.driver.find_element_by_id("logout")
        logout_link.click()

        result = self.driver.execute_script("return window.localStorage.getItem('access_token');")
        assert result == None


if __name__ == "__main__":

    try:
        requests.get(config['react'])
        unittest.main()

    except requests.exceptions.ConnectionError as e:
        raise(Exception('Cannot connect to Django'))