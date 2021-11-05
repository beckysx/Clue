from Vertex import *
from Card import *
from Clue import *
from random import randint
from model import *
from tensorflow.keras.callbacks import ModelCheckpoint



def create_next_generation(model_list, gen_num):
    model_list[0].append(room_model().model.load_weights(room_path + "g" + str(gen_num - 1)))
    model_list[1].append(char_model().model.load_weights(char_path + "g" + str(gen_num - 1)))
    model_list[2].append(weapon_model().model.load_weights(weapon_path + "g" + str(gen_num - 1)))


def save_check_points(model_list, gen_num):
    model_list[0][gen_num].save_w(room_path, gen_num)
    print("save room" + str(gen_num))
    model_list[1][gen_num].save_w(char_path, gen_num)
    print("save char" + str(gen_num))
    model_list[2][gen_num].save_w(weapon_path, gen_num)
    print("save weapon" + str(gen_num))



if __name__ == '__main__':
    room_names = {"Conservatory": [[4, 4], "Lounge"], "Billiard": [[0, 12], [5, 8]], "Library": [[2, 12], [6, 15]],
                  "Study": [[5, 19], "Kitchen"], "Ballroom": [[6, 4], [8, 7], [13, 7], [15, 4]],
                  "Hall": [[7, 19], [10, 16], [11, 16]],
                  "Kitchen": [[18, 6], "Study"], "Dining": [[14, 11], [16, 15]], "Lounge": [[16, 17], "Conservatory"]}
    character_names = {"Mr.Green": [3, [8, 0]], "Mrs.White": [2, [13, 0]], "Col.Mustard": [1, [21, 16]],
                       "Prof.Plum": [5, [0, 18]], "Miss.Scarlett": [0, [15, 22]],
                       "Mrs.Peacock": [4, [0, 5]]}
    weapons = {"Candlestick": 0, "Dagger": 1, "Lead_Pipe": 2, "Revolver": 3, "Rope": 4, "Wrench": 5}
    models = [[room_model()], [char_model()], [weapon_model()]]
    room_path = "checkpoints/room/"
    char_path = "checkpoints/char/"
    weapon_path = "checkpoints/weapon/"

    for gen_num in range(2):
        if gen_num > 0:  # create next generation based on previous checkpoints
            create_next_generation(models,gen_num)
        X, Y = [[], [], []], [[], [], []]
        for i in range(1):
            print("generation" + str(gen_num) + "  game" + str(i))
            game = Clue(randint(3, 5), weapons, room_names, character_names)
            gameY = game.get_Y()
            for count in range(3):
                Y[count].append(gameY[count])
            turn_num = 0
            while game.status:
                turn_num += 1
                if turn_num % 20 == 0:
                    print("TURN: " + str(turn_num))
                game.one_turn(turn_num)
            gameX = game.get_X()
            for count in range(3):
                X[count].extend(gameX[count])
            for count in range(3):
                y_true = [Y[count][0] for c in range(len(X[count]))]  # duplicate true y for every training data
                models[count][gen_num].fit(X[count], y_true)

        # before next generation, save checkpoints for next generation
        save_check_points(models, gen_num)
