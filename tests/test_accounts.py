import unittest
from bs4 import BeautifulSoup
from webtool import app
from SensitiveData import PROJECT_PASSWORD
#TODO: Edge cases: Unicode characters, XSS, SQL Injection
#TODO: Setup and teardown
#TODO: Signup
#TODO: Email changes
#TODO: Password changes
#TODO: Prayer additions and unsubcriptions (maybe in test_prayer).
#TODO: Account deletion
class AccountsTestCase(unittest.TestCase):
    def test_login_page(self):
        tester = app.test_client(self)
        response = tester.get('/login/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Username" in response.data)
        self.assertTrue(b"Password" in response.data)
        self.assertTrue(b"Forgot Password" in response.data)

    def test_correct_login(self):
        with app.test_client() as tester:
            response = tester.get('/login/')
            soup = BeautifulSoup(response.data, 'html.parser')
            token = soup.find(id='csrf_token')['value']
            response = tester.post('/login', data=dict(csrf_token=token, username='testing', password=PROJECT_PASSWORD, next='/'), follow_redirects=True)
            self.assertIn(b"Login Successful", response.data)
            self.assertEqual(response.status_code, 200)

    def test_correct_login_no_csrf(self):
        with app.test_client() as tester:
            response = tester.get('/login/')
            response = tester.post('/login', data=dict(username='testing', password=PROJECT_PASSWORD, next='/'), follow_redirects=True)
            self.assertIn(b"token is missing", response.data)
            self.assertEqual(response.status_code, 200)

    def test_incorrect_username(self):
        with app.test_client() as tester:
            response = tester.get('/login/')
            soup = BeautifulSoup(response.data, 'html.parser')
            token = soup.find(id='csrf_token')['value']
            response = tester.post('/login', data=dict(csrf_token=token, username='thisuserdoesnotexist', password=PROJECT_PASSWORD, next='/'), follow_redirects=True)
            self.assertIn(b"Account not found", response.data)
            self.assertEqual(response.status_code, 401)

    def test_incorrect_password(self):
        with app.test_client() as tester:
            response = tester.get('/login/')
            soup = BeautifulSoup(response.data, 'html.parser')
            token = soup.find(id='csrf_token')['value']
            response = tester.post('/login', data=dict(csrf_token=token, username='testing', password='this is the wrong password', next='/'), follow_redirects=True)
            self.assertIn(b"Incorrect password", response.data)
            self.assertEqual(response.status_code, 401)

    def test_account_no_login(self):
        tester = app.test_client(self)
        response = tester.get('/account/testing',
                              content_type='html/text', follow_redirects=False)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(b"Oops" in response.data)
