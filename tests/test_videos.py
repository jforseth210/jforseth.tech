import unittest
import os
import time
import random
import html
from snapshot import backup, backuptree, restore, restoretree
from bs4 import BeautifulSoup
from test_accounts import login, signup
from account_management import grant_access, get_current_access, get_account
from webtool import app


def choose_random_video():
    with open("text/videos.txt") as file:
        videos = file.readlines()
    videos = [video.split("|") for video in videos]
    video = random.choice(videos)
    return video


def choose_middle_video():
    with open("text/videos.txt") as file:
        videos = file.readlines()
    video = videos[round(len(videos) / 2)]
    return video

class VideoTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        backup("text/videos.txt")
        backup("/var/www/jforseth.tech/database.db")
        backuptree("userdata/")
        signup(app.test_client())
        grant_access("testing", "admin")

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        restore("text/videos.txt")
        restore("/var/www/jforseth.tech/database.db")
        restoretree("userdata/")

    def test_videos_logged_out(self):
        tester = app.test_client()
        response = tester.get("/videos")
        self.assertIs(200, response.status_code)
        with open("text/videos.txt") as file:
            videos = file.readlines()
        videos = [video.split("|")[0] for video in videos]
        for video in videos:
            self.assertTrue(video, str(response.data))

    def test_individual_video(self):
        tester = app.test_client()
        video = choose_random_video()[0]
        response = tester.get("/videos/video/{}".format(video))
        self.assertIs(200, response.status_code)
        self.assertTrue(video, str(response.data))

    def test_videos_as_admin(self):
        with app.test_client() as tester:
            login(tester)
            response = tester.get("/videos")
            self.assertIs(200, response.status_code)
            with open("text/videos.txt") as file:
                videos = file.readlines()
            videos = [video.split("|")[0] for video in videos]
            for video in videos:
                self.assertTrue(video, str(response.data))
            #print(BeautifulSoup(response.data,'html.parser').prettify())
            self.assertTrue(b"YouTube Link" in response.data)

    def test_upload_video(self):
        with app.test_client() as tester:
            login(tester)
            response = tester.post(
                "/videos/newupload",
                data=dict(
                    title="Great Video", youtube_id="https://youtu.be/DLzxrzFCyOs"
                ),
                follow_redirects=True,
            )
            self.assertIs(200, response.status_code)
            self.assertTrue(b"Great Video" in response.data)

    def test_delete_video(self):
        with app.test_client() as tester:
            login(tester)
            video = choose_random_video()[1]
            response = tester.post(
                "/videos/deletion", data=dict(youtube_id=video), follow_redirects=True
            )
            self.assertIs(200, response.status_code)
            self.assertNotIn(video, str(response.data))

    def test_bad_deletion(self):
        video = choose_random_video()[1]
        tester = app.test_client()
        response = tester.post(
            "/videos/deletion", data=dict(youtube_id=video), follow_redirects=True
        )
        self.assertTrue("You need to sign in to use this feature.", str(response.data))
        with tester:
            login(tester)
            response = tester.post(
                "/videos/deletion",
                data=dict(youtube_id="Too short"),
                follow_redirects=True,
            )
        self.assertTrue(
            "This doesn't look like a YouTube link. Try again.",
            html.unescape(str(response.data)),
        )

    def test_move_up(self):
        with open("text/videos.txt") as file:
            old_video_order = file.readlines()

        video = choose_middle_video()
        video = "".join(video).strip("\n")
        with app.test_client() as tester:
            login(tester)
            response = tester.post(
                "/videos/move", data=dict(element=video, direction="up")
            )

            with open("text/videos.txt") as file:
                current_video_order = file.readlines()

        old_index = old_video_order.index(video + "\n")
        current_index = current_video_order.index(video + "\n")
        self.assertEqual(old_index - 1, current_index)

    def test_move_down(self):
        with open("text/videos.txt") as file:
            old_video_order = file.readlines()

        video = choose_middle_video()
        video = "".join(video).strip("\n")
        with app.test_client() as tester:
            login(tester)
            response = tester.post(
                "/videos/move", data=dict(element=video, direction="down")
            )

            with open("text/videos.txt") as file:
                current_video_order = file.readlines()

        old_index = old_video_order.index(video + "\n")
        current_index = current_video_order.index(video + "\n")
        self.assertEqual(old_index + 1, current_index)


if __name__ == "__main__":
    unittest.main()
