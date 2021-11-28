from Vertex import *
from Card import *
from Clue import *
from random import randint
from model import *
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.models import load_model


def create_next_generation(model_list, gen_num):
    model_list[0].append(room_model())
    model_list[0][gen_num].model = load_model(room_path + "g" + str(gen_num - 1))
    model_list[1].append(char_model())
    model_list[1][gen_num].model = load_model(char_path + "g" + str(gen_num - 1))
    model_list[2].append(weapon_model())
    model_list[2][gen_num].model = load_model(weapon_path + "g" + str(gen_num - 1))


def save_check_points(model_list, gen_num):
    model_list[0][gen_num].save_model(room_path, gen_num)
    model_list[1][gen_num].save_model(char_path, gen_num)
    model_list[2][gen_num].save_model(weapon_path, gen_num)


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
    save_check_points(models, 0)  # save initial random model  g0

    for gen_num in range(1, 11, 1):
        if gen_num > 0:  # create next generation based on previous checkpoints
            create_next_generation(models, gen_num)
        for i in range(1):
            print("generation" + str(gen_num) + "  game" + str(i))
            game = Clue(6, weapons, room_names, character_names)
            gameY = game.get_Y()
            turn_num = 0
            X = [[], [], []]
            while game.status:
                turn_num += 1
                # if turn_num % 20 == 0:
                #     print("TURN: " + str(turn_num))
                game.one_turn(turn_num)
                gameX = game.get_X()  # [[],[],[]]
                for count in range(3):
                    X[count].extend(gameX[count])
                if turn_num > 700:
                    break
            for count in range(3):
                if len(X[count]) == 0:
                    continue
                y_true = [gameY[count] for c in range(len(X[count]))]  # duplicate true y for every training data
                models[count][gen_num].fit(X[count], y_true)

        # before next generation, save checkpoints for next generation
        save_check_points(models, gen_num)
