class Card:
    def __init__(self, color, number):
        self.color = color
        self.number = number

    def is_playable(self, curr_card):
        if (curr_card.color == self.color or curr_card.number == self.number):
            return True
        return False

class Player:
    def __init__(self,socket,addr):
        self.socket = socket
        self.addr = addr
        self.cards = []


class Game:
    def __init__(self):
        self.normal_cards = []
        self.special_cards = []
        self.available_cards = []
        self.players = []

        normal_indexes = (0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12,12)  # 10 = skip , 11 = draw two , 12 = reverse
        special_indexes = (13, 13, 13, 13, 14, 14, 14, 14)  # 13 = wild , 14 = draw 4
        colors = ('red', 'blue', 'green', 'yellow')

        for color in colors:
            for n_index in normal_indexes:
                self.normal_cards.append(Card(color, n_index))

        for s_index in special_indexes:
            self.special_cards.append(Card('special', s_index))

        self.available_cards = self.normal_cards + self.special_cards
        #print(len(self.available_cards))
        print("Game initialised")

    def add_player(self,player):
        print(f"{player.addr[0]} added! Socket:{player.socket}")
        self.players.append(player)