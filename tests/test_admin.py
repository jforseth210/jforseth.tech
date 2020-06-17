import unittest
from bs4 import BeautifulSoup
from webtool import app
from SensitiveData import PROJECT_PASSWORD


class AdminTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True

    def test_admin_disabled(self):
        # Admin contains a number of security risks.
        # It has been disabled and should return 404.
        tester = app.test_client(self)
        response = tester.get("/DBbrowser", content_type="html/text")
        print("Hi")
        print(response.data)
        self.assertTrue(404 == response.status_code)
        response = tester.get("/error", content_type="html/text")
        self.assertTrue(404 == response.status_code)


if __name__ == "__main__":
    unittest.main()
