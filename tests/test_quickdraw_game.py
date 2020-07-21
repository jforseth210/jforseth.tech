import unittest
from webtool import app
from test_accounts import login
from snapshot import backup, restore

class QuickdrawTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        backup('text/locked.txt')
    
    @classmethod
    def tearDownClass(self):
        restore('text/locked.txt')
    
    def test_quickdraw_big_screen(self):
        tester = app.test_client()
        response = tester.get('/quickdraw/bigscreen')
        self.assertIs(200, response.status_code)
        self.assertIn(b'When I say go, shoot!', response.data)
    
    def test_quickdraw_big_screen_begin(self):
        tester = app.test_client()
        for i in range(1,30):
            response = tester.get('/quickdraw/bigscreen/begin')
            self.assertIs(200, response.status_code)
            self.assertTrue(b'GO!' in response.data or b'Not yet' in response.data)

    def test_quickdraw(self):
        with app.test_client() as tester:
            login(tester)
            response = tester.get('/quickdraw')
        self.assertEqual(200, response.status_code)
        self.assertIn(b'SHOOT!', response.data)

    def test_quickdraw_shot(self):
        tester = app.test_client()
        response = tester.get('/quickdraw/shot', data=dict(user="testing"))
        self.assertIs(200, response.status_code)
        self.assertTrue(b'You were fastest!' in response.data or b'You were shot by: ' in response.data)