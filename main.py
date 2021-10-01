from Vertex import *
from Card import *
from Clue import *
import random

if __name__ == '__main__':
    room_names = {"Conservatory": [[4, 4]], "Billiard": [[0, 12], [5, 8]], "Library": [[2, 12], [6, 15]],
                  "Study": [[5, 19]], "Ballroom": [[6, 4], [8, 7], [13, 7], [15, 4]],
                  "Hall": [[7, 19], [10, 16], [11, 16]],
                  "Kitchen": [[18, 5]], "Dining": [[14, 11], [16, 15]], "Lounge": [[16, 17]]}
    character_names = {"Mr.Green": [3, [0, 8]], "Mrs.White": [2, [0, 13]], "Col.Mustard": [1, [21, 16]],
                       "Prof.Plum": [5, [0, 18]], "Miss.Scarlett": [0, [15, 22]],
                       "Mrs.Peacock": [4, [0, 5]]}
    weapons = ["Candlestick", "Dagger", "Lead_Pipe", "Revolver", "Rope", "Wrench"]
    test = Clue(6, weapons, room_names, character_names)
