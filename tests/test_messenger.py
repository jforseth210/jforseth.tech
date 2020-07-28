import unittest
from webtool import app
from snapshot import backup, restore
import time


class MessengerTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        backup("database.db")

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        restore("database.db")

    def test_messenger_page(self):
        tester = app.test_client(self)
        response = tester.get("/messenger", content_type="html/text")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Clear" in response.data)

    def test_chat_submission(self):
        tester = app.test_client(self)
        response = tester.post(
            "/messenger/result", data=dict(message="Hi"), follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        # print(response.data)
        self.assertTrue(b"<li class='message'> Hi </li>" in response.data)

    def test_chat_deletion(self):
        tester = app.test_client(self)
        response = tester.post(
            "/messenger/result",
            data=dict(message="This shouldn't show up after the db is cleared."),
            follow_redirects=True,
        )
        response = tester.post(
            "/messenger/clear", content_type="html/text", follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"<li class='message'>" not in response.data)


if __name__ == "__main__":
    unittest.main()
