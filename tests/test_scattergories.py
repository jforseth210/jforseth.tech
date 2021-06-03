import unittest
from bs4 import BeautifulSoup
from bs4.diagnose import diagnose
from snapshot import backup, restore
from webtool import app


class ScattergoriesTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        backup("/var/www/jforseth.tech/text/currentcatergorylist.txt")
        backup("/var/www/jforseth.tech/text/allcatergorylist.txt")
        backup("/var/www/jforseth.tech/text/scattergoriescurrentletter.txt")

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        restore("/var/www/jforseth.tech/text/currentcatergorylist.txt")
        restore("/var/www/jforseth.tech/text/allcatergorylist.txt")
        restore("/var/www/jforseth.tech/text/scattergoriescurrentletter.txt")

    def test_scattegories_main_page(self):
        tester = app.test_client()
        response = tester.get("/scattergories")
        self.assertEqual(200, response.status_code)
        self.assertTrue(b"Scattergories: " in response.data)

    def test_scattegories_newlist_page(self):
        tester = app.test_client()
        response = tester.get("/scattergories")
        soup = BeautifulSoup(response.data, "html.parser")
        original_categories = soup.find_all("p")

        response = tester.get("/scattergories/newlist")
        self.assertEqual(200, response.status_code)
        self.assertEqual(b"Done", response.data)

        response = tester.get("/scattergories")
        soup = BeautifulSoup(response.data, "html.parser")
        new_categories = soup.find_all("p")

        self.assertNotEqual(original_categories, new_categories)

    def test_scattegories_roll_page(self):
        tester = app.test_client()
        response = tester.get("/scattergories")
        soup = BeautifulSoup(response.data, "html.parser")
        original_letter = soup.find_all("h1")

        response = tester.get("/scattergories/roll")
        self.assertEqual(200, response.status_code)
        self.assertEqual(b"Done", response.data)

        response = tester.get("/scattergories")
        soup = BeautifulSoup(response.data, "html.parser")
        new_letter = soup.find_all("h1")

        self.assertNotEqual(original_letter, new_letter)


if __name__ == "__main__":
    unittest.main()
