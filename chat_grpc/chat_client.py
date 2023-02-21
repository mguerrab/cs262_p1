from __future__ import print_function
from _thread import start_new_thread

import logging
import time

import grpc
import chat_pb2
import chat_pb2_grpc

host = 'localhost'
port = '50051'

class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.username = ''

    def send_request(self, op, user2=None, msg=None):
        with grpc.insecure_channel(host + ':' + port) as channel:
            stub = chat_pb2_grpc.ChatAppStub(channel)
            request = chat_pb2.ServerRequest(op=op, user1=self.username, user2=user2, msg=msg)
            reply = stub.PerformService(request)
        if (len(reply.reply) > 0):
            print(reply.reply)
        return reply

    def menu(self):
        while True:
            time.sleep(0.1)
            print('Enter your request: ')
            request = input().split('|')
            op = request[0]

            # Create Account
            if op == '1':
                self.username = request[1]
                self.send_request('1')

            # Log In
            elif op == '2':
                self.username = request[1]
                self.send_request('2')

            # List Users
            elif op == '3':
                self.send_request('3')

            # Send Message
            elif op == '4':
                self.send_request('4', request[1], request[2])

            # Log Out
            elif op == '5':
                self.send_request('5')
                exit()

            # Delete Account
            elif op == '6':
                self.send_request('6')
                exit()
            
            # Invalid
            else: 
                print('Invalid input. Please try again.')

def listen(client):
    while True:
        client.send_request('7')
        time.sleep(0.1)

def run():
    client = ChatClient('localhost', '50051')
    start_new_thread(listen, (client,))
    client.menu()

if __name__ == '__main__':
    logging.basicConfig()
    run()