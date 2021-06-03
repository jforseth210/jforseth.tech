import unittest
from webtool import app
from test_accounts import login, signup
from account_management import grant_access, get_current_access, get_account
from snapshot import backup, backuptree, restoretree, restore


class LQATestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        backup("/var/www/jforseth.tech/database.db")
        backuptree("userdata/")
        signup(app.test_client())
        grant_access("testing", "lqa")

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        restore("/var/www/jforseth.tech/database.db")
        restoretree("userdata/")

    def test_lqa_no_login(self):
        tester = app.test_client(self)
        response = tester.get("/lqa", follow_redirects=True)
        self.assertIs(200, response.status_code)
        self.assertTrue(b"You need to sign in to use this feature." in response.data)

    def test_lqa_logged_in(self):
        with app.test_client(self) as tester:
            response = login(tester)
            response = tester.get("/lqa")
            self.assertIs(200, response.status_code)
            self.assertTrue(b"Teton County LQA" in response.data)

    def test_other_lqa_pages_logged_out(self):
        tester = app.test_client(self)
        for page in range(15):
            response = tester.get("/lqa/" + str(page + 1), follow_redirects=True)
            self.assertIs(200, response.status_code)
            self.assertTrue(b"You need to sign in to use this feature." in response.data)

    def test_other_lqa_pages_logged_in(self):
        with app.test_client(self) as tester:
            response = login(tester)
            for page in range(15):
                response = tester.get("/lqa/" + str(page + 1))
                self.assertIs(200, response.status_code)
                self.assertTrue("Station " + str(page + 1), str(response.data))


if __name__ == "__main__":
    unittest.main()
