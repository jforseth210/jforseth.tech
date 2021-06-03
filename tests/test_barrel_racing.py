import unittest
from bs4 import BeautifulSoup
from webtool import app
from snapshot import backup, restore
import os


class BarrelRacingTestCase(unittest.TestCase):

    # Make a copy of the original file to restore from after the tests are finished.
    def setUp(self):
        app.config["TESTING"] = True

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        backup("/var/www/jforseth.tech/text/barrel_racing_current_number.txt")

    # Replace the modified file with the original.
    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        restore("/var/www/jforseth.tech/text/barrel_racing_current_number.txt")

    def test_counter_displayed(self):
        tester = app.test_client(self)
        response = tester.get("/barrelracing/counter", content_type="html/text")
        self.assertTrue(b"is currently" in response.data)
        with open("/var/www/jforseth.tech/text/barrel_racing_current_number.txt", "r") as file:
            original_value = file.read()
        self.assertTrue(original_value, str(response.data))

    def test_increment(self):
        with app.test_client() as tester:
            response = tester.get("/barrelracing/counter")
            soup = BeautifulSoup(response.data, "html.parser")
            plus_value = soup.find(id="plushidden")["value"]
            response = tester.post(
                "/barrelracing/current_number_update",
                data=dict(current_number=plus_value),
                follow_redirects=True,
            )
            self.assertTrue(bytes(plus_value, "ascii") in response.data)
            self.assertIs(200, response.status_code)

    def test_decrement(self):
        with app.test_client() as tester:
            response = tester.get("/barrelracing/counter")
            soup = BeautifulSoup(response.data, "html.parser")
            minus_value = soup.find(id="minushidden")["value"]
            response = tester.post(
                "/barrelracing/current_number_update",
                data=dict(current_number=minus_value),
                follow_redirects=True,
            )
            self.assertTrue(bytes(minus_value, "ascii") in response.data)
            self.assertIs(200, response.status_code)

    def test_current_number_file_exists(self):
        self.assertTrue(os.path.isfile("/var/www/jforseth.tech/text/barrel_racing_current_number.txt"))


if __name__ == "__main__":
    unittest.main()
