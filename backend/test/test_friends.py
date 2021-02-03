#!/bin/env python
import pytest

from backend.app import create_app, socketio
from flask_socketio import SocketIO
import json
import unittest
import coverage

cov = coverage.coverage(branch=True)
cov.start()
app = None

with open(
        '../config.json', 'r') as config_file:
    config = json.loads(config_file.read())
    app = create_app(configs=[config['COMMON'], config['TEST']])
    disconnected = None


class UnitTest(unittest.TestCase):
    user_info1 = {
        'nickname': 'nickname1',
        'email': 'login1@emal.com',
        'username': 'login1',
        'password': 'password1'
    }
    user_login1 = {
        'email': 'login1@emal.com',
        'password': 'password1'
    }
    user_info2 = {
        'nickname': 'nickname2',
        'email': 'login2@emal.com',
        'username': 'login2',
        'password': 'password2'
    }
    user_login2 = {
        'email': 'login2@emal.com',
        'password': 'password2'
    }

    @classmethod
    def setUpClass(cls):
        # given
        client = app.test_client()
        client.post('/auth/signup', json=UnitTest.user_info1)
        client.post('/auth/signup', json=UnitTest.user_info2)

    @classmethod
    def tearDownClass(cls):
        app.db.drop_collection('users')
        # app.db.drop_collection('friends')

    def test_login(self):
        # given
        client1 = app.test_client()
        client2 = app.test_client()
        client1.post('/auth/signup', json=UnitTest.user_info1)
        client2.post('/auth/signup', json=UnitTest.user_info2)
        # when
        response1 = client1.post('/auth/login', json=UnitTest.user_login1)
        response2 = client1.post('/auth/login', json=UnitTest.user_login2)
        # then
        status_code1 = response1.__dict__['_status_code']
        status_code2 = response2.__dict__['_status_code']
        self.assertEqual(200, status_code1)
        self.assertEqual(200, status_code2)

    def test_find_friends(self):
        # given
        client = app.test_client()
        client.post('/auth/login', json=UnitTest.user_login1)

        # when
        response = client.get('/friends')
        status_code = response.__dict__['_status_code']
        self.assertEqual(200, status_code)

    def test_find_friend(self):
        # given
        client = app.test_client()
        response = client.post('/auth/login', json=UnitTest.user_login1)

        # when
        client_info = response.get_json()

        print(client_info)
        response = client.get('/friends/login2')
        print(response.get_json())
        status_code = response.__dict__['_status_code']
        self.assertEqual(200, status_code)

    def test_add_friend(self):
        # given
        client = app.test_client()
        response = client.post('/auth/login', json=UnitTest.user_login1)

        # when
        client_info = response.get_json()['data']
        response = client.post('/friends', json={
            "requester":
                {"username": client_info['username'],
                 "nickname": client_info['nickname']},
            "subject":
                {"username": "login4",
                 "nickname": "custom_friend_login2"}
        })
        response = client.get('/friends')
        friends = response.get_json().get('friends')
        print(friends)
        status_code = response.__dict__['_status_code']
        self.assertEqual(200, status_code)

    def test_add_oneself(self):
        # given
        client = app.test_client()
        response = client.post('/auth/login', json=UnitTest.user_login1)

        # when
        client_info = response.get_json()['data']
        response = client.post('/friends', json={
            "requester":
                {"username": client_info['username'],
                 "nickname": client_info['nickname']},
            "subject":
                {"username": client_info['username'],
                 "nickname": "custom_friend_login2"}
        })
        print(response.get_json())
        status_code = response.__dict__['_status_code']
        self.assertNotEqual(200, status_code)

    def test_delete_friend(self):
        # given
        client = app.test_client()
        response = client.post('/auth/login', json=UnitTest.user_login1)
        client_info = response.get_json()['data']
        response = client.post('/friends', json={
            "requester":
                {"username": client_info['username'],
                 "nickname": client_info['nickname']},
            "subject":
                {"username": "login3",
                 "nickname": "custom_friend_login2"}
        })
        # when
        response = client.delete('/friends/login3')
        print(response.get_json())
        status_code = response.__dict__['_status_code']
        self.assertEqual(200, status_code)

    def test_check_recommanded_friends(self):
        # given
        client1 = app.test_client()
        response = client1.post('/auth/login', json=UnitTest.user_login1)

        # when
        client_info = response.get_json()['data']
        response = client1.post('/friends', json={
            "requester":
                {"username": client_info['username'],
                 "nickname": client_info['nickname']},
            "subject":
                {"username": "login2",
                 "nickname": "custom_friend_login2"}
        })
        client2 = app.test_client()
        client2.post('/auth/login', json=UnitTest.user_login2)
        response = client2.get('/friends')
        friends = response.get_json().get('friends')
        print(friends)
        status_code = response.__dict__['_status_code']
        self.assertEqual(200, status_code)

        client2.post('/friends', json={
            "subject":
                {"username": client_info['username'],
                 "nickname": client_info['nickname']},
            "requester":
                {"username": "login2",
                 "nickname": "custom_friend_login2"}
        })

        response = client1.get('/friends')
        friends = response.get_json().get('friends')
        print(friends)
        status_code = response.__dict__['_status_code']
        self.assertEqual(200, status_code)


def run_test():
    unittest.main()


if __name__ == "__main__":
    run_test()
