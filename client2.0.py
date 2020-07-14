import socket
import pickle
import time


class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        self.host = "192.168.1.17"
        self.port = 5555

        self.client_socket.connect((self.host,self.port))

        self.run()

    def run(self):
        while True:
            try:
                received_msg = self.client_socket.recv(1024 * 4)
                unpickled_msg = pickle.loads(received_msg)
                if (unpickled_msg[2] == 'start'):
                    print(f"RECEIVED: {unpickled_msg}")

                    print("Player Cards:")
                    unpickled_msg[0].show_cards() #displays cards of player

                    print(f"Current Card:- Color: {unpickled_msg[1].curr_card.color} Number: {unpickled_msg[1].curr_card.number}") #made a change here

                    entry = int(input("Enter Serial Number of Card to be played"))

                    if(unpickled_msg[0].cards[entry].is_playable(unpickled_msg[1].curr_card)):
                        unpickled_msg[0].cards.remove(unpickled_msg[0].cards[entry])
                        unpickled_msg[1].curr_card = unpickled_msg[0].cards[entry]
                        #unpickled_msg[0].play_card(unpickled_msg[0].cards[entry], unpickled_msg[1])
                    else:
                        print("CANNOT PLAY THIS CARD!")

                print(f"SENDIG: {unpickled_msg}")
                #point_shower = PointShower(unpickled_msg)
                self.client_socket.send(pickle.dumps(unpickled_msg))  # change this line
                time.sleep(2)

            except socket.error as e:
                print(str(e))
client = Client()
client.run()