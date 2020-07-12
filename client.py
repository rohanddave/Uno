import socket
import pickle
from _thread import *

class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        self.host = "192.168.1.17"
        self.port = 5555

        self.client_socket.connect((self.host,self.port))

        self.player_cards()

    def display_cards(self,player_obj):
        for card in player_obj.cards:
            print(f"Color: {card.color} Number: {card.number}")
        print(f"Number of cards {len(player_obj.cards)}")
        print("\n\n\n")

    def player_cards(self):
        while True:
            try:
                message = self.client_socket.recv(1024*4)
                player_info_data =pickle.loads(message)  # player_info_data = [player_obj , curr_card_obj , msg(string)]
                player_obj , curr_card , msg = player_info_data[0] , player_info_data[1] , player_info_data[2]
                print(f"CURRENT CARD:\n Color: {curr_card.color} Number:{curr_card.number}")
                self.display_cards(player_obj)
                #print(player_info_data)
                if (msg == 'play'):
                    entry = int(input("Enter corresponding card number to play"))
                    if(player_obj.cards[entry].is_playable):
                        print(f"Card Played!\n {player_obj.cards[entry].color}")
                        player_obj.play_card(player_obj.cards[entry])
                    else:
                        print("Cannot play card!")
                        continue

            except Exception as e:
                pass
                #print(str(e))

client = Client()
start_new_thread(client.player_cards , ())
