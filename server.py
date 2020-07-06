import socket
from _thread import *
from game import Game
from game import Player
import tkinter as tk

#uno = Game()

class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.list_of_clients = []

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


    def broadcast(self,message, client_socket):
        for client in self.list_of_clients:
            if client == client_socket:
                try:
                    client.send(message)
                except:
                    client.close()
                    self.list_of_clients.remove(client)

    def start_game(self):
        game = Game(self.list_of_clients)


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