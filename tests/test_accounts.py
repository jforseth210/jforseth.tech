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
def login(app):
    response = app.get('/login/')
    soup = BeautifulSoup(response.data, 'html.parser')
    token = soup.find(id='csrf_token')['value']
    response = app.post('/login', data=dict(csrf_token=token, username='testing', password=PROJECT_PASSWORD, next='/'), follow_redirects=True)
    return response

class AccountsTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_login_page(self):
        response = self.app.get('/login/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Username" in response.data)
        self.assertTrue(b"Password" in response.data)
        self.assertTrue(b"Forgot Password" in response.data)

    def test_correct_login(self):
        with app:
            response = login(app)
            self.assertIn(b"Login Successful", response.data)
            self.assertEqual(response.status_code, 200)

    def test_correct_login_no_csrf(self):
        with app:
            response = app.get('/login/')
            response = app.post('/login', data=dict(username='testing', password=PROJECT_PASSWORD, next='/'), follow_redirects=True)
            self.assertIn(b"token is missing", response.data)
            self.assertEqual(response.status_code, 200)

    def test_incorrect_username(self):
        with app:
            response = app.get('/login/')
            soup = BeautifulSoup(response.data, 'html.parser')
            token = soup.find(id='csrf_token')['value']
            response = app.post('/login', data=dict(csrf_token=token, username='thisuserdoesnotexist', password=PROJECT_PASSWORD, next='/'), follow_redirects=True)
            self.assertIn(b"Account not found", response.data)
            self.assertEqual(response.status_code, 401)

    def test_incorrect_password(self):
        with app:
            response = app.get('/login/')
            soup = BeautifulSoup(response.data, 'html.parser')
            token = soup.find(id='csrf_token')['value']
            response = app.post('/login', data=dict(csrf_token=token, username='testing', password='this is the wrong password', next='/'), follow_redirects=True)
            self.assertIn(b"Incorrect password", response.data)
            self.assertEqual(response.status_code, 401)

    def test_account_no_login(self):
        response = app.get('/account/testing',
                              content_type='html/text', follow_redirects=False)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(b"Oops" in response.data)

if __name__ == '__main__':
    unittest.main()
