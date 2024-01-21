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

class RegistrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('log-level=3')
        self.driver = webdriver.Chrome(options=options)

    @classmethod
    def tearDownClass(self):
        self.driver.close()  


    def test_create_user(self):
        self.driver.get(config['react']+'/register')

        email = self.driver.find_element_by_id("email")
        username = self.driver.find_element_by_id("username")
        password = self.driver.find_element_by_id("password")

        email.send_keys("test@test.test")
        username.send_keys("test")
        password.send_keys("test000")

        submit = self.driver.find_element_by_id("submit")
        submit.click()

        time.sleep(5)

        assert(self.driver.find_element_by_id("add-button"))


    def test_create_user_empty_fields(self):
        self.driver.get(config['react']+'/register')

        submit = self.driver.find_element_by_id("submit")
        submit.click()

        time.sleep(5)

        email_error = self.driver.find_element_by_id("email_error").get_attribute('innerText')
        username_error = self.driver.find_element_by_id("username_error").get_attribute('innerText')
        password_error = self.driver.find_element_by_id("password_error").get_attribute('innerText')

        assert email_error == username_error == password_error == "This field may not be blank."


    def test_create_user_email(self):
        self.driver.get(config['react']+'/register')

        email = self.driver.find_element_by_id("email")
        email.send_keys("test@test")
        submit = self.driver.find_element_by_id("submit")
        submit.click()

        time.sleep(5)
        
        email_error = self.driver.find_element_by_id("email_error").get_attribute('innerText')
        
        assert email_error == "Enter a valid email address."


    def test_create_user_password(self):
        self.driver.get(config['react']+'/register')

        password = self.driver.find_element_by_id("password")
        password.send_keys("test0")

        submit = self.driver.find_element_by_id("submit")
        submit.click()

        time.sleep(5)
        
        password_error = self.driver.find_element_by_id("password_error").get_attribute('innerText')
        
        assert password_error == "Password must be longer than 6 characters."


    def test_create_user_email_already_exists(self):
        self.driver.get(config['react']+'/register')

        email = self.driver.find_element_by_id("email")
        email.send_keys("test@test.test")

        submit = self.driver.find_element_by_id("submit")
        submit.click()

        time.sleep(5)
        
        email_error = self.driver.find_element_by_id("email_error").get_attribute('innerText')
        
        assert email_error == "user with this email address already exists."


    def test_create_user_username_already_exists(self):
        self.driver.get(config['react']+'/register')

        username = self.driver.find_element_by_id("username")
        username.send_keys("test")

        submit = self.driver.find_element_by_id("submit")
        submit.click()

        time.sleep(5)
        
        username_error = self.driver.find_element_by_id("username_error").get_attribute('innerText')
        
        assert username_error == "user with this user name already exists."


if __name__ == "__main__":

    try:
        requests.get(config['react'])
        unittest.main()

    except requests.exceptions.ConnectionError as e:
        raise(Exception('Cannot connect to Django'))