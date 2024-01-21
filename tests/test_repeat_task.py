import unittest
import yaml
import requests
import os
import json
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
from time import sleep
from selenium.webdriver.common.keys import Keys


config_path = os.path.join(os.path.dirname(__file__), 'config.yml')
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)


class AddTaskTests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('log-level=3')
        self.driver = webdriver.Chrome(options=options)
        self.now = datetime.now()

        self.email = "test@test.test"
        self.password = "test000"

        self.wait_interval = 3

    @classmethod
    def tearDownClass(self):
        self.driver.close()


    def login(self):
        d = self.driver
        d.get(config['react'])
        
        email_field = self.driver.find_element_by_id("email")
        password_field = self.driver.find_element_by_id("password")

        email_field.send_keys(self.email)
        password_field.send_keys(self.password)

        submit_button = self.driver.find_element_by_id("submit")
        submit_button.click()

        sleep(self.wait_interval)


    def logout(self):
        d = self.driver
        d.get(config['react'])

        logout_button = self.driver.find_element_by_id("logout")
        logout_button.click()

        sleep(self.wait_interval)


    def add_task(self, data):
        """
        Add a task via the web interface.
        """
        d = self.driver
        d.get(config['react'])

        d.find_element_by_id('add-button').click()

        modal = d.find_element_by_class_name('modal-dialog')

        # Fill title field
        title = modal.find_element_by_name("title")
        title.send_keys(data['title'])

        # Fill description field
        description = modal.find_element_by_name("description")
        description.send_keys(data['description'])

        # Fill priority field
        priority = modal.find_element_by_name("priority")
        priority.click()

        # Fill priority field
        priorities = ["N", "L", "M", "H"]
        priority.send_keys(priorities[data['priority']])

        # Fill date field
        date = modal.find_element_by_name("date")
        date.send_keys(data['date'])
        description.click()

        # Click repeat checkbox
        repeat = modal.find_element_by_name("repeat")
        repeat.click()

        # Fill until field
        until = modal.find_element_by_name("until")
        until.send_keys(data['until'])
        description.click()

        # Fill 'every' field
        every = modal.find_element_by_name("every")
        every.send_keys(Keys.BACKSPACE)
        every.send_keys(data['every'])

        # Save
        save = modal.find_element_by_id("save-button")
        save.click()

        sleep(2)

        for r in reversed(self.driver.requests):
            if r.method == 'POST':
                del self.driver.requests
                return r


    def test_add_repeat_task(self):
        """
        Add a test task to calendar and repeat it, then check if the number of
        repetitions created are correct.
        """

        today = self.now.strftime('%Y-%m-%d')
        until = (self.now + timedelta(days=10)).strftime('%Y-%m-%d')

        data = {
            "title": "Test title",
            "description": "Test description",
            "priority": 3,
            "date": today,
            "until": until,
            "every": 1
        }

        self.login()

        response = self.add_task(data).response
        self.assertEqual(response.status_code, 201)
        response = json.loads(response.body.decode('utf-8'))

        self.assertEqual(len(response), 10)

        self.logout()

    
    def test_add_repeat_task_past_date(self):
        """
        Add a test task to calendar and repeat it, add a repetition with a past
        date and check if it gives an error.
        """

        today = self.now.strftime('%Y-%m-%d')
        until = (self.now - timedelta(days=10)).strftime('%Y-%m-%d')

        data = {
            "title": "Test title",
            "description": "Test description",
            "priority": 3,
            "date": today,
            "until": until,
            "every": 1
        }

        self.login()

        response = self.add_task(data).response
        self.assertEqual(response.status_code, 400)
        response = json.loads(response.body.decode('utf-8'))

        self.assertEqual(response['until'][0], "The date must be a day after today")

        self.logout()

    
    def test_add_repeat_task_past_date(self):
        """
        Add a test task to calendar and repeat it, then check if the number of
        repetitions created are correct.
        """

        today = self.now.strftime('%Y-%m-%d')
        until = (self.now + timedelta(days=10)).strftime('%Y-%m-%d')

        data = {
            "title": "Test title",
            "description": "Test description",
            "priority": 3,
            "date": today,
            "until": until,
            "every": 1
        }

        self.login()

        response = self.add_task(data).response
        self.assertEqual(response.status_code, 201)
        response = json.loads(response.body.decode('utf-8'))

        self.assertEqual(len(response), 10)

        self.logout()

    
    def test_add_repeat_task_wrong_every(self):
        """
        Add a test task to calendar and repeat it, add a repetition with a negative
        value of day span (every) and check if it gives an error.
        """

        today = self.now.strftime('%Y-%m-%d')
        until = (self.now + timedelta(days=10)).strftime('%Y-%m-%d')

        data = {
            "title": "Test title",
            "description": "Test description",
            "priority": 3,
            "date": today,
            "until": until,
            "every": -1
        }

        self.login()

        response = self.add_task(data).response
        self.assertEqual(response.status_code, 400)
        response = json.loads(response.body.decode('utf-8'))

        self.assertEqual(response['every'][0], "The number must be greater than 0")

        self.logout()



if __name__ == '__main__':
    # Test the connection before starting the tests

    try:
        requests.get(config['react'])
        unittest.main()
    
    except requests.exceptions.ConnectionError as e:
        raise(Exception('Cannot connect to React'))