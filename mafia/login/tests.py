from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
import datetime

# def create_user(username, password):
    # Creates a user with a given username and password
    # return User.objects.create_user(question_text=question_text, pub_date=time)# user = User.objects.create(name=)

class LoginIndexViewTests(TestCase):
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
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), 'Please enter a correct username and password. Note that both fields may be case-sensitive.')
    def test_incorrect_password(self):
        credentials = {
            'username': 'user',
            'password': 'password'
        }
        User.objects.create_user(**credentials)
        credentials['password'] = 'wrong_password'
        response = self.client.post('/login/', credentials, follow=True)
        self.assertIs(response.context['user'].is_active, False)
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), 'Please enter a correct username and password. Note that both fields may be case-sensitive.')


class LoginLogoutViewTests(TestCase):
    def test_successful_logout(self):
        credentials = {
            'username': 'user',
            'password': 'password'
        }
        User.objects.create_user(**credentials)
        #login
        login = self.client.login(**credentials)
        #logout
        response = self.client.get('/login/logout/', follow=True)
        #user would be missing from the response if logged out
        self.assertNotIn('user', response.context)

class LoginSignupViewTests(TestCase):
    def test_successful_signup(self):
        credentials = {
            'username': 'user',
            'password1': 'password',
            'password2': 'password',
        }
        response = self.client.post('/login/signup/', data=credentials, follow=True)
        self.assertIs(User.objects.filter(username=credentials['username']).exists(), True)
    def test_password_mismatch_signup(self):
        credentials = {
            'username': 'user',
            'password1': 'password',
            'password2': 'different_password',
        }
        response = self.client.post('/login/signup/', data=credentials, follow=True)
        self.assertIs(User.objects.filter(username=credentials['username']).exists(), False)
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), 'The two password fields didn’t match.')
    def test_username_exists_signup(self):
        credentials = {
            'username': 'user',
            'password': 'password'
        }
        User.objects.create_user(**credentials)
        self.assertIs(User.objects.filter(username=credentials['username']).exists(), True)
        credentials = {
            'username': 'user',
            'password1': 'password',
            'password2': 'password',
        }
        response = self.client.post('/login/signup/', data=credentials, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), 'A user with that username already exists.')
    def test_username_exists_password_mismatch_signup(self):
        credentials = {
            'username': 'user',
            'password': 'password'
        }
        User.objects.create_user(**credentials)
        self.assertIs(User.objects.filter(username=credentials['username']).exists(), True)
        credentials = {
            'username': 'user',
            'password1': 'password',
            'password2': 'different_password',
        }
        response = self.client.post('/login/signup/', data=credentials, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), 'The two password fields didn’t match.')
        self.assertEqual(str(messages[1]), 'A user with that username already exists.')

class LoginChangePasswordTests(TestCase):
    def test_successful_change_password(self):
        credentials = {
            'username': 'user',
            'password': 'password'
        }
        User.objects.create_user(**credentials)
        login = self.client.login(**credentials)
        credentials = {
            'username': 'user',
            'old_password': 'password',
            'new_password1': 'diff_password',
            'new_password2': 'diff_password',
        }
        response = self.client.post('/login/change_password/', data=credentials, follow=True)
        #should be logged in again
        self.assertIs(response.context['user'].is_active, True)
        user = User.objects.filter(username=credentials['username'])[0]
        self.assertIs(user.check_password(credentials['new_password1']), True)
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), 'Your password was successfully updated.')
        self.assertEqual(str(messages[1]), 'You have been logged in with your new credentials.')

    def test_wrong_old_password_change_password(self):
        credentials = {
            'username': 'user',
            'password': 'password'
        }
        User.objects.create_user(**credentials)
        login = self.client.login(**credentials)
        credentials = {
            'username': 'user',
            'old_password': 'password1',
            'new_password1': 'diff_password',
            'new_password2': 'diff_password',
        }
        response = self.client.post('/login/change_password/', data=credentials, follow=True)
        #should be logged in again
        self.assertIs(response.context['user'].is_active, True)
        user = User.objects.filter(username=credentials['username'])[0]
        self.assertIs(user.check_password(credentials['new_password1']), False)
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), 'Your old password was entered incorrectly. Please enter it again.')
    def test_diff_new_passwords_change_password(self):
        credentials = {
            'username': 'user',
            'password': 'password'
        }
        User.objects.create_user(**credentials)
        login = self.client.login(**credentials)
        credentials = {
            'username': 'user',
            'old_password': 'password',
            'new_password1': 'diff_password',
            'new_password2': 'another_diff_password',
        }
        response = self.client.post('/login/change_password/', data=credentials, follow=True)
        #should be logged in again
        self.assertIs(response.context['user'].is_active, True)
        user = User.objects.filter(username=credentials['username'])[0]
        self.assertIs(user.check_password(credentials['new_password1']), False)
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), 'The two password fields didn’t match.')
    def test_wrong_old_password_diff_new_passwords_change_password(self):
        credentials = {
            'username': 'user',
            'password': 'password'
        }
        User.objects.create_user(**credentials)
        login = self.client.login(**credentials)
        credentials = {
            'username': 'user',
            'old_password': 'password1',
            'new_password1': 'diff_password',
            'new_password2': 'another_diff_password',
        }
        response = self.client.post('/login/change_password/', data=credentials, follow=True)
        #should be logged in again
        self.assertIs(response.context['user'].is_active, True)
        user = User.objects.filter(username=credentials['username'])[0]
        self.assertIs(user.check_password(credentials['new_password1']), False)
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), 'Your old password was entered incorrectly. Please enter it again.')
        self.assertEqual(str(messages[1]), 'The two password fields didn’t match.')


class UserModelTests(TestCase):
    def test_has_username(self):
        user = User(username='username', password='password')
        # self.assertEqual(len(user.username), 8)
        self.assertIs(len(user.username) > 0, True)
    def test_hashed_password(self):
        user = User(username='username', password=make_password('password'))
        self.assertIs(user.check_password('password'), True)
