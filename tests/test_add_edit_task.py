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
        if 'date' in data:
            date = modal.find_element_by_name("date")
            date.send_keys(data['date'])

        save = modal.find_element_by_id("save-button")

        save.click()

        sleep(2)

        for r in reversed(self.driver.requests):
            if r.method == 'POST':
                del self.driver.requests
                return r


    def add_task_test_fields(self, data):
        """
        Check if the HTTP response corresponds to the data provided.
        """

        response = self.add_task(data).response
        self.assertEqual(response.status_code, 201)
        response = json.loads(response.body.decode('utf-8'))

        task_id = response['id']

        # Checks if the response fields are the same as the data provided
        for key in data.keys():
            if type(data[key]) == str:
                data[key] = data[key].strip()
                
            self.assertEqual(data[key], response[key])


    def test_add_calendar_task(self):
        """
        Add a test task to calendar.
        """

        today = self.now.strftime('%Y-%m-%d')

        data = {
            "title": "Test title",
            "description": "Test description",
            "priority": 3,
            "date": today
        }

        self.login()

        self.add_task_test_fields(data)

        self.logout()

        
    def test_add_task_title(self):
        """
        Check if trying to add a task with a title in a format not allowed
        (for example: more than 120 characters) gives an error.
        """

        data = {
            "title": "a"*121,
            "description": "Test description",
            "priority": 3,
        }

        self.login()

        response = self.add_task(data).response
        self.assertEqual(response.status_code, 400)
        body = json.loads(response.body.decode('utf-8'))
        self.assertEqual(body['title'], ['Ensure this field has no more than 120 characters.'])

        self.logout()


    def test_add_task_past_date(self):
        """
        Check if trying to add a task with a date before the current date
        gives an error.
        """

        today = (self.now - timedelta(days=1)).strftime('%Y-%m-%d')

        data = {
            "title": "Test title",
            "description": "Test description",
            "priority": 3,
            "date": today
        }

        self.login()

        response = self.add_task(data).response
        self.assertEqual(response.status_code, 400)
        body = json.loads(response.body.decode('utf-8'))
        self.assertEqual(body['date'], ['Cannot set date to a past day.'])

        self.logout()


    def update_task(self, data_update, task_id):
        """
        Update a task via the web interface.
        """

        d = self.driver
        d.get(config['react'])

        sleep(1)

        d.find_element_by_id(f'task-{task_id}').click()

        modal = d.find_element_by_class_name('modal-dialog')

        # Fill title field
        title = modal.find_element_by_name("title")
        title.send_keys(Keys.CONTROL, 'a')
        title.send_keys(Keys.BACKSPACE)
        title.send_keys(data_update['title'])

        # Fill description field
        description = modal.find_element_by_name("description")
        description.send_keys(Keys.CONTROL, 'a')
        description.send_keys(Keys.BACKSPACE)
        description.send_keys(data_update['description'])

        # Fill priority field
        priority = modal.find_element_by_name("priority")
        priority.click()

        # Fill priority field
        priorities = ["N", "L", "M", "H"]
        priority.send_keys(priorities[data_update['priority']])

        # Fill date field
        if 'date' in data_update:
            date = modal.find_element_by_name("date")
            date.send_keys(Keys.CONTROL, 'a')
            date.send_keys(Keys.BACKSPACE)
            date.send_keys(data_update['date'])

        save = modal.find_element_by_id("save-button")

        save.click()

        sleep(2)

        for r in reversed(self.driver.requests):
            if r.method == 'PUT':
                del self.driver.requests
                return r


    def add_task_test_fields_to_update(self, data, data_update):
        """
        Check if the HTTP response corresponds to the data provided.
        """

        response = self.add_task(data).response
        self.assertEqual(response.status_code, 201)
        response_json = json.loads(response.body.decode('utf-8'))

        task_id = response_json['id']
        
        # Checks if the response fields are the same as the data provided
        for key in data.keys():
            if type(data[key]) == str:
                data[key] = data[key].strip()
                
            self.assertEqual(data[key], response_json[key])
        
        result = self.update_task(data_update, task_id).response
        return result


    def test_update_calendar_task(self):
        """
        Add a test task to calendar and update it.
        """

        today = self.now.strftime('%Y-%m-%d')
        tomorrow = (self.now + timedelta(days=1)).strftime('%Y-%m-%d')

        data = {
            "title": "Title calendar",
            "description": "Description calendar",
            "priority": 0,
            "date": today
        }

        data_update = {
            "title": "Title update calendar",
            "description": "Description update calendar",
            "priority": 3,
            "date": tomorrow
        }

        self.login()

        result = self.add_task_test_fields_to_update(data, data_update)
        self.assertEqual(result.status_code, 200)

        self.logout()
        

    def test_update_calendar_task_title_fail(self):
        """
        Add a test task to calendar and update it.
        """

        today = self.now.strftime('%Y-%m-%d')
        tomorrow = (self.now + timedelta(days=1)).strftime('%Y-%m-%d')

        data = {
            "title": "Title calendar",
            "description": "Description calendar",
            "priority": 0,
            "date": today
        }

        data_update = {
            "title": "test"*120,
            "description": "Description update calendar",
            "priority": 3,
            "date": tomorrow
        }

        self.login()

        response = self.add_task_test_fields_to_update(data, data_update)
        self.assertEqual(response.status_code, 400)
        body = json.loads(response.body.decode('utf-8'))
        self.assertEqual(body['title'], ['Ensure this field has no more than 120 characters.'])

        self.logout()


    def test_update_calendar_task_date_fail(self):
        """
        Add a test task to calendar and update it.
        """

        today = self.now.strftime('%Y-%m-%d')
        yesterday = (self.now - timedelta(days=1)).strftime('%Y-%m-%d')

        data = {
            "title": "Title calendar",
            "description": "Description calendar",
            "priority": 0,
            "date": today
        }

        data_update = {
            "title": "Title update calendar",
            "description": "Description update calendar",
            "priority": 3,
            "date": yesterday
        }

        self.login()

        response = self.add_task_test_fields_to_update(data, data_update)
        self.assertEqual(response.status_code, 400)
        body = json.loads(response.body.decode('utf-8'))
        self.assertEqual(body['date'], ['Cannot set date to a past day.'])

        self.logout()


    def test_add_inbox_task(self):
        """
        Add a test task to inbox.
        """

        data = {
            "title": "Test title",
            "description": "Test description",
            "priority": 0,
        }

        self.login()

        self.add_task_test_fields(data)

        self.logout()


    def test_update_inbox_task(self):
        """
        Add a test task to inbox and update it.
        """


        data = {
            "title": "Title calendar",
            "description": "Description calendar",
            "priority": 0,
        }

        data_update = {
            "title": "Title update calendar",
            "description": "Description update calendar",
            "priority": 3,
        }

        self.login()

        result = self.add_task_test_fields_to_update(data, data_update)
        self.assertEqual(result.status_code, 200)

        self.logout()

if __name__ == '__main__':
    # Test the connection before starting the tests

    try:
        requests.get(config['react'])
        unittest.main()
    
    except requests.exceptions.ConnectionError as e:
        raise(Exception('Cannot connect to React'))