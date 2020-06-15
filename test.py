import unittest
import imaplib
from secrets import token_urlsafe
from bs4 import BeautifulSoup
from webtool import app
from SensitiveData import PROJECT_PASSWORD

class FlaskTestCase(unittest.TestCase):
    
    def test_welcome_page(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Welcome to jforseth.tech" in response.data)

    def test_instructions_page(self):
        tester = app.test_client(self)
        response = tester.get('/instructions', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Contents" in response.data)

    def test_prayer_requests_page(self):
        tester = app.test_client(self)
        response = tester.get('/prayer', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Request Prayer" in response.data)

    def test_videos_page(self):
        tester = app.test_client(self)
        response = tester.get('/videos', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"YouTube" in response.data)

    def test_messenger_page(self):
        tester = app.test_client(self)
        response = tester.get('/messenger', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Clear" in response.data)

    def test_luckyshoe(self):
        tester = app.test_client(self)
        response = tester.get('/luckyshoe', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Lucky Shoe Welding" in response.data)

    def test_todo_no_login(self):
        tester = app.test_client(self)
        response = tester.get(
            '/todo', content_type='html/text', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        response = tester.get(
            '/todo', content_type='html/text', follow_redirects=True)
        self.assertTrue(
            b"You need to sign in to use this feature." in response.data)

    def test_writer_no_login(self):
        tester = app.test_client(self)
        response = tester.get(
            '/writer', content_type='html/text', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        response = tester.get(
            '/writer', content_type='html/text', follow_redirects=True)
        self.assertTrue(
            b"You need to sign in to use this feature." in response.data)

    def test_account_no_login(self):
        tester = app.test_client(self)
        response = tester.get('/account/testing',
                              content_type='html/text', follow_redirects=False)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(b"Oops" in response.data)

    def test_file_sharing_page(self):
        tester = app.test_client(self)
        response = tester.get('/filesharing', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            b"Uploaded files (Available until midnight tonight):" in response.data)

    def test_login_page(self):
        tester = app.test_client(self)
        response = tester.get('/login/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Username" in response.data)
        self.assertTrue(b"Password" in response.data)
        self.assertTrue(b"Forgot Password" in response.data)

    def test_login(self):
        #tester = app.test_client(self)
        with app.test_client() as tester:
            response = tester.get('/login/')
            soup = BeautifulSoup(response.data, 'html.parser')
            token = soup.find(id='csrf_token')['value']
            response = tester.post('/login', data=dict(csrf_token=token, username='testing', password=PROJECT_PASSWORD, next='/'), follow_redirects=True)
            self.assertIn(b"Login Successful", response.data)
    def test_signup_page(self):
        tester = app.test_client(self)
        response = tester.get('/signup', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Recovery Email" in response.data)

    def test_chat_submission(self):
        tester = app.test_client(self)
        response = tester.post('/messenger/result', data={'Data':'Hi'},
                               content_type='html/text', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"<li class='message'> Hi </li>" in response.data)

    def test_chat_deletion(self):
        tester = app.test_client(self)
        response = tester.post(
            '/messenger/clear', content_type='html/text', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"<li class='message'> Hi </li>" not in response.data)

    def test_prayer_request_submission(self):
        tester = app.test_client(self)
        response = tester.post('/prayer/prayerrequest', data=dict(name="Testing: {}".format(token_urlsafe(16)), parish="Testing",
                                                                  prequest="This message should only go to the testing email. Sorry if it doesn't!"), content_type='html/text', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Prayer request sent!' in response.data)
        imap = imaplib.IMAP4_SSL('jforseth.tech')
        imap.login('testing',PROJECT_PASSWORD)
        _ , data = imap.search(None, 'ALL')
        print(data)
        imap.close()
"""
def login(driver, username='testing', password=PROJECT_PASSWORD):
    username_elem = driver.find_element_by_id('username')
    username_elem.send_keys(username)
    password_elem = driver.find_element_by_id('password')
    password_elem.send_keys(password)
    password_elem.send_keys(Keys.RETURN)

class LiveServer(LiveServerTestCase):
    def create_app(self):
        app.config['TESTING'] = True

        # Set to 0 to have the OS pick the port.
        app.config['LIVESERVER_PORT'] = 0

        return app
    # def setUp(self):
    #    self.driver = webdriver.Firefox()
    #    self.driver.get(self.get_server_url())

    # def tearDown(self):
    #    self.driver.quit()

    def test_correct_login(self):
        driver = webdriver.Firefox()
        driver.get(self.get_server_url()+"/login")
        login(driver)
        time.sleep(2)
        self.assertTrue('Successful' in driver.page_source)
        driver.close()

    def test_incorrect_username_login(self):
        driver = webdriver.Firefox()
        driver.get(self.get_server_url()+"/login")
        username = driver.find_element_by_id('username')
        username.send_keys('thisuserdoesnotexist')
        password = driver.find_element_by_id('password')
        password.send_keys(PROJECT_PASSWORD)
        password.send_keys(Keys.RETURN)
        time.sleep(2)
        self.assertTrue('Account not found' in driver.page_source)
        driver.close()

    def test_incorrect_password_login(self):
        driver = webdriver.Firefox()
        driver.get(self.get_server_url()+"/login")
        username = driver.find_element_by_id('username')
        username.send_keys('testing')
        password = driver.find_element_by_id('password')
        password.send_keys('THISISTHEWRONGPASSWORD')
        password.send_keys(Keys.RETURN)
        time.sleep(2)
        self.assertTrue('Incorrect password' in driver.page_source)
        driver.close()

    def test_writer_logged_in(self):
        driver = webdriver.Firefox()
        driver.get(self.get_server_url()+'/writer')
        login(driver)
        time.sleep(2)
        self.assertTrue('newbutton' in driver.page_source)
        driver.close()

    def test_account_page_logged_in(self):
        driver = webdriver.Firefox()
        driver.get(self.get_server_url()+'/login')
        login(driver)
        time.sleep(2)
        driver.get(self.get_server_url()+'/account/testing')
        time.sleep(2)
        self.assertTrue('Unsubscribe' in driver.page_source)
        driver.close()

    def test_videos_logged_in(self):
        driver = webdriver.Firefox()
        driver.get(self.get_server_url()+'/login')
        login(driver)
        time.sleep(2)
        driver.get(self.get_server_url()+'/videos')
        time.sleep(2)
        self.assertTrue('YouTube Link' not in driver.page_source)
        driver.close()

    def test_videos_logged_in_admin(self):
        driver = webdriver.Firefox()
        driver.get(self.get_server_url()+'/login')
        login(driver, username='bookboy210')
        time.sleep(2)
        driver.get(self.get_server_url()+'/videos')
        time.sleep(2)
        self.assertTrue('YouTube Link' in driver.page_source)
        driver.close()

    def test_todo_logged_in(self):
        driver = webdriver.Firefox()
        driver.get(self.get_server_url()+'/todo')
        login(driver)
        time.sleep(2)
        self.assertTrue('testing\'s Todo List' in driver.page_source)
        driver.close()

    def test_account_logged_in(self):
        driver = webdriver.Firefox()
        driver.get(self.get_server_url()+'/login')
        login(driver)
        time.sleep(2)
        driver.get(self.get_server_url()+'/account/testing')
        time.sleep(2)
        self.assertTrue('Unsubscribe' in driver.page_source)
        driver.close()

"""
if __name__ == '__main__':
    unittest.main()
