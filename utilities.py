import time
class Cq:
    def __init__(self, list_of_players):  # list of objects of type Player
        self.pointer = -1
        self.list_of_players = list_of_players
    def next_player(self):
        self.pointer+=1
        return self.list_of_players[self.pointer % len(self.list_of_players)]

class Timer:
    def countdown(self,time_limit):
        while time_limit > 0:
            #print(time_limit)
            time_limit -= 1
            time.sleep(1)