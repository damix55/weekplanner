from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
import time


class RegistrationTests(APITestCase):

    def test_create_user(self):
        """
        Add a new user.
        """
        url=reverse("users:create_user")
        data = {"email": "test.test@test.test",
                "user_name": "test",
                "password": "test000"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_empty_fields(self):
        """
        Check if trying to submit the form without
        filling any field returns an error.
        """
        url=reverse("users:create_user")
        data = {"email": "",
                "user_name": "",
                "password": ""}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['email'][0], "This field may not be blank.")
        self.assertEqual(response.json()['user_name'][0], "This field may not be blank.")
        self.assertEqual(response.json()['password'][0], "This field may not be blank.")

    def test_create_user_email(self):
        """
        Check if trying to add a user with an invalid
        e-mail format returns an error.
        """
        url=reverse("users:create_user")
        data = {"email": "test.test@test",
                "user_name": "test",
                "password": "test000"}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['email'][0], "Enter a valid email address.")

    def test_create_user_password(self):
        """
        Check if trying to add a user with a password
        length smaller than 6 characters returns an error.
        """
        url=reverse("users:create_user")
        data = {"email": "test.test@test.test",
                "user_name": "test",
                "password": "test0"}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['password'][0], "Password must be longer than 6 characters.")

    def test_create_user_email_already_exists(self):
        """
        Check if trying to add a user with an e-mail 
        already taken returns an error.
        """
        url=reverse("users:create_user")
        data1 = {"email": "test.test@test.test",
                "user_name": "test",
                "password": "test000"}
        data2 = {"email": "test.test@test.test",
                 "user_name": "test0",
                 "password": "test000"}

        response1 = self.client.post(url, data1, format='json')
        response2 = self.client.post(url, data2, format='json')

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.json()['email'][0], "user with this email address already exists.")

    def test_create_user_username_already_exists(self):
        """
        Check if trying to add a user with a password
        length smaller than 6 characters an error response
        is returned
        """
        url=reverse("users:create_user")
        data1 = {"email": "test.test@test.test",
                "user_name": "test",
                "password": "test000"}
        data2 = {"email": "test.test@test.test0",
                 "user_name": "test",
                 "password": "test000"}

        response1 = self.client.post(url, data1, format='json')
        response2 = self.client.post(url, data2, format='json')

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.json()['user_name'][0], "user with this user name already exists.")


class LoginTests(APITestCase):

    def test_login(self):
        """
        Login.
        """
        # register a new user
        url=reverse("users:create_user")
        data = {"email": "test.test@test.test",
                "user_name": "test",
                "password": "test000"}
        self.client.post(url, data, format='json')

        # login with correct credentials
        url=reverse("token_obtain_pair")
        data = {"email": "test.test@test.test",
                "password": "test000"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()['access'])
        self.assertIsNotNone(response.json()['refresh'])

        # login with wrong password
        url=reverse("token_obtain_pair")
        data = {"email": "test.test@test.test",
                "password": "test0000"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['detail'], "No active account found with the given credentials")

        # login with wrong e-mail
        url=reverse("token_obtain_pair")
        data = {"email": "test.test@test.testt",
                "password": "test000"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['detail'], "No active account found with the given credentials")

        # login with wrong password and e-mail
        url=reverse("token_obtain_pair")
        data = {"email": "test.test@test.testt",
                "password": "test0000"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['detail'], "No active account found with the given credentials")

        # login with empty fields
        url=reverse("token_obtain_pair")
        data = {"email": "",
                "password": ""}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['email'][0], "This field may not be blank.")
        self.assertEqual(response.json()['password'][0], "This field may not be blank.")


    # before running this test go to week_planner/settings.py
    # and change the property 'REFRESH_TOKEN_LIFETIME' setting it
    # to: timedelta(minutes=1)
    def test_refresh_token(self):
        """
        Refresh token.
        """

        # register a new user
        url=reverse("users:create_user")
        data = {"email": "test.test@test.test",
                "user_name": "test",
                "password": "test000"}
        self.client.post(url, data, format='json')

        # login with credentials
        url=reverse("token_obtain_pair")
        data = {"email": "test.test@test.test",
                "password": "test000"}
        response = self.client.post(url, data, format='json')

        access_token = response.json()['access']
        refresh_token = response.json()['refresh']

        # check that a new access token is returned
        url=reverse("token_refresh")
        data = {"refresh": refresh_token}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.json()['access'], access_token)

        # check con refresh token expired
        #time.sleep(65)
        #url=reverse("token_refresh")
        #data = {"refresh": refresh_token}
        #response = self.client.post(url, data, format='json')
        #self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        #self.assertEqual(response.json()['detail'], "Token is invalid or expired")
        #self.assertEqual(response.json()['code'], "token_not_valid")

        # check con refresh token sbagliato
        url=reverse("token_refresh")
        data = {"refresh": "test"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['detail'], "Token is invalid or expired")
        self.assertEqual(response.json()['code'], "token_not_valid")

        # check con campo vuoto
        url=reverse("token_refresh")
        data = {"refresh": ""}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['refresh'][0], "This field may not be blank.")

    def test_blacklist_token(self):
        """
        Blacklist token.
        """

        # register a new user
        url=reverse("users:create_user")
        data = {"email": "test.test@test.test",
                "user_name": "test",
                "password": "test000"}
        self.client.post(url, data, format='json')

        # login with credentials
        url=reverse("token_obtain_pair")
        data = {"email": "test.test@test.test",
                "password": "test000"}
        response = self.client.post(url, data, format='json')

        access_token = response.json()['access']
        refresh_token = response.json()['refresh']

        url=reverse("users:blacklist")
        data = {"refresh_token": refresh_token}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check that it is not possible to obtain
        # an access token using the blacklisted
        # refresh token
        url=reverse("token_refresh")
        data = {"refresh": refresh_token}
        #self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        #self.assertEqual(response.json()['detail'], "Token is blacklisted")
        #self.assertEqual(response.json()['code'], "token_not_valid")


        
        











