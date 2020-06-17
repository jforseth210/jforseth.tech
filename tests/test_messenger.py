import unittest
from shutil import copyfile, move
import os
import time
from webtool import app

class MessengerTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        copyfile('database.db', 'database.db.orig')
    
    def tearDown(self):
        os.remove('database.db')
        move('database.db.orig', 'database.db')

    def test_messenger_page(self):
        tester = app.test_client(self)
        response = tester.get('/messenger', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Clear" in response.data)

    def test_chat_submission(self):
        tester = app.test_client(self)
        response = tester.post('/messenger/result', data=dict(message='Hi'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        #print(response.data)
        self.assertTrue(b"<li class='message'> Hi </li>" in response.data)

    def test_chat_deletion(self):
        tester = app.test_client(self)
        response = tester.post('/messenger/result', data=dict(message='This shouldn\'t show up after the db is cleared.'), follow_redirects=True)
        response = tester.post(
            '/messenger/clear', content_type='html/text', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"<li class='message'>" not in response.data)

if __name__ == "__main__":
    unittest.main()