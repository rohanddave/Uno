import socket


client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host = "192.168.1.17"
port = 5555

client_socket.connect((host,port))

while True:
    try:
        received_msg = client_socket.recv(1024)
        print("Received: ",received_msg.decode())
        '''msg = "message from desktop to server"
        client_socket.send(str.encode(msg))'''
    except socket.error as e:
        print(str(e))
        break