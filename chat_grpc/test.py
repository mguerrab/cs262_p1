import unittest
from unittest.mock import patch

import time

import chat_pb2
from chat_server import ChatAppServicer
from chat_client import ChatClient

HOST = 'localhost'
PORT = '50051'

USER1 = 'alice'
USER2 = 'bob'
MSG = 'hello'

class TestServerAndClient(unittest.TestCase):
    server = ChatAppServicer()
    client1 = ChatClient(HOST, PORT)
    client2 = ChatClient(HOST, PORT)

    # Should both be logged out
    def test_start(self):
        self.assertEqual(self.client1.loggedIn, False)
        self.assertEqual(self.client2.loggedIn, False)

    # Create USER1 (should succeed)
    def test_create_account(self):
        request = chat_pb2.ServerRequest(op='1', user1 = USER1, user2 = None, msg = None)
        reply = self.server.PerformService(request, None)
        self.assertEqual(reply.reply, 'Account created!')
        self.assertEqual(reply.success, True)

    # Create USER1 again (should fail)
    def test_create_account_again(self):
        request = chat_pb2.ServerRequest(op='1', user1 = USER1, user2 = None, msg = None)
        reply = self.server.PerformService(request, None)
        self.assertEqual(reply.reply, 'This username is already taken.')
        self.assertEqual(reply.success, False)

    # Create USER2 (should succeed)
    def test_create_another_account(self):
        request = chat_pb2.ServerRequest(op='1', user1 = USER2, user2 = None, msg = None)
        reply = self.server.PerformService(request, None)
        self.assertEqual(reply.reply, 'Account created!')
        self.assertEqual(reply.success, True)

    # List users (should succeed)
    def test_list_accounts(self):
        request = chat_pb2.ServerRequest(op='3', user1 = USER1, user2 = None, msg = None)
        reply = self.server.PerformService(request, None)
        self.assertEqual(reply.reply, 'Here are the users you can message:\n' + USER1 + '\n' + USER2)
        self.assertEqual(reply.success, True)

    # Send message (should succeed)
    def test_send_message(self):
        request = chat_pb2.ServerRequest(op='4', user1 = USER1, user2 = USER2, msg = MSG)
        reply = self.server.PerformService(request, None)
        self.assertEqual(reply.reply, '')
        self.assertEqual(reply.success, True)

    # Listen for message (should fail) 
    def test_listen_message(self):
        request = chat_pb2.ServerRequest(op='7', user1 = USER1, user2 = None, msg = None)
        reply = self.server.PerformService(request, None)
        self.assertEqual(reply.reply, '')
        self.assertEqual(reply.success, False)

    # Log out USER1 (should succeed)
    def test_log_out(self):
        request = chat_pb2.ServerRequest(op='5', user1 = USER1, user2 = None, msg = None)
        reply = self.server.PerformService(request, None)
        self.assertEqual(reply.reply, 'You have been logged out. See you later!')
        self.assertEqual(reply.success, True)

    # Delete Account USER2 (should succeed)
    def delete_account(self):
        request = chat_pb2.ServerRequest(op='6', user1 = USER2, user2 = None, msg = None)
        reply = self.server.PerformService(request, None)
        self.assertEqual(reply.reply, 'Your account has been deleted. Sorry to see you go!')
        self.assertEqual(reply.success, True)

    # Log in USER1 (should succeed)
    def test_log_in(self):
        request = chat_pb2.ServerRequest(op='2', user1 = USER1, user2 = None, msg = None)
        reply = self.server.PerformService(request, None)
        self.assertEqual(reply.reply, 'You have been logged in. Welcome back!')
        self.assertEqual(reply.success, True)

    def test_log_in_again(self):
        request = chat_pb2.ServerRequest(op='2', user1 = USER2, user2 = None, msg = None)
        reply = self.server.PerformService(request, None)
        self.assertEqual(reply.reply, 'You have been logged in. Welcome back!')
        self.assertEqual(reply.success, True)

if __name__ == '__main__':
    unittest.main()