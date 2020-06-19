import unittest
import os
from test_accounts import login, signup
from account_management import grant_access, get_current_access, get_account
from shutil import move, copyfile,rmtree, copytree, move
from webtool import app
import time
class VideoTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        copyfile(
            "text/videos.txt",
            "text/videos.txt.orig",
        )
        copyfile("database.db", "database.db.orig")
        copytree('userdata/','tests/userdata/')
        signup(app.test_client())
        grant_access('testing', 'admin')
    def tearDown(self):
        pass
    @classmethod
    def tearDownClass(cls):
        os.remove("text/videos.txt")
        move(
            "text/videos.txt.orig",
            "text/videos.txt",
        )
        os.remove("database.db")
        move("database.db.orig", "database.db")
        rmtree('userdata/')
        move('tests/userdata/', 'userdata/')

    def test_videos_logged_out(self):
        tester = app.test_client()
        response = tester.get('/videos')
        self.assertIs(200, response.status_code)
        with open('text/videos.txt') as file:
            videos = file.readlines()
        videos = [video.split('|')[0] for video in videos]
        for video in videos:
            self.assertIn(video, str(response.data))

    def test_videos_as_admin(self):
        with app.test_client() as tester:
            login(tester)
            response = tester.get('/videos')
            self.assertIs(200, response.status_code)
            with open('text/videos.txt') as file:
                videos = file.readlines()
            videos = [video.split('|')[0] for video in videos]
            for video in videos:
                self.assertIn(video, str(response.data))
            self.assertIn(b'YouTube Link',response.data)

    def test_upload_video(self):
        with app.test_client() as tester:
            login(tester)
            response = tester.post('/videos/newupload',data=dict(title="Great Video", youtube_id="https://youtu.be/DLzxrzFCyOs"), follow_redirects=True)
            self.assertIs(200, response.status_code)
            self.assertIn(b'Great Video', response.data)