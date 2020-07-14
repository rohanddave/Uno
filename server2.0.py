import socket
from _thread import *
import pickle
from game import Player
from game import Game
import time
import tkinter as tk

'''p1 = Player('rohan', 0)
p2 = Player('aj',0)
p3 = Player('suraj',0)'''

class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.list_of_client_sockets = []
        self.info_list = [] # [ player_obj , game , msg ]

        self.host = "192.168.1.17"
        self.port = 5555

        self.server_socket.bind((self.host,self.port))

        self.server_socket.listen(4)


    def run(self):
        while True:
            print("listening for connections....")
            client_socket, addr = self.server_socket.accept()
            print(f"{addr[0]} connected to server!")
            self.list_of_client_sockets.append(client_socket)
            game.players.append(Player())
            start_new_thread(self.threaded_client, (client_socket, addr))

    def threaded_client(self,client_socket ,addr):
        #message_list = [p1,p2,p3]
        player_obj = game.players[self.list_of_client_sockets.index(client_socket)]
        self.msg = 'init'


        while True:
            message_list = [player_obj, game, self.msg]
            try:
                client_socket.send(pickle.dumps(message_list))

                message = client_socket.recv(1024 * 4)
                message_list = pickle.loads(message)
                print(f"Received: {message_list}")
                #point_shower = PointShower(message_list)
            except Exception as e:
                print(e)

            time.sleep(2)

    def start_game(self):
        game.show_players()
        game.deal_cards()
        self.msg = 'start'

server = Server()
game = Game()
def tkinter():
    window = tk.Tk()
    b1 = tk.Button(window , text = "start",command = server.start_game)
    b1.pack()
    window.mainloop()

start_new_thread(tkinter , ())

server.run()