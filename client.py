import socket
import pickle
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host = "192.168.1.17"
port = 5555

client_socket.connect((host,port))

while True:
    try:
        msg = client_socket.recv(1024*4)
        player_obj  = pickle.loads(msg)
        print(f"Received: {player_obj} and it's type: {type(player_obj)}")
        for card in player_obj.cards:
            print(f"Color: {card.color} Number: {card.number}")
        print(f"Number of cards {len(player_obj.cards)}")
        '''msg = "message from desktop to server"
        client_socket.send(str.encode(msg))'''
    except Exception as e:
        print(str(e))
