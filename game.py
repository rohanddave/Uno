import random
class Card:
    def __init__(self, color, number):
        self.color = color
        self.number = number

    def is_playable(self, curr_card):
        if (curr_card.color == self.color or curr_card.number == self.number):
            return True
        return False

class Player:
    def __init__(self,socket):
        self.socket = socket
        #self.addr = addr
        self.cards = []

    def show_cards(self):
        for card in self.cards:
            print(f"Color:{card.color} Number:{card.number}")


class Game:
    def __init__(self,players):
        self.normal_cards = []
        self.special_cards = []
        self.available_cards = []
        self.selected_cards = []
        self.all_cards = []
        self.players = []

        normal_indexes = (0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12,12)  # 10 = skip , 11 = draw two , 12 = reverse
        special_indexes = (13, 13, 13, 13, 14, 14, 14, 14)  # 13 = wild , 14 = draw 4
        colors = ('red', 'blue', 'green', 'yellow')

        for color in colors:
            for n_index in normal_indexes:
                self.normal_cards.append(Card(color, n_index))

        for s_index in special_indexes:
            self.special_cards.append(Card('special', s_index))

        self.all_cards = self.normal_cards + self.special_cards
        self.available_cards = self.all_cards

        #print(len(self.available_cards))
        print("Game initialised!")
        self.add_players(players)
        self.show_players()
        self.deal_cards()

    def add_players(self,player_sockets):
        for player_socket in player_sockets:
            self.players.append(Player(player_socket))

    def show_players(self):
        for player in self.players:
            print(f"{player} added!")
            #self.players.append(player)
        print(f"Number of players in game:{len(self.players)}")

    def deal_cards(self):
        for player in self.players:
            player.cards.extend(random.choices(self.available_cards,k=7))
            self.selected_cards+=player.cards
            for card in self.selected_cards:
                if card in self.available_cards:
                    self.available_cards.remove(card)

        for player in self.players:
            print("CARDS FOR PLAYER:")
            player.show_cards()