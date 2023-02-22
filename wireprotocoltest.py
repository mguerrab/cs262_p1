import unittest
from unittest.mock import patch

import time

import chat_pb2
from client import Client
from server import Server

HOST = 'localhost'
PORT = '5005'

USER1 = 'alice'
USER2 = 'bob'
MSG = 'hello'

class TestServerAndClient(unittest.TestCase):
    server = Server()
    client1 = Client(HOST, PORT)
    client2 = Client(HOST, PORT)

    # Should both be logged out
    def test_01_start(self):
        self.assertEqual(self.client1.loggedIn, False)
        self.assertEqual(self.client2.loggedIn, False)

    # Create USER1 (should succeed)
    def test_02_create_account(self):
        request = server.ServerRequest(op='1', user1 = USER1, user2 = None, msg = None)
        reply = self.server.PerformService(request, None)
        self.assertEqual(reply.reply, 'Account created!')
        self.assertEqual(reply.success, True)

    # Create USER1 again (should fail)
    def test_03_create_account_again(self):
        request = server.ServerRequest(op='1', user1 = USER1, user2 = None, msg = None)
        reply = self.server.PerformService(request, None)
        self.assertEqual(reply.reply, 'This username is already taken.')
        self.assertEqual(reply.success, False)

    # Create USER2 (should succeed)
    def test_04_create_another_account(self):
        request = server.ServerRequest(op='1', user1 = USER2, user2 = None, msg = None)
        reply = self.server.PerformService(request, None)
        self.assertEqual(reply.reply, 'Account created!')
        self.assertEqual(reply.success, True)

    # List users (should succeed)
    def test_05_list_accounts(self):
        request = server.ServerRequest(op='2', user1 = USER1, user2 = None, msg = None)
        reply = self.server.PerformService(request, None)
        self.assertEqual(reply.reply, 'the users are:\n' + USER1 + '\n' + USER2)
        self.assertEqual(reply.success, True)

    # Send message (should succeed)
    def test_06_send_message(self):
        request = server.ServerRequest(op='3', user1 = USER1, user2 = USER2, msg = MSG)
        reply = self.server.PerformService(request, None)
        self.assertEqual(reply.reply, '')
        self.assertEqual(reply.success, True)

    # Log out USER1 (should succeed)
    def test_08_log_out(self):
        request = server.ServerRequest(op='6', user1 = USER1, user2 = None, msg = None)
        reply = self.server.PerformService(request, None)
        self.assertEqual(reply.reply, 'You have been logged out. See you later!')
        self.assertEqual(reply.success, True)

    # Delete Account USER2 (should succeed)
    def test_09_delete_account(self):
        request = server.ServerRequest(op='5', user1 = USER2, user2 = None, msg = None)
        reply = self.server.PerformService(request, None)
        self.assertEqual(reply.reply, 'Your account has been deleted. Sorry to see you go!')
        self.assertEqual(reply.success, True)

if __name__ == '__main__':
    unittest.main()
