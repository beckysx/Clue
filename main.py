from Vertex import *
from Card import *
from Clue import *
import random
from model import *

if __name__ == '__main__':
    room_names = {"Conservatory": [[4, 4], "Lounge"], "Billiard": [[0, 12], [5, 8]], "Library": [[2, 12], [6, 15]],
                  "Study": [[5, 19], "Kitchen"], "Ballroom": [[6, 4], [8, 7], [13, 7], [15, 4]],
                  "Hall": [[7, 19], [10, 16], [11, 16]],
                  "Kitchen": [[18, 6], "Study"], "Dining": [[14, 11], [16, 15]], "Lounge": [[16, 17], "Conservatory"]}
    character_names = {"Mr.Green": [3, [8, 0]], "Mrs.White": [2, [13, 0]], "Col.Mustard": [1, [21, 16]],
                       "Prof.Plum": [5, [0, 18]], "Miss.Scarlett": [0, [15, 22]],
                       "Mrs.Peacock": [4, [0, 5]]}
    weapons = {"Candlestick": 0, "Dagger": 1, "Lead_Pipe": 2, "Revolver": 3, "Rope": 4, "Wrench": 5}
    models = [room_model(), char_model(), weapon_model()]

    for i in range(1):
        X = [[], [], []]
        Y = [[], [], []]
        game = Clue(3, weapons, room_names, character_names)
        gameY = game.get_Y()
        for count in range(3):
            Y[count].append(gameY[count])
        turn_num = 0
        while game.status:
            turn_num += 1
            print("TURN: " + str(turn_num))
            game.one_turn(turn_num)
        gameX = game.get_X()
        for count in range(3):
            X[count].extend(gameX[count])
        for count in range(3):
            y_true = [Y[count][0] for c in range(len(X[count]))]
            models[count].fit(X[count], y_true)
