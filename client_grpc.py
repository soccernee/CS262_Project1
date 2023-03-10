import _thread
import time

import client_utils
import config
import grpc
import messages_pb2 as pb2
import messages_pb2_grpc as pb2_grpc
import string
import signal

class GrpcClient():

    def __init__(self):
        self.host = config.SERVER_HOST
        self.port = config.GRPC_PORT
        self.logged_in_user = None

        # instantiate the channel
        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.port))
        
        self.stub = pb2_grpc.MessageExchangeStub(self.channel)
        #Logic to handle SIGINT
        self.SIGINT = False
        signal.signal(signal.SIGINT, self.signal_handler)

        self.main()

    def create_account(self):
        print("create account")
        username = str(input("Username: "))
        response = self.stub.CreateAccount(pb2.AccountRequest(name=username))
        print(response)
        if response.response_code == 200:
            self.logged_in_user = username
            _thread.start_new_thread(self.get_new_message_stream, ())
        elif response.response_code == 404:
            print("Error creating an account: ", response.response_text)

    def log_in(self):
        print("log in")
        username = str(input("Username: "))
        response = self.stub.LogIn(pb2.AccountRequest(name=username))
        print(response)
        if response.response_code == 200:
            self.logged_in_user = username
            _thread.start_new_thread(self.get_new_message_stream, ())

        elif response.response_code == 404:
            print("Error logging in: ", response.response_text)

    def send_message(self, sender_id: string="-1"):
        print("send_message")
        user_msg = str(input("Message to Send: "))
        receiver_id = str(input("Receiver username: "))
        send_message_response = self.stub.SendMessage(
            pb2.SendMessageRequest(
                sender_id=self.logged_in_user,
                receiver_id=receiver_id,
                message=user_msg
            )
        )
        print(send_message_response)

    def request_messages(self):
        print("request messages")
        receiver_id = str(input("Messages with username: "))
        request_messages_response = self.stub.RequestMessages(
            pb2.RequestMessagesRequest(
                sender_id=self.logged_in_user,
                receiver_id=receiver_id
            )
        )
        print(request_messages_response)

    def list_accounts(self):
        print("list accounts")
        account_str = str(input("Search for accounts (* to see them all): "))
        list_accounts_response = self.stub.ListAccounts(pb2.ListAccountsRequest(search_pattern=account_str))
        print(list_accounts_response)

    def log_out(self):
        print("log out")
        response = self.stub.LogOut(pb2.AccountRequest(name=self.logged_in_user))
        print(response)
        if response.response_code == 200:
            self.logged_in_user = None
        elif response.response_code == 404:
            print("Error logging out: ", response.response_text)

    def delete_account(self, sender_id: string="-1"):
        print("delete_account")
        response = self.stub.DeleteAccount(pb2.AccountRequest(name=self.logged_in_user))
        print(response)
        if response.response_code == 200:
            self.logged_in_user = None
        elif response.response_code == 404:
            print("Error logging out: ", response.response_text)

    def get_new_message_stream(self):
        while self.logged_in_user:
            response = self.stub.GetNewMessages(pb2.GetNewMessagesRequest(sender_id=self.logged_in_user))
            if response.response_code == 200:
                print("New Messages: ", response)
                print("Press enter to continue...")

            #How long we wait to poll the server for new messages  
            time.sleep(1)

        return

    def end_session(self):
        if self.logged_in_user:
            self.log_out()


    def signal_handler(self, signal, frame):
        
        print('You quit the program!')
        self.end_session()
        self.SIGINT = True
        sys.exit(0)

    def main(self):
        print("Starting client...")

        try:
            while True:
                print("Logged In User: ", self.logged_in_user)
                user_action = client_utils.client_options_menu(self.logged_in_user)
                
                # parse the user input and prepare the payload
                if self.logged_in_user:
                    if user_action == config.LIST_ACCOUNTS:
                        self.list_accounts()
                    elif user_action == config.SEND_MESSAGE:
                        self.send_message()
                    elif user_action == config.REQUEST_MESSAGES:
                        self.request_messages()
                    elif user_action == config.ACCOUNT_DELETION:
                        self.delete_account()
                    elif user_action == config.LOG_OUT:
                        self.log_out()
                    else:
                        if (user_action == config.ERROR):
                            continue
                        else:
                            print("Please log out to perform this action.")
                            continue
                else:
                    if user_action == config.ACCOUNT_CREATION:
                        self.create_account()
                    elif user_action == config.LOG_IN:
                        self.log_in()
                    elif user_action == config.LIST_ACCOUNTS:
                        self.list_accounts()
                    elif user_action == config.END_SESSION:
                        self.end_session()
                        
                    else:
                        if (user_action == config.ERROR):
                            continue
                        else:
                            print("Please log in to perform this action.")
                            continue

                if user_action == config.END_SESSION:
                    print("Ending session...")
                    break

        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")



client = GrpcClient()

#Used if the user presses Ctrl+C

