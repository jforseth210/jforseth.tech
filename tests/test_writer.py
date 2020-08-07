import unittest
from webtool import app
from test_accounts import signup, login
from snapshot import backuptree, restoretree
import os


class WriterTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        backuptree("userdata/")
        signup(app.test_client())

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        restoretree("userdata/")

    def test_writer_home_logged_in(self):
        with app.test_client() as tester:
            login(tester)
            response = tester.get("/writer")
            documents = os.listdir("userdata/testing/writer/documents/")
            for document in documents:
                self.assertTrue(document, str(response.data))


if __name__ == "__main__":
    unittest.main()
