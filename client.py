#import thread module
from _thread import *
import socket
import time

HOST =localhost
    
#define port on which to connect
PORT = 6000

S=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

logged_out_message = "You have been successfully logged out."
deleted_account_message = "Your account has been successfully deleted."

# Used to disconnect both threads in the client which includes the thread that listens to messages from the server and the thread that sends messages to the server
class DisconnectMessage():
    def __init__(self):
        self.disconnect_message = ''

    def shouldClientClose(self):
        return self.disconnect_message == logged_out_message or self.disconnect_message == deleted_account_message

def Listening_Messages(s, disconnect):
    while True:
        time.sleep(0.1)
        # receive message from server
        data = S.recv(1024)
        if not data:
            continue
        data_str = data.decode('ascii')
        print("Received from the server: ", str(data_str))
        
        # If user logged out or deleted account, this thread should close
        if data_str == logged_out_message:
            disconnect.disconnect_message = data_str
            S.close()
            exit()
        if data_str == deleted_account_message:
            disconnect.disconnect_message = data_str
            S.close()
            exit()
    

def Run(S):
    disconnect = DisconnectMessage()
    # connect to server
    S.connect((HOST, HOST))

    start_new_thread(Listening_Messages, (S,disconnect))

    while True:
        time.sleep(0.1)
        # If user logged out or deleted account, this thread should close
        if disconnect.shouldClientClose():
            S.close()
            exit()

        ans=input("\nEnter your request:")

        # If user logged out or deleted account, this thread should close
        if disconnect.shouldClientClose():
            S.close()
            exit()
        # send message to server
        S.send(ans.encode('ascii'))

def Main():
    Run(S)


if __name__ == "__main__":
    Main()

