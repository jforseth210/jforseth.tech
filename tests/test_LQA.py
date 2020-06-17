import unittest
from webtool import app
from test_accounts import login


class LQATestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True

    def tearDown(self):
        pass

    def test_lqa_no_login(self):
        tester = app.test_client(self)
        response = tester.get("/lqa", follow_redirects=True)
        self.assertIs(200, response.status_code)
        self.assertIn(b"You need to sign in to use this feature.", response.data)

    def test_lqa_logged_in(self):
        with app.test_client(self) as tester:
            login(tester)
            response = tester.get("/lqa")
            self.assertIs(200, response.status_code)
            self.assertIn(b"Teton County LQA", response.data)

    def test_other_lqa_pages_logged_out(self):
        tester = app.test_client(self)
        for page in range(15):
            response = tester.get("/lqa/" + str(page + 1), follow_redirects=True)
            self.assertIs(200, response.status_code)
            self.assertIn(b"You need to sign in to use this feature.", response.data)

    def test_other_lqa_pages_logged_in(self):
        with app.test_client(self) as tester:
            login(tester)
            for page in range(15):
                response = tester.get("/lqa/" + str(page + 1))
                self.assertIs(200, response.status_code)
                self.assertIn("Station " + str(page + 1), str(response.data))


if __name__ == "__main__":
    unittest.main()
