from Card import *
from Vertex import *
import random
import math


class Player(object):
    def __init__(self, char_card, own_card_list, all_cards, n):
        self.character = char_card
        self.status = True  # active
        self.in_room = False  # 使用v label检查
        self.can_rowdice = True  # block can't rowdice
        self.can_suggest = False  # self.in_room 控制
        self.cards_have = own_card_list
        self.all_rooms = []
        self.p_weapons, self.im_weapons = [], []
        self.p_rooms, self.im_rooms = [], []
        self.p_characters, self.im_characters = [], []
        self.curr_location = None  # should be a vertex
        self.player_card_records = [[] for i in range(n)]
        for card in all_cards:  # put card into different categories
            if card.get_category() == "weapon":
                if card in own_card_list:
                    self.im_weapons.append(card)
                else:
                    self.p_weapons.append(card)
            elif card.get_category() == "room":
                self.all_rooms.append(card)
                if card in own_card_list:
                    self.im_rooms.append(card)
                else:
                    self.p_rooms.append(card)
            else:
                if card in own_card_list:
                    self.im_characters.append(card)
                else:
                    self.p_characters.append(card)

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

    def move_to(self, new_location):
        if new_location.isRoom():
            self.can_suggest = True
        self.curr_location = new_location

    def isActive(self):
        return self.status

    def can_make_suggest(self):
        return self.can_suggest

    def only_one_combination(self):
        print("possible choices:")
        print(*self.p_rooms, sep=" ")
        print(*self.p_weapons, sep=" ")
        print(*self.p_characters, sep=" ")
        return len(self.p_rooms) == 1 and len(self.p_weapons) == 1 and len(self.p_characters) == 1

    def make_suggestion(self, room):
        self.can_suggest = False
        person = random.choice(self.p_characters)
        weapon = random.choice(self.p_weapons)
        self.can_suggest = False
        return [room, person, weapon]

    def have_card(self, card):
        for c in self.cards_have:
            if c == card:
                return True
        return False

    def is_p_room(self, room_name):
        if room_name is None:
            return False
        for card in self.p_rooms:
            if card.get_name() == room_name:
                return True
        return False

    def disprove(self, suggestion):
        range = []
        for card in suggestion:
            bool = self.have_card(card)
            if bool:
                range.append(card)
        priority = []
        if len(range) > 1:
            for card in range:
                if card.have_shown:
                    priority.append(card)
            if len(priority) > 0:
                return [random.choice(priority)]
        return random.choice(range) if len(range) > 0 else None

    def elliminate(self, card, card_owner):
        if card.isRoom():
            self.im_rooms.append(card)
            self.p_rooms = card.delete_from(self.p_rooms)
            print("after delete from")
            print(*self.p_rooms, sep=",")
        elif card.isWeapon():
            self.im_weapons.append(card)
            self.p_weapons = card.delete_from(self.p_weapons)
            print("after delete from")
            print(*self.p_weapons, sep=",")
        elif card.isChar():
            self.im_characters.append(card)
            self.p_characters = card.delete_from(self.p_characters)
            print("after delete from")
            print(*self.p_characters, sep=",")
        self.player_card_records[card_owner.get_num()].append(card)

    def make_accusation(self, suggestion=None):
        self.status = False
        if suggestion is not None:
            return suggestion
        room = random.choice(self.p_rooms)
        person = random.choice(self.p_characters)
        weapon = random.choice(self.p_weapons)
        return [room, person, weapon]

    def update_room_distance(self, path_dict):
        for k, v in path_dict.items():
            for room_card in self.all_rooms:
                if room_card.name == k:
                    room_card.distance == v[1]
        self.all_rooms.sort()
        return self.all_rooms

    def __str__(self):
        return self.character.get_name()
