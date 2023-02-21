from concurrent import futures
import logging

import grpc
import chat_pb2
import chat_pb2_grpc

usernames = {}
inbox = {}

class ChatAppServicer(chat_pb2_grpc.ChatAppServicer):
    def PerformService(self, request, context):
        # Variables to parse the request
        op = request.op
        user1 = request.user1
        user2 = request.user2
        msg = request.msg

        # Final message to be sent to client
        message = ''

        # Create Account
        if op == '1':
            if user1 in usernames:
                message = 'This username is already taken.'
            else:
                usernames[user1] = True
                message = 'Account created!'

        # Log In
        elif op == '2':
            if user1 in usernames:
                usernames[user1] = True
                message = 'You have been logged in. Welcome back!'
                # TODO: Fetch undelivered messages
            else:
                message = 'This username does not exist.'
        
        # List Users
        elif op == '3':
            message = 'Here are the users you can message:'
            for username in list(usernames.keys()):
                message += ('\n' + username)

        # Send Message
        elif op == '4':
            if user2 in usernames:
                if user2 not in inbox:
                    inbox[user2] = []
                inbox[user2].append((user1, msg))
            else:
                message = 'This username does not exist.'
            
        # Log Out
        elif op == '5':
            usernames[user1] = False
            message = 'You have been logged out. See you later!'

        # Delete Account
        elif op == '6':
            del usernames[user1]
            if user1 in inbox: # Undelivered messages are deleted along with the account.
                del inbox[user1]
            message = 'Your account has been deleted. Sorry to see you go!'

        # Listen for Messages
        elif op == '7':
            if user1 not in inbox:
                inbox[user1] = []
            if len(inbox[user1]) > 0:
                message = 'Here are messages you received:'
                for s, m in inbox[user1]:
                    message += ('\n' + s + ': ' + m)
                del inbox[user1]
    
        return chat_pb2.ServerReply(reply=message)

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