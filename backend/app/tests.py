from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from datetime import datetime, timedelta


class AddTaskTests(APITestCase):

    @classmethod
    def setUpClass(self):
        self.user = User.objects.create_user(user_name='test', password='test000', email='test@test.test', first_name='test')
        self.now = datetime.now()


    @classmethod
    def tearDownClass(self):
        self.user.delete()


    def login(self):
        url=reverse("token_obtain_pair")
        data = {"email": "test@test.test",
                "password": "test000"}
        response = self.client.post(url, data, format='json')
        access_token = response.json()['access']
        return access_token


    def add_task(self, data, task_type):
        """
        Add a task via API.
        """
        authorization_header = 'JWT ' + self.login()
        url = reverse(f'app:{task_type}-list', args=[self.user.id])
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=authorization_header)

        return response


    def get_task(self, task_id, task_type):
        """
        Add a task via API.
        """
        authorization_header = 'JWT ' + self.login()
        url = reverse(f'app:{task_type}-list', args=[self.user.id]) + f"{task_id}/"
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=authorization_header)

        return response


    def repeat_task(self, data):
        """
        Repeat a task via API.
        """
        authorization_header = 'JWT ' + self.login()
        url = reverse(f'app:repeat', args=[self.user.id])
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=authorization_header)

        return response


    def add_task_test_fields(self, data, task_type):
        """
        Check if the response and the task obtained via the API are the same
        as the data provided to the task added.
        """

        response = self.add_task(data, task_type)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = response.json()

        # Checks if the response fields are the same as the data provided
        for key in data.keys():
            if type(data[key]) == str:
                data[key] = data[key].strip()
                
            self.assertEqual(data[key], response[key])

        id = response['id']
        url = reverse(f'app:{task_type}-detail', args=[self.user.id, id])

        authorization_header = 'JWT ' + self.login()
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=authorization_header).json()

        # Checks if the task obtained via the API is the same as the one created
        for key in data.keys():
            if type(data[key]) == str:
                data[key] = data[key].strip()
                
            self.assertEqual(data[key], response[key])


    def update_task(self, data, url, task_type):
        """
        Update a task via API.
        """

        authorization_header = 'JWT ' + self.login()
        response_update = self.client.put(url, data, format='json', HTTP_AUTHORIZATION=authorization_header)

        return response_update


    def add_task_test_fields_to_update(self, data, data_update, task_type):
        """
        Check if the response and the task obtained via the API are the same
        as the data provided to the task added.
        """

        response = self.add_task(data, task_type)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_json = response.json()

        # Checks if the response fields are the same as the data provided
        for key in data.keys():
            if type(data[key]) == str:
                data[key] = data[key].strip()
                
            self.assertEqual(data[key], response_json[key])

        id = response_json['id']
        url = reverse(f'app:{task_type}-detail', args=[self.user.id, id])

        authorization_header = 'JWT ' + self.login()
        response_json = self.client.get(url, format='json', HTTP_AUTHORIZATION=authorization_header).json()

        # Checks if the task obtained via the API is the same as the one created
        for key in data.keys():
            if type(data[key]) == str:
                data[key] = data[key].strip()
                
            self.assertEqual(data[key], response_json[key])
        
        return self.update_task(data_update, url, task_type)


    def test_add_inbox_task(self):
        """
        Add a test task to inbox.
        """

        data = {
            "title": "Test title",
            "description": "Test description",
            "priority": 0,
            "completed": False,
        }

        self.add_task_test_fields(data, 'inbox')


    def test_add_calendar_task(self):
        """
        Add a test task to calendar.
        """

        today = self.now.strftime('%Y-%m-%d')

        data = {
            "title": "Test title",
            "description": "Test description",
            "priority": 3,
            "completed": False,
            "date": today
        }

        self.add_task_test_fields(data, 'calendar')


    def test_add_task_title(self):
        """
        Check if trying to add a task with a title in a format not allowed
        (for example: more than 120 characters) gives an error.
        """

        data = {
            "title": "a"*121,
            "description": "Test description",
            "priority": 3,
            "completed": True,
        }

        response = self.add_task(data, 'inbox')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['title'], ['Ensure this field has no more than 120 characters.'])


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
            "completed": True,
            "date": today
        }

        response = self.add_task(data, 'calendar')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['date'], ['Cannot set date to a past day.'])


    def test_add_task_priority(self):
        """
        Check if trying to add a task with a priority outside the range (0,3)
        gives an error.
        """
        
        data = {
            "title": "Test title",
            "description": "Test description",
            "priority": 4,
            "completed": True,
        }

        response = self.add_task(data, 'inbox')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['priority'], ['"4" is not a valid choice.'])


    def test_update_calendar(self):
        """
        Add a test task to calendar and try to update all the fields.
        """

        today = self.now.strftime('%Y-%m-%d')
        tomorrow = (self.now + timedelta(days=1)).strftime('%Y-%m-%d')

        data = {
            "title": "Test title",
            "description": "Test description",
            "priority": 0,
            "completed": False,
            "date": today
        }

        data_update = {
            "title": "Test update 1",
            "description": "Test update",
            "priority": 1,
            "completed": True,
            "date": tomorrow
        }

        response = self.add_task_test_fields_to_update(data, data_update, 'calendar')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_update_calendar_2(self):
        """
        Add a test task to calendar and try to update it with an unaccepted title.
        """

        today = self.now.strftime('%Y-%m-%d')

        data = {
            "title": "Test title",
            "description": "Test description",
            "priority": 0,
            "completed": False,
            "date": today
        }

        data_update = {
            "title": "a"*121,
            "description": "Test description",
            "priority": 0,
            "completed": False,
            "date": today
        }

        response = self.add_task_test_fields_to_update(data, data_update, 'calendar')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['title'], ['Ensure this field has no more than 120 characters.'])


    def test_update_calendar_3(self):
        """
        Add a test task to calendar and try to update it with an unaccepted date.
        """

        today = self.now.strftime('%Y-%m-%d')
        yesterday = (self.now - timedelta(days=1)).strftime('%Y-%m-%d')

        data = {
            "title": "Test title",
            "description": "Test description",
            "priority": 0,
            "completed": False,
            "date": today
        }

        data_update = {
            "title": "Test title",
            "description": "Test description",
            "priority": 0,
            "completed": False,
            "date": yesterday
        }

        response = self.add_task_test_fields_to_update(data, data_update, 'calendar')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['date'], ['Cannot set date to a past day.'])


    def test_update_inbox(self):
        """
        Add a test task to inbox and try to update all the fields.
        """

        data = {
            "title": "Test title",
            "description": "Test description",
            "priority": 0,
            "completed": False
        }

        data_update = {
            "title": "Test update",
            "description": "Test update",
            "priority": 1,
            "completed": True
        }

        response = self.add_task_test_fields_to_update(data, data_update, 'inbox')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_update_inbox_2(self):
        """
        Add a test task to inbox and try to update some field.
        """

        data = {
            "title": "Test title",
            "description": "Test description",
            "priority": 0,
            "completed": False
        }

        data_update = {
            "title": "Test update",
            "description": "",
            "priority": 1,
            "completed": True
        }

        response = self.add_task_test_fields_to_update(data, data_update, 'inbox')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    def test_update_inbox_3(self):
        """
        Add a test task to inbox and try to update some field.
        """

        data = {
            "title": "Test priority",
            "description": "Test description",
            "priority": 0,
            "completed": False
        }

        data_update = {
            "title": "Test priority",
            "description": "Test description",
            "priority": 4,
            "completed": False
        }

        response = self.add_task_test_fields_to_update(data, data_update, 'inbox')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['priority'], ['"4" is not a valid choice.'])



    def test_add_repeat_task(self):
        """
        Add a test task to calendar and repeat it, then check if the repetitions
        are created correctly.
        """

        today = self.now.strftime('%Y-%m-%d')
        until = (self.now + timedelta(days=4)).strftime('%Y-%m-%d')

        data = {
            "title": "Test priority",
            "description": "Test description",
            "priority": 0,
            "completed": False,
            "date": today
        }

        response = self.add_task(data, "calendar")

        data_repeat = {
            "task_id": response.json()['id'],
            "until": until,
            "every": 1
        }

        repetitions = self.repeat_task(data_repeat).json()

        date_repeated = self.now

        for r in repetitions:
            task = self.get_task(r, "calendar").json()

            date_repeated += timedelta(days=1)

            for key in task.keys():
                if key=="date":
                    self.assertEqual(date_repeated.strftime('%Y-%m-%d'), task["date"])
                
                elif key!="id" and key!="user_id":
                    self.assertEqual(task[key], data[key])


    def test_add_repeat_task_past_date(self):
        """
        Add a test task to calendar and repeat it, add a repetition with a past
        date and check if it gives an error.
        """

        today = self.now.strftime('%Y-%m-%d')
        until = (self.now - timedelta(days=4)).strftime('%Y-%m-%d')

        data = {
            "title": "Test priority",
            "description": "Test description",
            "priority": 0,
            "completed": False,
            "date": today
        }

        response = self.add_task(data, "calendar")

        data_repeat = {
            "task_id": response.json()['id'],
            "until": until,
            "every": 1
        }

        repetitions = self.repeat_task(data_repeat).json()
        self.assertEqual(repetitions['until'][0], "The date must be a day after today")


    def test_add_repeat_task_wrong_every(self):
        """
        Add a test task to calendar and repeat it, add a repetition with a negative
        value of day span (every) and check if it gives an error.
        """

        today = self.now.strftime('%Y-%m-%d')
        until = (self.now + timedelta(days=4)).strftime('%Y-%m-%d')

        data = {
            "title": "Test priority",
            "description": "Test description",
            "priority": 0,
            "completed": False,
            "date": today
        }

        response = self.add_task(data, "calendar")

        data_repeat = {
            "task_id": response.json()['id'],
            "until": until,
            "every": -1
        }

        repetitions = self.repeat_task(data_repeat).json()
        self.assertEqual(repetitions['every'][0], "The number must be greater than 0")


    def test_repeat_not_existing_task(self):
        """
        Try to repeat a task that doesn't exist.
        """

        until = (self.now + timedelta(days=4)).strftime('%Y-%m-%d')

        data_repeat = {
            "task_id": 999999,
            "until": until,
            "every": 1
        }

        repetitions = self.repeat_task(data_repeat).json()
        self.assertEqual(repetitions['task_id'][0], "Task not found")

    
