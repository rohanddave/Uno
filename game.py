import random
import _thread

class Card:
    def __init__(self, color, number):
        self.color = color
        self.number = number

    def is_playable(self, curr_card ): # curr_card is the topmost card
        if (curr_card.color == self.color or curr_card.number == self.number or self.color == 'special'):
            return True
        return False

class Player:
    def __init__(self):
        #self.socket = socket
        self.is_turn = False
        self.cards = []

    def show_cards(self):
        for card in self.cards:
            print(f"Color:{card.color} Number:{card.number}")

    def play_card(self,card,game):  # card here is the chosen card
        if (self.is_turn and card.is_playable(game.curr_card)):
            self.cards.remove(card)
            game.curr_card = card
            print(f"Card Played {card.color} {card.number}")


class Game:
    def __init__(self,players):
        self.normal_cards = []
        self.special_cards = []
        self.available_cards = []
        self.selected_cards = []
        self.all_cards = []
        self.players = []  # list of player objects
        self.number_cards = []
        self.non_number_cards = []

        normal_indexes = (0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12,12)  # 10 = skip , 11 = draw two , 12 = reverse
        special_indexes = (13, 13, 13, 13, 14, 14, 14, 14)  # 13 = wild , 14 = draw 4
        colors = ('red', 'blue', 'green', 'yellow')

        for color in colors:
            for n_index in normal_indexes:
                card = Card(color, n_index)
                self.normal_cards.append(card)
                if n_index <= 9:
                    self.number_cards.append(card)
                else:
                    self.non_number_cards.append(card)


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
            self.players.append(Player())

    def Diff(self,li1, li2):
        return (list(set(li1) - set(li2)))

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
        self.curr_card = random.choice(self.Diff(self.number_cards,self.available_cards))
        print(f"Current Card:{self.curr_card.color} {self.curr_card.number}")

        for player in self.players:
            print("CARDS FOR PLAYER:")
            player.show_cards()