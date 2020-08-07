import unittest
import os
from io import BytesIO
from webtool import app


class FileSharingTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        original_files = os.listdir("uploads")
        with open("tests/file_sharing_original_files.txt", "w") as file:
            file.writelines(original_files)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        with open("tests/file_sharing_original_files.txt", "r") as file:
            original_files = file.readlines()
        for file in os.listdir("uploads"):
            if file not in original_files:
                os.remove("uploads/" + file)
        os.remove("tests/file_sharing_original_files.txt")

    def test_file_sharing_page(self):
        tester = app.test_client(self)
        response = tester.get("/filesharing", content_type="html/text")
        self.assertIs(200, response.status_code)
        self.assertTrue(b"Upload" in response.data)

    def test_file_sharing_upload(self):
        with app.test_client(self) as tester:

            class TestFile:
                content = bytes("Testing, testing, 123", "utf-8")
                name = "test.txt"

            testfile = TestFile()
            response = tester.post(
                "/filesharing",
                data=dict(file=(BytesIO(testfile.content), testfile.name)),
                follow_redirects=True,
            )
            self.assertIs(200, response.status_code)
            self.assertEqual(testfile.content in response.data)
            response = tester.get("/filesharing")
            self.assertIs(200, response.status_code)
            self.assertTrue(testfile.name, str(response.data))


if __name__ == "__main__":
    unittest.main()
