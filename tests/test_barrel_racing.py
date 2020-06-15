import os
import unittest
from bs4 import BeautifulSoup
from webtool import app
from shutil import copyfile

class BarrelRacingTestCase(unittest.TestCase):
    
    # Make a copy of the original file to restore from after the tests are finished. 
    def setUp(self):
        copyfile('text/barrel_racing_current_number.txt', 'text/barrel_racing_current_number.txt.orig')
    
    # Replace the modified file with the original. 
    def tearDown(self):
        with open('text/barrel_racing_current_number.txt', 'r') as file:
            original_value = file.read()
        with open('text/barrel_racing_current_number.txt', 'w') as file:
            file.write(original_value)
        os.remove('text/barrel_racing_current_number.txt.orig')
    
    def test_counter_displayed(self):
        tester = app.test_client(self)
        response = tester.get('/barrelracing/counter', content_type='html/text')
        self.assertIn(b'Horse #', response.data)
        with open('text/barrel_racing_current_number.txt', 'r') as file:
            original_value = file.read()
        self.assertIn(original_value, str(response.data))        
    def test_increment(self):
        with app.test_client() as tester:
            response = tester.get('/barrelracing/counter')
            soup = BeautifulSoup(response.data, 'html.parser')
            plus_value = soup.find(id='plushidden')['value']
            response = tester.post('/barrelracing/current_number_update', data=dict(current_number=plus_value), follow_redirects=True)
            self.assertIn(bytes(plus_value, 'ascii'), response.data)
            self.assertIs(200, response.status_code)

    def test_decrement(self):
        with app.test_client() as tester:
            response = tester.get('/barrelracing/counter')
            soup = BeautifulSoup(response.data, 'html.parser')
            minus_value = soup.find(id='minushidden')['value']
            response = tester.post('/barrelracing/current_number_update', data=dict(current_number=minus_value), follow_redirects=True)
            self.assertIn(bytes(minus_value, 'ascii'), response.data)
            self.assertIs(200, response.status_code)
    def test_current_number_file_exists(self):
        self.assertTrue(os.path.isfile('text/barrel_racing_current_number.txt'))
