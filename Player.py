from Card import *
from Vertex import *

class Player(object):
    def __init__(self, char_card, own_card_list, all_cards):
        self.character = char_card
        self.status = True  # active
        self.in_room = False  # 使用v label检查
        self.can_rowdice = True  # block can't rowdice
        self.can_suggest = False  # self.in_room 控制
        self.cards_have = own_card_list
        self.p_weapons, self.im_weapons = [], []
        self.p_rooms, self.im_rooms = [], []
        self.p_characters, self.im_characters = [], []
        self.curr_location = None  # should be a vertex
        for card in all_cards:  # put card into different categories
            print(type(card))
            if card.category() == "weapon":
                if card in own_card_list:
                    self.p_weapons.append(card)
                else:
                    self.im_weapons.append(card)
            elif card.category() == "room":
                if card in own_card_list:
                    self.p_rooms.append(card)
                else:
                    self.im_rooms.append(card)
            else:
                if card in own_card_list:
                    self.p_characters.append(card)
                else:
                    self.im_characters.append(card)

    def __lt__(self, other):
        return self.character < other.character

    def change_num(self, num):
        self.character.change_num(num)

    def get_num(self):
        return self.character.get_num()

    def get_character(self):
        return self.character

    def get_name(self):
        return self.character.get_name()

    def change_location(self, new_location):
        self.curr_location = new_location

