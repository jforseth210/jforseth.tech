import unittest
from snapshot import backup, backuptree, restore, restoretree
import os
import json
from bs4 import BeautifulSoup
import secrets
from webtool import app
from account_management import delete_account, remove_token
from SensitiveData import PROJECT_PASSWORD, TESTING_GROUP_SIGNUP_CODE


USERNAMES = [
    "testing",
    "testing with spaces",
    "'\"",
    '<script>alert("Hi")!</script>',
    "👨‍💻",
]
PASSSWORDS = [
    "a",
    "password",
    "spaces spaces",
    "'\"",
    '<script>alert("Hi")!</script>',
    "👨‍💻👨‍💻👨‍💻👨‍💻",
]


def login(tester, username="testing", password=PROJECT_PASSWORD):
    response = tester.get("/login/")
    soup = BeautifulSoup(response.data, "html.parser")
    token = soup.find(id="csrf_token")["value"]
    response = tester.post(
        "/login",
        data=dict(csrf_token=token, username=username, password=password, next="/"),
        follow_redirects=True,
    )
    return response


def signup(
    tester,
    emailInput="justin@jforseth.tech",
    username="testing",
    password=PROJECT_PASSWORD,
    confirm_password=PROJECT_PASSWORD,
    prayer_user="on",
    parish=TESTING_GROUP_SIGNUP_CODE,
):

    response = tester.post(
        "/signup",
        data=dict(
            emailInput=emailInput,
            usernameInput=username,
            passwordInput=password,
            confirmPasswordInput=confirm_password,
            prayerInput=prayer_user,
            parishInput=parish,
        ),
        follow_redirects=True,
    )
    if b"Account exists already" in response.data:
        delete_account("testing")
        response = tester.post(
            "/signup",
            data=dict(
                emailInput=emailInput,
                usernameInput=username,
                passwordInput=password,
                confirmPasswordInput=confirm_password,
                prayerInput=prayer_user,
                parishInput=parish,
            ),
            follow_redirects=True,
        )
    return response


# def delete_account(tester, confirm_password=PROJECT_PASSWORD):
#    response = tester.post("/accountdel", data=dict(confirm_password=confirm_password))
#    return response


class AccountsTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        backup("database.db")
        backuptree("userdata/")

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True

    def tearDown(self):
        restore("database.db")
        restoretree("userdata/")

    @classmethod
    def tearDownClass(cls):
        pass


    def test_login_page(self):
        tester = app.test_client(self)
        response = tester.get("/login/", content_type="html/text")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Username" in response.data)
        self.assertTrue(b"Password" in response.data)
        self.assertTrue(b"Forgot Password" in response.data)

    def test_correct_login(self):
        with app.test_client() as tester:
            signup(tester)
            response = login(tester)
            self.assertTrue(b"Login Successful" in response.data)
            self.assertEqual(response.status_code, 200)

    def test_correct_login_no_csrf(self):
        with app.test_client() as tester:
            response = tester.get("/login/")
            response = tester.post(
                "/login",
                data=dict(username="testing", password=PROJECT_PASSWORD, next="/"),
                follow_redirects=True,
            )
            self.assertTrue(b"token is missing" in response.data)
            self.assertEqual(response.status_code, 200)

    def test_incorrect_username(self):
        with app.test_client() as tester:
            response = tester.get("/login/")
            soup = BeautifulSoup(response.data, "html.parser")
            token = soup.find(id="csrf_token")["value"]
            response = tester.post(
                "/login",
                data=dict(
                    csrf_token=token,
                    username="thisuserdoesnotexist",
                    password=PROJECT_PASSWORD,
                    next="/",
                ),
                follow_redirects=True,
            )
            self.assertTrue(b"Account not found" in response.data)
            self.assertEqual(response.status_code, 401)

    def test_incorrect_password(self):
        with app.test_client() as tester:
            signup(tester)
            response = tester.get("/login/")
            soup = BeautifulSoup(response.data, "html.parser")
            token = soup.find(id="csrf_token")["value"]
            response = tester.post(
                "/login",
                data=dict(
                    csrf_token=token,
                    username="testing",
                    password="this is the wrong password",
                    next="/",
                ),
                follow_redirects=True,
            )
            self.assertTrue(b"Incorrect password" in response.data)
            self.assertEqual(response.status_code, 401)

    def test_account_no_login(self):
        tester = app.test_client(self)
        response = tester.get(
            "/account/testing", content_type="html/text", follow_redirects=False
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(b"Oops" in response.data)

    def test_signup(self):
        with app.test_client() as tester:
            response = signup(tester)
            self.assertEqual(200, response.status_code)

    def test_account_deletion(self):
        with app.test_client() as tester:
            signup(tester)
            login(tester)
            response = tester.post(
                "/accountdel",
                data=dict(confirm_password=PROJECT_PASSWORD, follow_redirects=True),
            )
            self.assertEqual(302, response.status_code)
            self.assertTrue(
                b'<p>You should be redirected automatically to target URL: <a href="/logout">/logout</a>',
                response.data,
            )

    def test_password_change_correctly(self):
        with app.test_client() as tester:
            signup(tester)
            login(tester)
            new_password = secrets.token_urlsafe(10)
            response = tester.post(
                "/changepw",
                data=dict(
                    old_password=PROJECT_PASSWORD,
                    new_password=new_password,
                    confirm_new_password=new_password,
                ),
                follow_redirects=True,
            )
            self.assertTrue(b"Success!" in response.data)
        with app.test_client() as tester:
            login(tester, password=new_password)

    def test_password_change_incorrect_old_pw(self):
        with app.test_client() as tester:
            signup(tester)
            login(tester)
            new_password = secrets.token_urlsafe(10)
            response = tester.post(
                "/changepw",
                data=dict(
                    old_password="THIS IS THE INCORRECT OLD PASSWORD!",
                    new_password=new_password,
                    confirm_new_password=new_password,
                ),
                follow_redirects=True,
            )
            self.assertTrue(b"Old password incorrect." in response.data)
        with app.test_client() as tester:
            response = login(tester, password=new_password)
            self.assertTrue(b"Incorrect password." in response.data)

    def test_password_change_missmatched_pws(self):
        with app.test_client() as tester:
            signup(tester)
            login(tester)
            new_password = secrets.token_urlsafe(10)
            response = tester.post(
                "/changepw",
                data=dict(
                    old_password=PROJECT_PASSWORD,
                    new_password=new_password,
                    confirm_new_password="THIS IS A DIFFERENT NEW PASSWORD!",
                ),
                follow_redirects=True,
            )
            self.assertTrue(b"New passwords do not match!" in response.data)
        with app.test_client() as tester:
            response = login(tester, password=new_password)
            self.assertTrue(b"Incorrect password." in response.data)

    def test_change_recovery_email(self):
        with app.test_client() as tester:
            signup(tester)
            login(tester)
            response = tester.post(
                "/change_email",
                data=dict(email="testing@jforseth.tech", email_type="Recovery email"),
            )
            username, email, email_type, token = json.loads(response.data)
            response = tester.get(
                "/change_email/verified",
                query_string=dict(
                    username=username, email=email, type=email_type, token=token
                ),
                follow_redirects=True,
            )
            self.assertTrue(b"Success!" in response.data)
            self.assertEqual(200, response.status_code)


if __name__ == "__main__":
    unittest.main()
