#!/bin/env python
from datetime import datetime

import pytest

from backend.app import create_app, socketio
from flask_socketio import SocketIO
import json
import unittest
import coverage

cov = coverage.coverage(branch=True)
cov.start()
app = None

with open("../config.json", "r") as config_file:
    config = json.loads(config_file.read())
    app = create_app(configs=[config["COMMON"], config["TEST"]])
    disconnected = None


class UnitTest(unittest.TestCase):
    client1 = None
    client2 = None
    user_info1 = {
        "nickname": "nickname1",
        "email": "login1@emal.com",
        "username": "login1",
        "password": "password1"
    }
    user_login1 = {
        "email": "login1@emal.com",
        "password": "password1"
    }
    user_info2 = {
        "nickname": "nickname2",
        "email": "login2@emal.com",
        "username": "login2",
        "password": "password2"
    }
    user_login2 = {
        "email": "login2@emal.com",
        "password": "password2"
    }

    def setUp(self):
        # given
        UnitTest.client1 = app.test_client()
        UnitTest.client2 = app.test_client()
        UnitTest.client1.post("/auth/signup", json=UnitTest.user_info1)
        UnitTest.client2.post("/auth/signup", json=UnitTest.user_info2)
        UnitTest.client1.post("/auth/login", json=UnitTest.user_login1)
        UnitTest.client2.post("/auth/login", json=UnitTest.user_login2)
        UnitTest.client1.post("/friends", json={
            "requester":
                {"username": "login1",
                 "nickname": "nickname1"},
            "subject":
                {"username": "login2",
                 "nickname": "nickname2"}
        })

    def tearDown(self):
        app.db.drop_collection("users")
        app.db.drop_collection("friends")
        app.db.drop_collection("rooms")
        app.db.drop_collection("msgs")

    def test_check_rooms(self):
        response = UnitTest.client1.get("/chats")
        self.assertEqual(200, response.__dict__["_status_code"])

    def test_socket(self):
        client1 = socketio.test_client(app=app, flask_test_client=UnitTest.client1)
        client2 = socketio.test_client(app=app, flask_test_client=UnitTest.client2)
        self.assertTrue(client1.is_connected())
        self.assertTrue(client2.is_connected())
        self.assertNotEqual(client1.sid, client2.sid)
        print(client1.get_received())

    def test_create_room(self):
        response = UnitTest.client1.post("/chats", json={
            "title": "title",
            "members": [
                {"username": "login1", "nickname": "nickname1"},
                {"username": "login2", "nickname": "nickname2"}
            ]
        })
        self.assertEqual(200, response.__dict__["_status_code"])

    def test_create_delete_room(self):
        response = UnitTest.client1.post("/chats", json={
            "title": "title",
            "members": [
                {"username": "login1", "nickname": "nickname1"},
                {"username": "login2", "nickname": "nickname2"}
            ]
        })
        room_id = response.get_json()['data']['_id']

        response = UnitTest.client1.delete('/chats/' + room_id)
        self.assertEqual(200, response.__dict__["_status_code"])

    def test_check_room(self):
        # given
        room_info = {
            "title": "title",
            "members": [
                {"username": "login1", "nickname": "nickname1"},
                {"username": "login2", "nickname": "nickname2"}
            ]
        }
        response = UnitTest.client1.post("/chats", json=room_info)
        room_id_from_1 = response.get_json()['data']['_id']

        # when
        response = UnitTest.client2.get('/chats')
        print(response.get_json())
        room_id_from_2 = response.get_json()['data'][0]['_id']

        # then
        self.assertEqual(room_id_from_1, room_id_from_2)

    def test_send_chat(self):
        # given
        room_info = {
            "title": "title",
            "members": [
                {"username": "login1", "nickname": "nickname1"},
                {"username": "login2", "nickname": "nickname2"}
            ]
        }
        response = UnitTest.client1.post("/chats", json=room_info)
        room_id = response.get_json()['data']['_id']

        # when
        socket_1 = socketio.test_client(app=app, flask_test_client=UnitTest.client1)
        self.assertTrue(socket_1.is_connected())
        socket_1.emit('join room', {'room_id': room_id})
        msg = {
            "sender": "login1",
            'room_id': room_id,
            'msg': 'new message',
            'members': list(map(lambda x: x['username'], room_info['members']))
        }
        socket_1.emit('send msg', msg)
        response = socket_1.get_received()

        # then
        received = response[0]['args'][0]['data']
        self.assertNotEqual(msg, received)
        del received['_id']
        del received['timestamp']
        self.assertEqual(msg, received)

    def test_load_chat(self):
        # given
        room_info = {
            "title": "title",
            "members": [
                {"username": "login1", "nickname": "nickname1"},
                {"username": "login2", "nickname": "nickname2"}
            ]
        }
        response = UnitTest.client1.post("/chats", json=room_info)
        room_id = response.get_json()['data']['_id']

        socket_1 = socketio.test_client(app=app, flask_test_client=UnitTest.client1)
        msg = {
            "sender": "login1",
            'room_id': room_id,
            'msg': 'new message',
            'members': list(map(lambda x: x['username'], room_info['members']))
        }
        socket_1.emit('join room', {'room_id': room_id})
        socket_1.emit('send msg', msg)

        socket_2 = socketio.test_client(app=app, flask_test_client=UnitTest.client2)
        load_msg_request = {
            'room_id': room_id,
            'username': 'login2',
            'timestamp': str(datetime.utcnow().timestamp())
        }
        print(load_msg_request)
        socket_2.emit('read msg', load_msg_request)
        response = socket_1.get_received()

        # then
        received = response[0]['args'][0]['data']
        print(received)


if __name__ == "__main__":
    unittest.main()
