
import socket

def Main():
    host ='127.0.0.1'
    
    #define port on which to connect
    port = 6000

    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server
    s.connect((socket.gethostname(), port))


    while True:
        ans=input("\nEnter your request:")
        if ans == '':
            ans2 = input("\nDo you want to continue (y/n):")
            if ans2 == 'y' or ans2 == 'yes':
                continue
            else:
                break
        else:
            # send message to server
            s.send(ans.encode('ascii'))
            # receive message from server
            data = s.recv(1024)
            if not data:
                continue
            data_str = data.decode('ascii')
            print("Received from the server: ", str(data_str))
    print("From client.py, the client connection is closed. \n")
    s.close()

if __name__ == "__main__":
    Main()

