import unittest
import secrets
from bs4 import BeautifulSoup
from snapshot import backup, restore
from webtool import app


class WelcomeTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        backup("text/sign_text.txt")

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        restore("text/sign_text.txt")

    def test_welcome_page(self):
        tester = app.test_client()
        response = tester.get("/")
        self.assertEqual(200, response.status_code)
        self.assertTrue(b"Welcome to jforseth.tech" in response.data)

    # This is probably unnecessary
    def test_flaskapp_redirect(self):
        tester = app.test_client()
        response = tester.get("/FlaskApp")
        self.assertEqual(302, response.status_code)

    def test_about_page(self):
        tester = app.test_client()
        response = tester.get("/about")
        self.assertEqual(302, response.status_code)

    def test_instructions_page(self):
        tester = app.test_client()
        response = tester.get("/instructions")
        self.assertEqual(200, response.status_code)
        self.assertTrue(
            b"This is the place to find more detailed instructions for all of the various pages on my site. ",
            response.data,
        )

    def test_sign_edit_page(self):
        tester = app.test_client()
        response = tester.get("/sign/edit")
        self.assertEqual(200, response.status_code)
        self.assertTrue(b"signUpdated()" in response.data)

    def test_sign_page(self):
        tester = app.test_client()
        response = tester.get("/sign")
        self.assertEqual(200, response.status_code)
        self.assertTrue(b"signtext" in response.data)

    def test_editing_sign(self):
        tester = app.test_client()

        random_string = secrets.token_urlsafe(10)

        with open("text/sign_text.txt", "r") as file:
            original_text = file.read()
        self.assertNotEqual(original_text, random_string)

        response = tester.get("/sign/update", query_string=dict(text=random_string))
        self.assertEqual(200, response.status_code)

        with open("text/sign_text.txt", "r") as file:
            current_text = file.read()
        self.assertEqual(current_text, random_string)

    def test_italypics_redirect(self):
        tester = app.test_client()
        response = tester.get("/italypics")
        self.assertEqual(302, response.status_code)

    def test_jeopardy_redirect(self):
        tester = app.test_client()
        response = tester.get("/jeopardy")
        self.assertEqual(302, response.status_code)

if __name__ == "__main__":
    unittest.main()
