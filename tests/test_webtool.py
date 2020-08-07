import unittest
from webtool import app


class WebtoolTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True

    def tearDown(self):
        pass

    # Redundant. See test_welcome.py

    # def test_server_working(self):
    #    tester = app.test_client()
    #    response = tester.get("/")
    #    self.assertIs(200, response.status_code)
    #    self.assertTrue(b"Welcome" in response.data)

    def test_404_working(self):
        tester = app.test_client()
        response = tester.get("/thispagedoesnotexist")
        self.assertEqual(404, response.status_code)
        self.assertTrue(b"Oops" in response.data)


if __name__ == "__main__":
    unittest.main()
