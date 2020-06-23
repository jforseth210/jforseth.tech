import unittest
import os
from shutil import copytree, rmtree, move
from webtool import app
from test_accounts import signup, login

class WriterTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        try:
            copytree('userdata/', 'tests/userdata/')
        except FileExistsError:
            rmtree('tests/userdata/')
            copytree('userdata/', 'tests/userdata/')
        signup(app.test_client())

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        rmtree('userdata/')
        move('tests/userdata/', 'userdata/')

    def test_writer_home_logged_in(self):
        with app.test_client() as tester:
            login(tester)
            response = tester.get('/writer')
            documents = os.listdir('userdata/')
            for document in documents:
                self.assertIn(document, str(response.data))

if __name__ == "__main__":
    unittest.main()
