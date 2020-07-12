import socket
from _thread import *
from game import Game
from utilities import Cq
from utilities import Timer
import tkinter as tk
import pickle

class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.list_of_clients = [] #LIST OF CLIENT SOCKETS


        self.host = "192.168.1.17"
        self.port = 5555

        try:
            self.server_socket.bind((self.host,self.port))
        except socket.error as e:
            print(str(e))

        self.server_socket.listen(4)

    def threaded_client(self,client_socket , addr):
        #player_client = Player(client_socket,addr)
        #uno.add_player(player_client)
        client_socket.send(str.encode("You joined the server!"))
        client_socket.send(str.encode("message from server"))
        while True:
            try:
                message = client_socket.recv(1024)
                if message:
                    print(f"<{addr[0]}>{message.decode()}")
                else:
                    print("Removing:",addr[0])
                    self.list_of_clients.remove(client_socket)
            except Exception as e:
                print(str(e))
                break


    '''def broadcast(self,message, client_socket):
        for client in self.list_of_clients:
            if client == client_socket:
                try:
                    client.send(message)
                except:
                    client.close()
                    self.list_of_clients.remove(client)'''

    def send_player_info(self,game):     # sends a list [player_obj , curr_card , msg] where msg = 'play' if that player's turn else msg = 'wait'
        for i in range(0, len(self.list_of_clients)):
            msg = "play"
            if self.curr_player != game.players[i]:
                msg = "wait"
            msg_list = [game.players[i] , game.curr_card , msg]
            pickled_message = pickle.dumps(msg_list)
            print(f"Type: {type(pickled_message)} pickle data:{pickled_message} END")
            self.list_of_clients[i].send(pickled_message)

    def start_game(self):
        game = Game(self.list_of_clients)
        #self.curr_player_socket = self.list_of_clients[0]
        circular_queue = Cq(game.players)
        timer = Timer()
        while True:  #main game loop
            self.curr_player , self.curr_player_index= circular_queue.next_player()
            self.curr_player.is_turn = True
            self.curr_player_socket = self.list_of_clients[self.curr_player_index]
            #self.curr_player_socket.send(str.encode("your turn"))
            print(f"current player is {self.curr_player}")
            self.send_player_info(game)
            timer.countdown(10)

server = Server()

def tkinter():
    window = tk.Tk()
    b = tk.Button(window , text = "Start",command = server.start_game)
    b.pack()
    window.mainloop()

tkinter_thread = start_new_thread(tkinter,())
while True:
    print("Server listening for connections.....")
    client_socket , addr = server.server_socket.accept()
    server.list_of_clients.append(client_socket)
    print(f"{addr} connected!")
    start_new_thread(server.threaded_client , (client_socket,addr))
