from concurrent import futures
import logging

# Imports for gRPC
import grpc
import chat_pb2
import chat_pb2_grpc

# Dictionary mapping existing usernames to their status (online or offline)
usernames = {} 
# Dictionary mapping existing usernames to a list of undelivered messages, represented as (sender, message)
inbox = {}

# The ChatAppServicer class as specified by the .proto
class ChatAppServicer(chat_pb2_grpc.ChatAppServicer):
    def PerformService(self, request, context):
        # Variables to parse the request
        op = request.op
        user1 = request.user1
        user2 = request.user2
        msg = request.msg

        # Final message to be sent to client
        message = ''
        # Final success value assumed to be positive
        success = True

        # Create Account
        if op == '1':
            if user1 in usernames: # If username is already taken
                message = 'This username is already taken.'
                success = False # Negative success value returned
            else: # Otherwise, username is valid
                usernames[user1] = True
                message = 'Account created!'

        # Log In
        elif op == '2':
            if user1 in usernames: # If username exists
                usernames[user1] = True
                message = 'You have been logged in. Welcome back!'
            else: # Otherwise, username is invalid
                message = 'This username does not exist.'
                success = False # Negative success value returned
        
        # List Users
        elif op == '3':
            message = 'Here are the users you can message:'
            for username in list(usernames.keys()): # Iterate through all users
                message += ('\n' + username)

        # Send Message
        elif op == '4':
            if user2 in usernames: # If recipient username exists
                if user2 not in inbox: # If recipient username does not yet have an inbox
                    inbox[user2] = [] # Initialize inbox
                inbox[user2].append((user1, msg)) # Insert message into inbox of recipient
            else: # Otherwise, recipient username is invalid
                message = 'This username does not exist.'
                success = False # Negative success value returned
            
        # Log Out
        elif op == '5':
            usernames[user1] = False # Username now maps to offline value
            message = 'You have been logged out. See you later!'

        # Delete Account
        elif op == '6':
            del usernames[user1] # The mapping from this username is deleted
            if user1 in inbox: # Undelivered messages are deleted along with the account
                del inbox[user1]
            message = 'Your account has been deleted. Sorry to see you go!'

        # Listen for Messages
        elif op == '7':
            if user1 not in inbox: # If username does not yet have an inbox
                inbox[user1] = [] # Initialize inbox

            if len(inbox[user1]) == 0: # If inbox is empty
                success = False # Negative success value returned
            else: # If there are messages in the inbox
                message = 'Here are messages you received:'
                for s, m in inbox[user1]: # Iterate through all undelivered messages
                    message += ('\n' + s + ': ' + m) # Message displayed as "alice: hey bob"
                del inbox[user1] # These messages are now delivered so are removed from inbox

        # Both the reply message and success value are returned
        return chat_pb2.ServerReply(reply=message, success=success) 

# Function to start the server up
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatAppServicer_to_server(ChatAppServicer(), server) # !
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server is up!")
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()