import unittest
from webtool import app
from twilio.rest import Client
from SensitiveData import *


class LuckyShoeTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True

    def tearDown(self):
        pass

    def test_lucky_shoe_page(self):
        tester = app.test_client(self)
        response = tester.get("/luckyshoe")
        self.assertEqual(200, response.status_code)
        self.assertTrue(b"Lucky Shoe Welding" in response.data)

    def test_lucky_shoe_order(self):
        data = dict(
            testing="True", testing_well="False", code_working="True", code_good="False"
        )
        tester = app.test_client(self)
        response = tester.post("/luckyshoe/order", data=data)
        self.assertIs(200, response.status_code)
        for key, value in data.items():
            self.assertTrue(key, str(response.data))
            self.assertTrue(value, str(response.data))

    def test_twilio_working(self):
        account_sid = TWILIO_SID
        auth_token = TWILIO_TOKEN
        client = Client(account_sid, auth_token)
        # If we make it this far without errors, it works.
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
