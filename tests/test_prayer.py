import unittest
import json
from webtool import app
from SensitiveData import TESTING_GROUP_SIGNUP_CODE
from test_accounts import signup, login
import html


class PrayerTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True

    def tearDown(self):
        pass

    def test_prayer_requests_page(self):
        tester = app.test_client(self)
        response = tester.get("/prayer", content_type="html/text")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Request Prayer" in response.data)

    def test_prayer_request(self):
        name = "Testing"
        parish = "TestParish"
        prequest = "This should only go to the test user. If it doesn't, something has broken. Please email me at support@jforseth.tech"
        tester = app.test_client(self)
        response = tester.post(
            "/prayer/prayerrequest",
            data=dict(name=name, parish=parish, prequest=prequest),
        )
        responsedict = json.loads(response.data.decode("utf-8"))
        self.assertEqual(type(responsedict["emails"]), type([]))
        self.assertIn(parish, responsedict["subject_template"])
        self.assertIn(name, responsedict["subject_template"])
        self.assertIn(prequest, html.unescape(responsedict["message_template"]))

    def test_prayer_subscription(self):
        with app.test_client() as tester:
            signup(tester, parish="")
            login(tester)
            response = tester.post(
                "/prayer/addgroup",
                data=dict(group=TESTING_GROUP_SIGNUP_CODE),
                follow_redirects=True,
            )
        with app.test_client() as tester:
            login(tester)
            response = tester.get("/account/testing")
            self.assertTrue(b"Testing" in response.data)
            self.assertEqual(200, response.status_code)

    def test_prayer_unsubscription(self):
        with app.test_client() as tester:
            signup(tester)
            login(tester)
            tester.get('/prayer/unsubscribe_logged_in', ) 
if __name__ == "__main__":
    unittest.main()
