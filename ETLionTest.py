import urllib2
import unittest

from flask import Flask

from ETLionServer import app
from ETLionServer import index, trade, signup, login, logout, app

class ETLionSeresponseerTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config.update(
            TESTING = True,
            TEST_USER_FIRSTNAME = 'test',
            TEST_USER_LASTNAME = 'test',
            TEST_EMAIL = 'itisatest@gmail.com',
            TEST_PASSWORD = 'itisatest',
            EMAIL = 'test@test.com',
            PASSWORD = 'testtest'
        )
        self.tester = self.app.test_client()

    def index(self):
        return self.tester.get('/')
    
    def signup(self, first_name, last_name, email, password):
        return self.tester.post(
            '/signup', 
            data=dict(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            ),
            follow_redirects=True
        )

    def login(self, email, password):
        return self.tester.post(
            '/login',
            data=dict(
                email=email,
                password=password
            ),
            follow_redirects=True
        )

    def logout(self):
        return self.tester.get('/logout', follow_redirects=True)

    def test_index(self):
        response = self.index()
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        self.logout()
        response = self.login(
            self.app.config["EMAIL"],
            self.app.config["PASSWORD"]
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse("Welcome to ETLion Trading System!" in response.data)
        self.assertTrue("Hi, Trader" in response.data)
        self.logout()
        response = self.login(
            self.app.config["EMAIL"] + 'x',
            self.app.config["PASSWORD"] + 'x'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Log in" in response.data)

    def test_logout(self):
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Welcome to ETLion Trading System!" in response.data)
        self.assertFalse("Hi, Trader" in response.data)

if __name__ == "__main__":
    unittest.main()