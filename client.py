import socket
import pickle
import time
import random

class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        self.host = input("Enter host IP Address")
        self.port = 5555

        try:
            self.client_socket.connect((self.host,self.port))
            print("Connected Successfully! Waiting for Server to Start Game ")
        except Exception as e:
            print(e)
            return


        self.run()

    def run(self):
        while True:
            try:
                received_msg = self.client_socket.recv(1024 * 4)
                unpickled_msg = pickle.loads(received_msg)  # [game obj , index of player obj]
                if (unpickled_msg[0].players[unpickled_msg[1]].is_turn == True):

                    print("Player Cards:")
                    unpickled_msg[0].players[unpickled_msg[1]].show_cards() #displays cards of player

                    print(f"Current Card:- Color: {unpickled_msg[0].curr_card.color} Number: {unpickled_msg[0].curr_card.number}") #made a change here

                    entry = int(input("Enter Serial Number of Card to be played"))

                    if(entry == 100): # pick up a card
                        picked_up_card_index = random.randrange(0,len(unpickled_msg[0].available_cards))
                        unpickled_msg[0].players[unpickled_msg[1]].cards.append(unpickled_msg[0].available_cards[picked_up_card_index])
                        unpickled_msg[0].available_cards.remove(unpickled_msg[0].available_cards[picked_up_card_index])

                    else:
                        if(unpickled_msg[0].players[unpickled_msg[1]].cards[entry].is_playable(unpickled_msg[0].curr_card)):
                            unpickled_msg[0].curr_card = unpickled_msg[0].players[unpickled_msg[1]].cards[entry]
                            if (unpickled_msg[0].curr_card.color == 'special'):
                                while True:
                                    choice = str(input("ENTER COLOR OF CHOICE"))
                                    choice.strip()
                                    colors = ['red','blue','green','yellow']
                                    if (choice in colors):
                                        unpickled_msg[0].curr_card.color = choice
                                        break
                                    else:
                                        continue

                            unpickled_msg[0].players[unpickled_msg[1]].cards.remove(unpickled_msg[0].players[unpickled_msg[1]].cards[entry])
                        else:
                            print("CANNOT PLAY THIS CARD!")
                    unpickled_msg[0].players[unpickled_msg[1]].is_turn = False
                    print(f"SENDING: {unpickled_msg}")
                    self.client_socket.send(pickle.dumps(unpickled_msg))  # change this line
                    time.sleep(2)

            except Exception as e:
                print(str(e))
client = Client()
client.run()
