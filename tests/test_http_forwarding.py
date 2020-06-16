import unittest
from webtool import app

class HTTPForwardingTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"]=True
    def tearDown(self):
        pass

    def test_HTTPForwarding(self):
        pass

if __name__ == '__main__':
    unittest.main()