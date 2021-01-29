#!/bin/env python
import pytest

from app import create_app, socketio
from flask_socketio import SocketIO
import json
import unittest
import coverage

cov = coverage.coverage(branch=True)
cov.start()
app = None

with open('./config.json', 'r') as config_file:
    config = json.loads(config_file.read())
    app = create_app(configs=[config['COMMON'], config['TEST']])
    disconnected = None


class UnitTest(unittest.TestCase):

    def setUp(self):
        pass

    @classmethod
    def tearDownClass(cls):
        print(132123)
        app.db.drop_collection('users')

    def test_get_index(self):
        # given
        client = app.test_client()
        # when
        response = client.get('/')
        # then
        status_code = response.__dict__['_status_code']
        self.assertEqual(200, status_code)

    def test_get_signup(self):
        # given
        client = app.test_client()
        # when
        response = client.get('/auth/signup')
        # then
        status_code = response.__dict__['_status_code']
        self.assertEqual(200, status_code)

    def test_sign_up(self):
        # given
        user_info = {
            'email': 'good@emal.com',
            'username': 'name',
            'password': 'password'
        }
        client = app.test_client()
        # when
        response = client.post('/auth/signup', json=user_info)
        # then
        status_code = response.__dict__['_status_code']
        self.assertEqual(200, status_code)

    def test_sign_up_bad_request(self):
        # given
        user_wrong_schema = {
            'email': 'wrong_schema@emal.com',
            'name': 'wrong_schema',
            'password': 'password'
        }
        client = app.test_client()
        # when
        response = client.post('/auth/signup', json=user_wrong_schema)
        # then
        status_code = response.__dict__['_status_code']
        self.assertEqual(400, status_code)

    def test_sign_up_conflict1(self):
        # given
        user_duplicate_email = {
            'email': 'dup_email@emal.com',
            'username': 'dup_email',
            'password': 'user_dup'
        }
        client1 = app.test_client()
        client2 = app.test_client()
        # when
        response1 = client1.post('/auth/signup', json=user_duplicate_email)
        response2 = client2.post('/auth/signup', json=user_duplicate_email)
        # then
        status_code1 = response1.__dict__['_status_code']
        status_code2 = response2.__dict__['_status_code']
        self.assertEqual(200, status_code1)
        self.assertEqual(409, status_code2)

    def test_sign_up_conflict2(self):
        # given
        user_duplicate_username1 = {
            'email': 'dup_username1@emal.com',
            'username': 'dup_username',
            'password': 'user_dup'
        }
        user_duplicate_username2 = {
            'email': 'dup_username2@emal.com',
            'username': 'dup_username',
            'password': 'user_dup'
        }
        client1 = app.test_client()
        client2 = app.test_client()
        # when
        response1 = client1.post('/auth/signup', json=user_duplicate_username1)
        response2 = client2.post('/auth/signup', json=user_duplicate_username2)
        # then
        status_code1 = response1.__dict__['_status_code']
        status_code2 = response2.__dict__['_status_code']
        self.assertEqual(200, status_code1)
        self.assertEqual(409, status_code2)

    def test_get_login(self):
        # given
        client = app.test_client()
        # when
        response = client.get('/auth/login')
        # then
        status_code = response.__dict__['_status_code']
        self.assertEqual(200, status_code)

    def test_login(self):
        user_info = {
            'email': 'login@emal.com',
            'username': 'login',
            'password': 'password'
        }
        user_login = {
            'email': 'login@emal.com',
            'password': 'password'
        }
        # given
        client = app.test_client()
        client.post('/auth/signup', json=user_info)

        # when
        response = client.post('/auth/login', json=user_login)
        # then
        status_code = response.__dict__['_status_code']
        print(response.get_json())
        self.assertEqual(200, status_code)

    def test_logout(self):
        user_info = {
            'email': 'logout@emal.com',
            'username': 'logout',
            'password': 'password'
        }
        user_login = {
            'email': 'logout@emal.com',
            'password': 'password'
        }
        # given
        client = app.test_client()
        client.post('/auth/signup', json=user_info)
        client.post('/auth/login', json=user_login)
        # when
        response = client.post('/auth/logout')
        # then
        status_code = response.__dict__['_status_code']
        self.assertEqual(200, status_code)

if __name__ == '__main__':
    unittest.main()
