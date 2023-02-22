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


## Running gRPC code
To run the gRPC code, navigate to the grpc folder in the repository. Then, inside of that folder, run the command
``` $ python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./messages.proto ```

This will generate the _pb2_grpc.py and _pb2.py from the messages.proto file. 

Then, from the grpc_server.py, set the host and port to the same thing as in grpc_client.py (if running on one machine) and run the two files using the instructions above replacing server.py with grpc_server.py and same for the client file. If you are running in two machines, follow the instructions above. 
