## Running socket-based chat app

### To run the code of the socket-based chat app on the same machine, 
1. Go to the cs262_p1 folder and edit the server.py file to have global variable HOST set to 'localhost' and global variable PORT set to 6000.
2. Edit client.py to have global variable HOST set to 'localhost' and global variable PORT set to 6000 (needs to be the same value PORT is assigned to in server.py).
3. In one linux-based terminal, start the server by running the following command: ``` $ python3 server.py ```.
4. In a new linux-based terminal, start the client by running the following command: ``` $ python client.py ```
5. For every new client you want to add, repeat step 4.

### Across Machines
1. Go to the cs262_p1 folder and edit the server.py file to have global variable HOST set to '0.0.0.0' and global variable PORT set to 6000.
2. Find the private IP address of the machine the server will be run on. This can be done by going to Settings of the machine and clicking on Wifi/Network properties and look for IPv4 address. Another way to find the IP address is running ```hostname -I``` in a linux based terminal. 
3. Then, edit client.py (also in cs262_p1 folder) to have global variable HOST set to the IP address found in the previous step and global variable PORT set to 6000 (needs to be the same value PORT is assigned to in server.py).
4. In one linux-based terminal, start the server by running the following command: ``` $ python3 server.py ```.
5. In a new linux-based terminal, start the client by running the following command: ``` $ python client.py ```
6. For every new client you want to add, repeat step 5.


### Operation Syntax
The bullets below show how to run the different operations and what they do. The format is: 'command to run in terminal': what this command does

- '1|Username': creates an account with username supplied
- '2': lists usernames of all accounts created
- '3|target_username|message': sends message to target_username
- '4|username': log in to account of username supplied
- '5': delete current account user is logged into
- '6': log out of account user is logged into
