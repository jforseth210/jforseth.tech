import unittest
import shutil import copyfile
from webtool import app

class WriterTestCase(unittest.TestCase):
  def setUp(self):
    app.config["TESTING"] = True

  @classmethod
  def setUpClass(cls):
    app.config["TESTING"] = True

  def tearDown(self):
    pass

  @classmethod
  def tearDownClass(cls):
    pass

  def test_test(self):
      tester = app.test_client()
      response = tester.get()

if __name__ == "__main__":
   unittest.main()
  