import unittest
import random
from secrets import token_urlsafe
from bs4 import BeautifulSoup
from snapshot import backuptree, restoretree
from test_accounts import login, signup
from webtool import app


def add_todo(tester, todo_name):
    response = tester.post("/todo/submitted", data=dict(taskname=todo_name))
    return response


def find_index(todos, todo):
    for idx, current_todo in enumerate(todos):
        if todo in current_todo:
            taskid = idx + 1
    return taskid


class TodoTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        backuptree("userdata/")
        tester = app.test_client()
        signup(tester)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        restoretree("userdata/")

    def test_todo_not_logged_in(self):
        tester = app.test_client()
        response = tester.get("/todo")
        self.assertEqual(302, response.status_code)

    def test_todo_logged_in(self):
        with app.test_client() as tester:
            login(tester)
            response = tester.get("/todo")
        self.assertEqual(200, response.status_code)
        self.assertTrue(b"testing's Todo List" in response.data)

    def test_todo_submission(self):
        with app.test_client() as tester:
            taskname = token_urlsafe(10)
            login(tester)
            response = add_todo(tester, taskname)
            self.assertEqual(302, response.status_code)
            response = tester.get("/todo")
            self.assertEqual(200, response.status_code)
            self.assertTrue(taskname, str(response.data))

    def test_todo_deletion(self):
        with app.test_client() as tester:
            taskname = token_urlsafe(10)
            taskid = 0
            login(tester)
            add_todo(tester, taskname)
            with open("userdata/testing/todo/list.csv") as file:
                tasks = file.readlines()
            tasks.reverse()
            taskid = find_index(tasks, taskname)
            response = tester.post("/todo/delete", data=dict(taskid=taskid))
            self.assertEqual(302, response.status_code)
            response = tester.get("/todo")
            self.assertEqual(200, response.status_code)
            self.assertNotIn(taskname, str(response.data))

    def test_todo_relocation(self):
        with app.test_client() as tester:
            taskname = token_urlsafe(10)
            taskid = 0
            login(tester)
            add_todo(tester, taskname)
            #Add some made up tasks
            add_todo(tester, "This is another todo.")
            add_todo(tester, "As is this.")
            add_todo(tester, "As is this.")
            add_todo(tester, "As is this.")
            add_todo(tester, "As is this.")
            with open("userdata/testing/todo/list.csv") as file:
                tasks = file.readlines()
            tasks.reverse()
            taskid = find_index(tasks, taskname)
            new_location = taskid
            while new_location == taskid:
                new_location = random.randint(0, len(tasks) - 1)
            tester.post("/todo/reorder", data=dict(taskid=taskid, taskloc=new_location))
            with open("userdata/testing/todo/list.csv") as file:
                tasks = file.readlines()
            tasks.reverse()
            taskid = find_index(tasks, taskname)
            self.assertEqual(taskid, new_location)


if __name__ == "__main__":
    unittest.main()

