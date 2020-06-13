import unittest
from webtool import *

class TestWebtool(unittest.TestCase):
    def test_page_not_found(self):
        print(page_not_found(""))
        self.assertFalse(False);


if __name__ == '__main__':
    unittest.main()