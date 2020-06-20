import unittest
from webtool import app


class WebtoolTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True

    def tearDown(self):
        pass

    def test_server_working(self):
        tester = app.test_client()
        response = tester.get("/")
        self.assertIs(200, response.status_code)
        self.assertIn(b"Welcome", response.data)

    def test_404_working(self):
        tester = app.test_client()
        response = tester.get("/thispagedoesnotexist")
        self.assertEqual(404, response.status_code)
        self.assertIn(b"Oops", response.data)


if __name__ == "__main__":
    unittest.main()