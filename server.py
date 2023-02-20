from ast import And
from asyncio.windows_events import NULL
from contextlib import nullcontext
import socket
import random

#import thread module
from _thread import *
import threading
from xmlrpc import client

p_lock = threading.Lock()

# format is key=username; 
# value is a list where first element is true iff user is online and false iff user is offline; 
# and second element is queue of messages when offline

usernames = {}
online_offline_idx = 0
messages_idx = 1
client_connection_idx = 2

# thread function
def threaded(client_connection):
    user_of_current_session = ''
    while True:
        # data received from client
        data = client_connection.recv(1024)
        data_str = data.decode('UTF-8')
        if not data:
            print('No data sent. Goodbye!')
            break
        print(data_str + "\n")

        """
        if (user_of_current_session != ''): 
            num_messages = len(usernames[user_of_current_session][messages_idx])
            if (usernames[user_of_current_session][online_offline_idx] and num_messages > 0):
                i = 0
                while i < num_messages:
                    # buggy only sends 1 message at a time
                    client_connection.send(usernames[user_of_current_session][messages_idx].pop(0).encode('ascii'))
                    i = i + 1
        """
        # holds the data the client sent
        data_list = []
        data_list = data_str.split('|')
        
        opcode = data_list[0]
        print('Opcode: ' + str(opcode))

        # opcode '1' creates account by supplying a unique username.
        # format is: 1|username
        if opcode == '1':
            username = str(data_list[1])

            # if username already exists, do not create account
            if username in usernames:
                data = "This username has already been taken. \n"
                print(data)
                # send non-message data
                client_connection.send(data.encode('ascii'))
                break

            # if unique username, add to list of usernames
            usernames[username] = [True, [], client_connection]
            user_of_current_session = username

            # notification
            data = "Account has been successfully created with the following username: " + username + "\n"
            print(data)

        # opcode '2' represents list accounts
        # format is: 2
        elif opcode == '2':
            data = "The list of accounts are:\n"
            print(data)
            
            accounts = list(usernames.keys())
            for name in accounts:
                print(name + "\n")
                data += name + "\n"

        # opcode '3' represents sending messages to another user. User must be logged in to send messages.
        # format is: 3|destination_username|message
        elif opcode == '3':
            destination_username = str(data_list[1])

            #check if username exists
            if destination_username not in usernames:
                data = "Message has not been sent. This username does not exist. \n"
                print(data)
                # send non-message data
                client_connection.send(data.encode('ascii'))
                break

            # user must be signed into a valid account
            if user_of_current_session not in usernames:
                data = "Unsuccessful. You are currently not signed into an account and so you can not send messages to an account.\n"
                print(data)
                client_connection.send(data.encode('ascii'))
                break

            #append sender to the message so recipient knows who the sender was
            message = user_of_current_session + " says: " + str(data_list[2])
            #if recipient message is online, send message right away
            if (usernames[destination_username][online_offline_idx]):
                # sends message
                usernames[destination_username][client_connection_idx].send(message.encode('ascii'))
                # notify sender
                data = "Successful message delivery. If " + destination_username + " is offline, the message will be received once they log back in.\n"
                print(data)
                client_connection.send(data.encode('ascii'))
                break
            
            # recipient is offline -> append message to list of messages that need to be delivered to user 
            usernames[destination_username][messages_idx].append(message)
            
            # notify sender
            data = "Successful message delivery. If " + destination_username + " is offline, the message will be received once they log back in.\n"
            print("the number of messages that need to be delivered is: " + str(len(usernames[destination_username][messages_idx])) + "\n")
            print("these messages are" + str(usernames[destination_username][messages_idx]))
            print(data)
        
        # opcode '4' represents logging in to an existing account, meaning an existing username
        # format is 4|username
        # if username does not exist, it notifies the user and does not create a username
        # if there are messages on the queue for this user that have yet to be delivered, they will be delivered upon successful login
        elif opcode == '4':
            expected_username = str(data_list[1])

            #check if username exists
            if expected_username not in usernames:
                data = "This username does not exist. \n"
                print(data)
                client_connection.send(data.encode('ascii'))
                break

            #sets user of current session
            user_of_current_session = expected_username
            usernames[user_of_current_session][online_offline_idx] = True
            usernames[user_of_current_session][client_connection_idx] = client_connection
            data = "You have successfully logged into the account of " + user_of_current_session + "\n"
            print(data)

            # if user is logged on and they have messages on the queue that have not been delivered, deliver the messages
            print("the number of messages that need to be delivered is: " + str(len(usernames[user_of_current_session][messages_idx])) + "\n")
            ###PROBLEM HERE IS IT WILL ONLY SEND THE FIRST MESSAGE IN THE QUEUE AND NOT THE REST.
            num_messages = len(usernames[user_of_current_session][messages_idx])
            if (usernames[user_of_current_session][online_offline_idx] and num_messages > 0):
                i = 0
                while i < num_messages:
                    # buggy only sends 1 message at a time
                    client_connection.send(usernames[user_of_current_session][messages_idx].pop(0).encode('ascii'))
                    #THIS PRINT STATEMENT IS REACHED
                    print("REACHED LINE AFTER CLIENT_CONNECITON.SEND() and the value of i is " + i + "\n")
                    i = i + 1
        
        # opcode '5' deletes current account user is signed into.
        # format is: '5'
        elif opcode == '5':
            # user must be signed into a valid account
            if user_of_current_session not in usernames:
                data = "Unsuccessful. You are currently not signed into an account and so you can not delete an account.\n"
                print(data)
                client_connection.send(data.encode('ascii'))
                break

            # deletes entry of user from master table
            del usernames[user_of_current_session]
            # sets user of current session to be empty
            user_of_current_session = ''

            # notification
            data = "You have been successfully logged out."
            print(data)

        # opcode '6' logs out of the current account user is signed into.
        # format is: '6'
        elif opcode == '6':
            # user must be signed into a valid account
            if user_of_current_session not in usernames:
                data = "Unsuccessful. You are currently not signed into an account and so you can not log out an account."
                print(data)
                client_connection.send(data.encode('ascii'))
                break

            # Updates entry of user from master table to be offline
            usernames[destination_username][online_offline_idx] = False
            # Updates entry of user from master table to not have client connection
            usernames[destination_username][client_connection_idx] = NULL
            # sets user of current session to be empty
            user_of_current_session = ''

            # notification
            data = "You have been successfully logged out."
            print(data)
            client_connection.send(data.encode('ascii'))
            client_connection.close()
            break
            
        # send non-message data
        client_connection.send(data.encode('ascii'))
        

    print("From server.py, the client connection is closed. \n")
    # Log user off and close client connection
    usernames[user_of_current_session][online_offline_idx] = False
    user_of_current_session = ''
    client_connection.close()
if __name__ == "__main__":
    HOST='172.20.10.2'
    
    PORT=6000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((socket.gethostname(), PORT))

    print("socket binded to port", PORT)

    # can specify the nunumber of unaccepted connections that the system will allow before refusing new connections
    s.listen(3)
    
    # a forever loop until client wants to exit
    while True:

        # establish connection with client
        client_connection, addr = s.accept()

        print("Connected to :", addr[0], ":", addr[1])

        start_new_thread(threaded, (client_connection,))
    
    s.close()


    # put the socket into listening mode
    # server_ex()

    #to enable tcpip through your port, type:
    # sudo ufw allow 2050

