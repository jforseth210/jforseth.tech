import unittest
from webtool import app


class WebtoolTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True

    def tearDown(self):
        pass

    def test_server_working(self):
        tester = app.test_client()
        response = tester.get("/")
        self.assertIs(200, response.status_code)
        self.assertIn(b"Welcome", response.data)

    def test_404_working(self):
        tester = app.test_client()
        response = tester.get("/thispagedoesnotexist")
        self.assertEqual(404, response.status_code)
        self.assertIn(b"Oops", response.data)


if __name__ == "__main__":
    unittest.main()

"""
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


    def test_file_sharing_page(self):
        tester = app.test_client(self)
        response = tester.get('/filesharing', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            b"Uploaded files (Available until midnight tonight):" in response.data)


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


if __name__ == '__main__':
    unittest.main()
"""
