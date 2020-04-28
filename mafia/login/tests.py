from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
import datetime

# def create_user(username, password):
    # Creates a user with a given username and password
    # return User.objects.create_user(question_text=question_text, pub_date=time)# user = User.objects.create(name=)

class UserIndexViewTests(TestCase):
    def test_existing_user_login(self):
        credentials = {
            'username': 'user',
            'password': 'password'
        }
        User.objects.create_user(**credentials)
        response = self.client.post('/login/', credentials, follow=True)
        self.assertIs(response.context['user'].is_active, True)
    def test_nonexisting_user_login(self):
        credentials = {
            'username': 'user',
            'password': 'password'
        }
        User.objects.create_user(**credentials)
        credentials['username'] = 'other_user'
        response = self.client.post('/login/', credentials, follow=True)
        self.assertIs(response.context['user'].is_active, False)


class UserModelTests(TestCase):
    def test_has_username(self):
        user = User(username='username', password='password')
        # self.assertEqual(len(user.username), 8)
        self.assertIs(len(user.username) > 0, True)
    def test_hashed_password(self):
        user = User(username='username', password=make_password('password'))
        self.assertIs(user.check_password('password'), True)
