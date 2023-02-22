import socket
from _thread import *
import threading


p_lock = threading.Lock()

  
usernames = {} # master data structure where key is the username and value is list where index 0 of list is online/offline status, index 1 of list is messages that are queued and index 2 of their client connection 
online_offline_idx = 0 # index inside list of master data structure
messages_idx = 1 # index inside list of master data structure
client_connection_idx = 2 # index inside list of master data structure 

HOST='0.0.0.0'
PORT=6000
ADDR=(HOST,PORT)

# deals with each client connection
def threaded(client_connection):
    # tracks if which user is currently signed on
    user_of_current_session = ''
    while True:
        # data received from client and is then used ot send data back to the client
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

        # opcode '1' creates account by supplying a unique username.
        # format is: 1|username
        if opcode == '1':
            if (len(data_list) != 2):
                data = "You have not entered a successful operation. To send messages, the format is 1|desired_username. Do not type the '|' character as part of your username as this is used for parsing."
                print(data)
            
            username = str(data_list[1])

            # if username already exists, do not create account
            if username in usernames:
                data = "Unsuccessful. This username has already been taken. Choose a different username to create an account. \n"
                print(data)
                # send notification to client
                client_connection.send(data.encode('ascii'))
                continue

            # if unique username, add account to master data structure
            usernames[username] = [True, [], client_connection]
            # update user of current session to be the newly created account
            user_of_current_session = username

            # notification that will be sent to client
            data = "Account has been successfully created with the following username: " + username + "\n"
            print(data)

        # opcode '2' represents list accounts
        # format is: 2
        elif opcode == '2':
            data = "The list of accounts are:\n"
            print(data)
            
            # iterate through usernames of master data structure
            accounts = list(usernames.keys())
            for name in accounts:
                print(name + "\n")
                data += name + "\n"

        # opcode '3' represents sending messages to another user. User must be logged in to send messages.
        # format is: 3|destination_username|message
        elif opcode == '3':
            if (len(data_list) != 3):
                data = "You have not entered a successful operation. To send messages, the format is 3|recipient_username|message. Do not type the '|' character in your message as this is used for parsing."
                print(data)
            
            destination_username = str(data_list[1])

            #check if username exists
            if destination_username not in usernames:
                data = "Message has not been sent. This username does not exist. \n"
                print(data)
                # send non-message data
                client_connection.send(data.encode('ascii'))
                continue

            # user must be signed into a valid account in order to send a message.
            if user_of_current_session not in usernames:
                data = "Unsuccessful. You are currently not signed into an account and so you can not send messages to an account.\n"
                print(data)
                client_connection.send(data.encode('ascii'))
                continue

            # append sender to the message so recipient knows who the sender was
            message = user_of_current_session + " says: " + str(data_list[2])
            
            #if recipient message is online, send message right away
            if (usernames[destination_username][online_offline_idx]):
                # sends message
                usernames[destination_username][client_connection_idx].send(message.encode('ascii'))
                # notify sender
                data = "Successful message delivery." + destination_username + " is currently online, and they have received the message.\n"
                print(data)
                client_connection.send(data.encode('ascii'))
                continue
            
            # recipient is offline -> append message to list of messages that need to be delivered to user 
            usernames[destination_username][messages_idx].append(message)
            
            # notify sender
            data = "Successful message delivery." + destination_username + " is offline, they will receive the message once they log back in.\n"
            print(data)
        
        # opcode '4' represents logging in to an existing account
        # format is 4|username
        # if there are messages on the queue for this user that have yet to be delivered, they will be delivered upon successful login
        elif opcode == '4':
            
            if (len(data_list) != 2):
                data = "You have not entered a successful operation. To send messages, the format is 4|username."
                print(data)
            
            expected_username = str(data_list[1])

            #check if username exists
            if expected_username not in usernames:
                data = "Unsuccessful. You have not logged into the account of " + expected_username + " since this username does not exist. \n"
                print(data)

            # user can not be previously logged into another account when logging in. They must log out their previous account before logging in.
            elif user_of_current_session in usernames:
                data = "You must log out your current account before logging into another account.\n"
                print(data)
            
            else:
                #sets user of current session
                user_of_current_session = expected_username
                usernames[user_of_current_session][online_offline_idx] = True
                usernames[user_of_current_session][client_connection_idx] = client_connection
                data = "You have successfully logged into the account of " + user_of_current_session + "\n"
                print(data)

                # if user is logged on and they have messages on the queue that have not been delivered, deliver messages immediately
                num_messages = len(usernames[user_of_current_session][messages_idx])
                if (num_messages > 0):
                    i = 0
                    while i < num_messages:
                        client_connection.send(usernames[user_of_current_session][messages_idx].pop(0).encode('ascii'))
                        i = i + 1
        
        # opcode '5' deletes current account user is signed into.
        # format is: '5'
        elif opcode == '5':
            # user must be signed into a valid account
            if user_of_current_session not in usernames:
                data = "Unsuccessful. You are currently not signed into an account and so you can not delete an account.\n"
                print(data)
            else:
                # deletes entry of user from master table
                del usernames[user_of_current_session]
                # sets user of current session to be empty
                user_of_current_session = ''

                # notification
                data = "Your account has been successfully deleted."
                print(data)
                client_connection.send(data.encode('ascii'))
                client_connection.close()
                exit()

        # opcode '6' logs out of the current account user is signed into.
        # format is: '6'
        elif opcode == '6':
            # user must be signed into a valid account
            if user_of_current_session not in usernames:
                data = "Unsuccessful. You are currently not signed into an account and so you can not log out an account."
                print(data)
            else:
                # Updates entry of user from master table to be offline
                usernames[user_of_current_session][online_offline_idx] = False
                # Updates entry of user from master table to not have client connection
                usernames[user_of_current_session][client_connection_idx] = None
                # sets user of current session to be empty
                user_of_current_session = ''

                # notification
                data = "You have been successfully logged out."
                print(data)
                client_connection.send(data.encode('ascii'))
                client_connection.close()
                exit()
        else:
            data = "You have not entered a successful operation. Please try again"
            print(data)
                    
        # send non-message data
        client_connection.send(data.encode('ascii'))
    client_connection.close()
    print("From server.py, the client connection is closed. \n")

class Server:
    def run(self, addr):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.bind(ADDR)
        # s.bind((socket.gethostname(), PORT))

        print("socket binded to port", PORT)

        # can specify the nunumber of unaccepted connections that the system will allow before refusing new connections
        s.listen(3)

        # a forever loop until client wants to exit
        while True:

            # establish connection with client
            client_connection, addr = s.accept()

            print("Connected to :", addr[0], ":", addr[1])

            start_new_thread(threaded, (client_connection,))

if __name__ == "__main__":
    server = Server()
    server.run(ADDR)
