from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse


class AccountTest(APITestCase):

    @staticmethod
    def create_test_account(username, password):
        user = get_user_model()
        test_user = user.objects.create(name=username, gender=1, phone_number='1234567788')
        test_user.set_password(password)
        test_user.save()
        return test_user

    def test_login(self):
        username = "Test User"
        password = "TestCaseDjango@2020"
        test_user = self.create_test_account(username, password)
        self.assertEqual(username, test_user.username, "Account Creation Test")
        response = self.client.post(reverse('login'), data={'username': username, 'password': password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
