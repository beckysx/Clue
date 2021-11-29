from Clue import *
from model import *
from tensorflow.keras.models import load_model

room_names = {"Conservatory": [[4, 4], "Lounge"], "Billiard": [[0, 12], [5, 8]], "Library": [[2, 12], [6, 15]],
              "Study": [[5, 19], "Kitchen"], "Ballroom": [[6, 4], [8, 7], [13, 7], [15, 4]],
              "Hall": [[7, 19], [10, 16], [11, 16]],
              "Kitchen": [[18, 6], "Study"], "Dining": [[14, 11], [16, 15]], "Lounge": [[16, 17], "Conservatory"]}
character_names = {"Mr.Green": [3, [8, 0]], "Mrs.White": [2, [13, 0]], "Col.Mustard": [1, [21, 16]],
                   "Prof.Plum": [5, [0, 18]], "Miss.Scarlett": [0, [15, 22]],
                   "Mrs.Peacock": [4, [0, 5]]}
weapons = {"Candlestick": 0, "Dagger": 1, "Lead_Pipe": 2, "Revolver": 3, "Rope": 4, "Wrench": 5}
room_path = "checkpoints/room/"
char_path = "checkpoints/char/"
weapon_path = "checkpoints/weapon/"
g10 = [room_model(), char_model(), weapon_model()]
g10[0].model = load_model(room_path + "g10")
g10[1].model = load_model(char_path + "g10")
g10[2].model = load_model(weapon_path + "g10")

for gen_num in range(0, 11):
    g = [room_model(), char_model(), weapon_model()]
    g[0].model = load_model(room_path + "g" + str(gen_num))
    g[1].model = load_model(char_path + "g" + str(gen_num))
    g[2].model = load_model(weapon_path + "g" + str(gen_num))
    agents = [g, g10]
    g10_win = 0
    for i in range(50):
        game = Clue(4, weapons, room_names, character_names, agents)
        turn_num = 0
        while game.status:
            turn_num += 1
            game.one_turn(turn_num)
        winner = game.winner
        if winner % 2 == 1:
            g10_win += 1
    print(g10_win)
