from __future__ import print_function
from _thread import start_new_thread

import logging
import time

# Imports for gRPC
import grpc
import chat_pb2
import chat_pb2_grpc

# Host and port for connecting to server
host = 'localhost'
port = '50051'

# Class definition for clients of the chat app
class ChatClient:
    # Class constructor to set default values
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.username = '' # Username defaults to empty
        self.loggedIn = False # loggedIn defaults to false

    # Function to send request to and receive reply from server
    def send_request(self, op, user2=None, msg=None):
        # Send request to server
        with grpc.insecure_channel(host + ':' + port) as channel:
            stub = chat_pb2_grpc.ChatAppStub(channel)
            request = chat_pb2.ServerRequest(op=op, user1=self.username, user2=user2, msg=msg)
            reply = stub.PerformService(request)
        # If there is a reply message, it is printed
        if (len(reply.reply) > 0):
            print(reply.reply)
        # A prompt to enter request unless it is a trivial reply to op 7
        if not (op == '7' and reply.success == False):
            print('Enter your request:')
        return reply # Reply message is also returned

    def menu(self):
        print('Enter your request:') # A prompt to enter request

        while True: # Repeats every 0.1 seconds
            time.sleep(0.1)
            request = input().split('|') # Request is parsed, as demarcated by '|' sign
            op = request[0] # The op code is the first character

            if self.loggedIn and (op in ['1', '2']): # If they try to log in or sign up while already logged in
                print("You are already logged in.") # Error message
            elif (not self.loggedIn) and (op in ['3', '4', '5', '6']): # If they they haven't logged in yet
                print("You must be logged in first.") # Error message
            elif (op in ['1', '2', '3', '4', '5', '6']): # If a valid op code is entered
                # Create Account
                if op == '1':
                    if len(request) == 2: # If syntax is correct
                        self.username = request[1] # Username is set
    
                        if self.send_request('1').success: # If account creation request is successful
                            self.loggedIn = True # They are now logged in
                        else: # If account creation request failed
                            self.username = '' # Username is back to empty
                    else: # If syntax is incorrect
                        print("Invalid syntax. Try 1|[username].") # Error message

                # Log In
                elif op == '2':
                    if len(request) == 2: # If syntax is correct
                        self.username = request[1] # Username is set

                        if self.send_request('2').success: # If log in request is successful
                            self.loggedIn = True # They are now logged in
                        else: # If log in request failed
                            self.username = '' # Username is back to empty
                    else: # If syntax is incorrect
                        print("Invalid syntax. Try 2|[username].") # Error message

                # List Users
                elif op == '3': 
                    self.send_request('3') # Request sent to server

                # Send Message
                elif op == '4':
                    if len(request) == 3: # If syntax is correct
                        self.send_request('4', request[1], request[2]) # Request sent to server
                    else: # If syntax is incorrect
                        print("Invalid syntax. Try 4|[username]|[message].") # Erorr message

                # Log Out
                elif op == '5': 
                    self.send_request('5') # Request sent to server
                    exit() # Exit

                # Delete Account
                elif op == '6':
                    self.send_request('6') # Request sent to server
                    exit() # Exit
            # Invalid
            else: 
                print('Invalid input. Please try again.') # Error message

# Function to constantly listen for incoming messages
def listen(client): 
    while True: # Repeats every 0.1 seconds
        time.sleep(0.1)
        if client.loggedIn: # If client is logged in
            client.send_request('7') # Listen for incoming messages

# Function to run program
def run():
    client = ChatClient('localhost', '50051') # Instantiate client
    start_new_thread(listen, (client,)) # Start a new thread for listening
    client.menu() # Start the selection menu to solicit request

if __name__ == '__main__':
    logging.basicConfig()
    run()