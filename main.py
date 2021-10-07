from Vertex import *
from Card import *
from Clue import *
import random

if __name__ == '__main__':
    room_names = {"Conservatory": [[4, 4], "Lounge"], "Billiard": [[0, 12], [5, 8]], "Library": [[2, 12], [6, 15]],
                  "Study": [[5, 19], "Kitchen"], "Ballroom": [[6, 4], [8, 7], [13, 7], [15, 4]],
                  "Hall": [[7, 19], [10, 16], [11, 16]],
                  "Kitchen": [[18, 6], "Study"], "Dining": [[14, 11], [16, 15]], "Lounge": [[16, 17], "Conservatory"]}
    character_names = {"Mr.Green": [3, [8, 0]], "Mrs.White": [2, [13, 0]], "Col.Mustard": [1, [21, 16]],
                       "Prof.Plum": [5, [0, 18]], "Miss.Scarlett": [0, [15, 22]],
                       "Mrs.Peacock": [4, [0, 5]]}
    weapons = ["Candlestick", "Dagger", "Lead_Pipe", "Revolver", "Rope", "Wrench"]
    test = Clue(3, weapons, room_names, character_names)
    while test.status:
        test.one_turn()
