import socket
from _thread import *
from game import Game
from game import Player

uno = Game()
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host = "192.168.1.17"
port = 5555

try:
    server_socket.bind((host,port))
except socket.error as e:
    print(str(e))

server_socket.listen(4)

list_of_clients = []

def threaded_client(client_socket , addr):
    player_client = Player(client_socket,addr)
    uno.add_player(player_client)
    client_socket.send(str.encode("You were added to the game!"))
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"<{addr[0]}>{message.decode()}")
            else:
                print("Removing:",addr[0])
                list_of_clients.remove(client_socket)
        except Exception as e:
            print(str(e))
            break


def broadcast(message, client_socket):
    for client in list_of_clients:
        if client == client_socket:
            try:
                client.send(message)
            except:
                client.close()
                list_of_clients.remove(client)

while True:
    client_socket , addr = server_socket.accept()
    list_of_clients.append(client_socket)
    print(f"{addr} connected!")
    start_new_thread(threaded_client , (client_socket,addr))
