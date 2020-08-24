import socket
from _thread import *
import pickle
from game import Player , Game
import random
import tkinter as tk
from utilities import Cq
from utilities import Timer


class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.list_of_client_sockets = []
        self.info_list = [] # [ player_obj , game , msg ]

        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 5555

        self.server_socket.bind((self.host,self.port))

        self.server_socket.listen(4)

        self.message_list = []

        self.game = Game()

    def run(self):
        while True:
            print("listening for connections....")
            client_socket, addr = self.server_socket.accept()
            print(f"{addr[0]} connected to server!")
            self.list_of_client_sockets.append(client_socket)
            self.game.players.append(Player())

    def start_game(self): # working on tkinter thread

        self.queue = Cq(self.game.players)
        self.timer = Timer()

        self.game.deal_cards()

        self.msg = 'start'
        index = -1
        while True:  # everything that the server does
            self.message_list = [self.game,index]  # [game_obj , index of player]
            print(self.message_list[0].curr_card)
            for i in range(0,len(self.list_of_client_sockets)):

                if(self.message_list[0].curr_card.number == 11): # for draw 2
                    for i in range(0,2):
                        random_index = random.randrange(0, len(self.message_list[0].available_cards))
                        self.message_list[0].players[(i+1)%len(self.list_of_client_sockets)].cards.append(self.message_list[0].available_cards[random_index])
                        self.message_list[0].available_cards.remove(self.message_list[0].available_cards[random_index])
                self.message_list[1]=i # index = i
                self.message_list[0].players[i].is_turn = True
                self.list_of_client_sockets[i].send(pickle.dumps(self.message_list))
                try:
                    recieved_pickled_message = self.list_of_client_sockets[i].recv(1024 * 4)
                    self.message_list = pickle.loads(recieved_pickled_message)
                except:
                    pass
            self.game = self.message_list[0]
            index = -1

server = Server()

def tkinter():
    window = tk.Tk()
    b1 = tk.Button(window , text = "start",command = server.start_game)
    b1.pack()
    window.mainloop()

start_new_thread(tkinter , ())

server.run()
