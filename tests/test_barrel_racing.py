import unittest
from bs4 import BeautifulSoup
from webtool import app
from SensitiveData import PROJECT_PASSWORD

class FlaskTestCase(unittest.TestCase):
    def test_counter_displayed(self):
        # Admin contains a number of security risks.
        # It has been disabled and should return 404.
        tester = app.test_client(self)
        response = tester.get('/barrelracing/counter/', content_type='html/text')
        self.assertIn(b'Horse #', response.data)