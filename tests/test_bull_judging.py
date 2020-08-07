import unittest
from webtool import app


class BullJudgingTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True

    def test_bulljudging_start(self):
        tester = app.test_client(self)
        response = tester.get("/bulljudging", content_type="html/text")
        self.assertTrue(b"Start" in response.data)
        self.assertIs(200, response.status_code)

    def test_bulljudging_one(self):
        tester = app.test_client(self)
        response = tester.get("/bulljudging1", content_type="html/text")
        self.assertTrue(b"bull1.png" in response.data)
        self.assertIs(200, response.status_code)

    def test_bulljudging_two(self):
        tester = app.test_client(self)
        response = tester.get("/bulljudging2", content_type="html/text")
        self.assertTrue(b"bull5.png" in response.data)
        self.assertIs(200, response.status_code)

    def test_bulljudging_three(self):
        tester = app.test_client(self)
        response = tester.get("/bulljudging3", content_type="html/text")
        self.assertTrue(b"bull9.png" in response.data)
        self.assertIs(200, response.status_code)

    def test_bulljudging_four(self):
        tester = app.test_client(self)
        response = tester.get("/bulljudging4", content_type="html/text")
        self.assertTrue(b"bull13.png" in response.data)
        self.assertIs(200, response.status_code)

    def test_bulljudging_done(self):
        tester = app.test_client(self)
        response = tester.get("/bulljudgingdone", content_type="html/text")
        self.assertTrue(b"That's all" in response.data)
        self.assertIs(200, response.status_code)


if __name__ == "__main__":
    unittest.main()
