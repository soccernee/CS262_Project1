import client_utils
import datetime
import socket
import string
import config
import wire_protocol
import threading

class Client:
    def __init__(self):
        self.logged_in_user = None
        self.clientsocket = self.create_client_socket()
        
        self.open_thread()
        self.user_thread = threading.Thread(target=self.client_main)
        self.user_thread.start()

    def open_thread(self):
        self.receiving_thread = threading.Thread(target=self.threaded_listen_to_server)
        self.receiving_thread.start()

    def create_client_socket(self):
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((config.SERVER_HOST, config.PORT))
        return clientsocket

    def create_account(self):
        print("create account")
        username = str(input("Username: "))
        return wire_protocol.marshal_request(config.ACCOUNT_CREATION, username, -1, -1)

    def log_in(self):
        print("log in")
        username = str(input("Username: "))
        return wire_protocol.marshal_request(config.LOG_IN, username, -1, -1)

    def send_message(self, sender_id: string="-1"):
        print("send_message")
        user_msg = str(input("Message to Send: "))
        receiver_id = str(input("Recipient username: "))
        return wire_protocol.marshal_request(config.SEND_MESSAGE, sender_id, receiver_id, user_msg)

    def request_messages(self, sender_id: string="-1"):
        print("request messages")
        user_msg = str(input("Messages with username: "))
        return wire_protocol.marshal_request(config.REQUEST_MESSAGES, sender_id, user_msg)

    def list_accounts(self):
        print("list accounts")
        account_str = str(input("Search for accounts (* to see them all): "))
        return wire_protocol.marshal_request(config.LIST_ACCOUNTS, -1, -1, account_str)

    def log_out(self, sender_id: string="-1"):
        print("log out")
        return wire_protocol.marshal_request(config.LOG_OUT, sender_id)

    def delete_account(self, sender_id: string="-1"):
        print("delete_account")
        return wire_protocol.marshal_request(config.ACCOUNT_DELETION, sender_id)

    def end_session(self):
        print("end session")
        return wire_protocol.marshal_request(config.END_SESSION, self.logged_in_user)
    
    def get_new_messages(self):
        print("looking for new messages")
        return wire_protocol.marshal_request(config.NEW_MESSAGES, self.logged_in_user)

    def parse_response(self, user_action, response_code, message):
        if user_action == config.ACCOUNT_CREATION:
            if response_code == 200:
                self.logged_in_user = message

                return 'Account: {} created and loged in succsessfully!'.format(message)

            elif response_code == 404:
                return 'Error creating account: {}'.format(message)
        elif user_action == config.LOG_IN:

            if response_code == 200:
                self.logged_in_user = message
                #Get New Messages
                bsmg = self.get_new_messages()
                self.clientsocket.send(bsmg)

                return 'Successfully logged in as: {}'.format(message)
            
            elif response_code == 404:
                return 'Error logging in: {}'.format(message)
            
        elif user_action == config.LIST_ACCOUNTS:
            if response_code == 200:
                return 'Accounts: {}'.format(message)
            elif response_code == 404:
                return 'Error listing accounts: {}'.format(message)

        elif user_action == config.SEND_MESSAGE:
            if response_code == 200:
                return 'Message sent successfully'
            elif response_code == 404:
                return 'Error sending message: {}'.format(message)
            
        elif user_action == config.REQUEST_MESSAGES:
            if response_code == 200:
                messageList = eval(message)
                
                if(len(messageList) == 0):
                    return 'No messages found'
                
                messageListResponse = "Messages with " + messageList[0][2] + ":\n"

                for msg in messageList:

                    intTimestamp = int((msg[5]).split(".", 1)[0])

                    timestamp = datetime.datetime.fromtimestamp(intTimestamp).strftime('%Y-%m-%d %H:%M:%S')
                    messageListResponse += ( "( " + timestamp + " ) " + msg[1] + " to " + msg[2] + " : " + msg[3] + '\n')

                return messageListResponse
            elif response_code == 404:
                return 'Error retrieving messages: {} '.format(message)
        
        elif user_action == config.NEW_MESSAGES:
            if response_code == 200:
                messageList = eval(message)

                if(len(messageList) == 0):
                    return "No messages sent while you were logged out"
                messageListResponse = "New Messages:\n"

                for msg in messageList:

                    intTimestamp = int((msg[5]).split(".", 1)[0])

                    timestamp = datetime.datetime.fromtimestamp(intTimestamp).strftime('%Y-%m-%d %H:%M:%S')
                    messageListResponse += ( "( " + timestamp + " ) " + msg[1] + " to " + msg[2] + " : " + msg[3] + '\n')
                
                return messageListResponse
            elif response_code == 201:
                return "No new messages"
            elif response_code == 404:
                return 'Error retrieving new messages: {} '.format(message)

        elif user_action == config.RECEIVE_MESSAGE:
            if response_code == 200:
                messageTuple = eval(message)
                return 'Message from {}: {} '.format(messageTuple[1], messageTuple[0])
            elif response_code == 404:
                return 'Error recieving message: {} '.format(message)
        elif user_action == config.ACCOUNT_DELETION:
            if response_code == 200:
                self.logged_in_user = None
                return 'Successfully deleted account: {} '.format(message)
            
            elif response_code == 404:
                return 'Error deleting account: {} '.format(message)
        elif user_action == config.LOG_OUT:
            if response_code == 200:
                
                self.logged_in_user = None
                return 'Successfully logged out: {} '.format(message)
            elif response_code == 404:
                return 'Error logging out: '.format(message)    
            
    def threaded_listen_to_server(self):
        while True: 
            message, originalMessage = self.listen_to_server_one_time()
            print('\n')
            print(message)
            print("Press enter to continue...")
  

            
    def listen_to_server_one_time(self):
        bdata, addr = self.clientsocket.recvfrom(1024)
        # parse the response and print the result
        response = wire_protocol.unmarshal_response(bdata)
        response_code = response['response_code']
        message = response['message']
        user_action = response['response_type']
        printResponse = self.parse_response(user_action, response_code, message)
        return printResponse, response

    def client_main(self):
        print("Starting client...")
        print("Connected.")

        try:
            while True:
                print("Logged In User: ", self.logged_in_user)
                user_action = client_utils.client_options_menu(self.logged_in_user)
                bmsg = b''

                # parse the user input and prepare the payload
                if self.logged_in_user:
                    if user_action == config.LIST_ACCOUNTS:
                        bmsg = self.list_accounts()
                    elif user_action == config.SEND_MESSAGE:
                        bmsg = self.send_message(sender_id=self.logged_in_user)
                    elif user_action == config.REQUEST_MESSAGES:
                        bmsg = self.request_messages(sender_id=self.logged_in_user)
                    elif user_action == config.ACCOUNT_DELETION:
                        bmsg = self.delete_account(sender_id=self.logged_in_user)
                    elif user_action == config.LOG_OUT:
                        bmsg = self.log_out(sender_id=self.logged_in_user)
                    else:
                        if (user_action == config.ERROR):
                            continue
                        else:
                            print("Please log out to perform this action.")
                            continue
                else:
                    if user_action == config.ACCOUNT_CREATION:
                        bmsg = self.create_account()
                    elif user_action == config.LOG_IN:
                        bmsg = self.log_in()
                    elif user_action == config.LIST_ACCOUNTS:
                        bmsg = self.list_accounts()
                    elif user_action == config.END_SESSION:
                        bmsg = self.end_session()
                        
                    else:
                        print("Please log in to perform this action.")
                        continue

                # send the payload along the wire
                sent = self.clientsocket.send(bmsg)
                print('Message sent, %d/%d bytes transmitted' % (sent, len(bmsg)))
                
                
                if user_action == config.END_SESSION:
                    print("Ending session...")
                    break           
                            
            # after loop, close socket
            self.clientsocket.shutdown(socket.SHUT_RDWR)
            self.clientsocket.close()
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            self.clientsocket.shutdown(socket.SHUT_RDWR)
            self.clientsocket.close()


# stuff to run always here such as class/def
def main():
    pass

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   client = Client()
