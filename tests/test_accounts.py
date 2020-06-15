import unittest
from bs4 import BeautifulSoup
from webtool import app
from SensitiveData import PROJECT_PASSWORD

class FlaskTestCase(unittest.TestCase):
    def test_login_page(self):
        tester = app.test_client(self)
        response = tester.get('/login/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Username" in response.data)
        self.assertTrue(b"Password" in response.data)
        self.assertTrue(b"Forgot Password" in response.data)

    def test_login(self):
        with app.test_client() as tester:
            response = tester.get('/login/')
            soup = BeautifulSoup(response.data, 'html.parser')
            token = soup.find(id='csrf_token')['value']
            response = tester.post('/login', data=dict(csrf_token=token, username='testing', password=PROJECT_PASSWORD, next='/'), follow_redirects=True)
            self.assertIn(b"Login Successful", response.data)