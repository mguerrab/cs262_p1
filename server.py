from ast import And
import socket
import random

#import thread module
from _thread import *
import threading

p_lock = threading.Lock()

# format is key=username; 
# value is a list where first element is true iff user is online and false iff user is offline; 
# and second element is queue of messages when offline

usernames = {}
messages_idx = 1
online_offline_idx = 0

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
        
        # holds the data the client sent
        data_list = []
        data_list = data_str.split('|')
        
        opcode = data_list[0]
        print('Opcode: ' + str(opcode))

        # opcode '1' represents create account
        if opcode == '1':
            username = str(data_list[1])

            # if username is in dictionary, break
            if username in usernames:
                data = "This username has already been taken. \n"
                print("This username has already been taken. \n")
                break

            # if unique username, add to list of usernames
            usernames[username] = [True, []]
            user_of_current_session = username
            data = "Account has been successfully created with the following username: " + username + "\n"
            print(data)
        # opcode '2' represents list accounts
        elif opcode == '2':
            print("The list of accounts are:\n")
            data = "The list of accounts are:\n"
            accounts = list(usernames.keys())
            for name in accounts:
                print(name + "\n")
                data += name + "\n"
        # opcode '3' represents sending messages to another user
        elif opcode == '3':
            destination_username = str(data_list[1])

            #check if username exists
            if destination_username not in usernames:
                print("Login is unsuccessful. This username does not exist. \n")
                data += "Login is unsuccessful. This username does not exist. \n"
                break
            #append message to list of messages that need to be delivered to user and indicate sender
            message = user_of_current_session + " says: " + str(data_list[2])
            usernames[destination_username][messages_idx].append(message)

            data = "Successful message delivery. If " + destination_username + " is offline, the message will be received once they log back in.\n"
            print(data)
        
        # opcode '4' represents logging in to an existing account, meaning an existing username
        # if username does not exist, it notifies the user and does not create a username
        # format is 4|username
        # if there are messages on the queue for this user that have yet to be delivered, they will be delivered upon successful login
        elif opcode == '4':
            expected_username = str(data_list[1])

            #check if username exists
            if expected_username not in usernames:
                print("This username does not exist. \n")
                break

            #set user of current session
            user_of_current_session = expected_username
            usernames[user_of_current_session][online_offline_idx] = True

        
        # send non-message data
        client_connection.send(data.encode('ascii'))
        # if user is logged on and they have messages on the queue that have not been delivered, deliver the messages
        num_messages = len(usernames[user_of_current_session][messages_idx])
        if (usernames[user_of_current_session][online_offline_idx] and num_messages > 0):
            i = 0
            while i < num_messages:
                client_connection.send(usernames[user_of_current_session][messages_idx].pop(0).encode('ascii'))
                i = i + 1
        

    print("From server.py, the client connection is closed. \n")
    # Log user off and close client connection
    usernames[user_of_current_session][online_offline_idx] = False
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
