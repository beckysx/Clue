from Vertex import *
from Card import *


def blank_exist(x, y):
    if y == 0:
        if 0 <= x <= 5 or 9 <= x <= 12 or 16 <= x <= 21:
            return False
    elif y ==1 or y == 2 or y ==3 :
        if 0 <= x <= 4 or 7 <= x <= 14 or 17 <= x <= 21:
            return False
    elif y == 4:
        if 0 <= x <= 3 or 7 <= x <= 14 or 17 <= x <= 21:
            return False
    elif y == 5:
        if 7 <= x <= 14 or 17 <= x <= 21:
            return False
    elif y ==6:
        if 7 <= x <= 14:
            return False
    elif y == 7:
        if 0 <= x <= 4:
            return False
    elif y ==8:
        if 0 <= x <= 4 or 18 <= x <= 21:
            return False
    elif y ==9 or y == 10 or y == 11 or y == 13:
        if 0 <= x <= 4 or 8 <= x <= 12 or 15 <= x <= 21:
            return False
    elif y == 12:
        if 8 <= x <= 12 or 15 <= x <= 21:
            return False
    elif y ==14:
        if 0 <= x <= 5 or 8 <= x <= 12 or 15 <= x <= 21:
            return False
    elif y ==15:
        if 0 <= x <= 5 or 8 <= x <= 12:
            return False
    elif y ==16:
        if 0 <= x <= 5:
            return False
    elif y ==17:
        if 0 <= x <= 4 or 8 <= x <= 13:
            return False
    elif y == 18 or y == 19 :
        if 8 <= x <= 13 or 16 <= x <= 21:
            return False
    elif y == 20 or y == 21 or y == 22:
        if 0 <= x <= 5 or 8 <= x <= 13 or 16 <= x <= 21:
            return False
    return True


def generate_blank_vertices():
    blank_vertices = []
    for y in range(23):
        for x in range(22):
            if blank_exist(x, y):
                blank_vertices.append(Blank(x, y))
    return blank_vertices


if __name__ == '__main__':
    room_names = ["Ballroom", "Kitchen", "Conservatory", "Billiard", "Library", "Dining", "Study", "Hall", "Lounge"]
    character_names = {"Mr.Green": 3, "Mrs.White": 2, "Col.Mustard": 1, "Prof.Plum": 5, "Miss.Scarlett": 0,
                       "Mrs.Peacock": 4}
    weapons = ["Candlestick", "Dagger", "Lead_Pipe", "Revolver", "Rope", "Wrench"]
    room_vertices = [Room(room_name) for room_name in room_names]
    start_vertices = [GreenStart(char_name) for char_name in character_names.keys()]
    blank_vertices = generate_blank_vertices()
    room_cards = [Room_card(room_name) for room_name in room_names]
    char_cards = [Character(name=k, num=v) for k, v in character_names.items()]
    weapon_cards = [Weapon(weapon) for weapon in weapons]
