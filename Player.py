from Card import *
from Vertex import *
import random
import math
from itertools import chain, combinations


class Player(object):
    def __init__(self, char_card, own_card_list, n):
        self.character = char_card
        self.num = 0
        self.n = n
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
        self.room_p_table = [[0 for i in range(8)] for i in range(9)]  # 0~5 players, 6 distance, 7 time records
        self.weapon_p_table = [[0 for i in range(7)] for i in range(6)]  # 0~5 players, 6 time records
        self.character_p_table = [[0 for i in range(7)] for i in range(6)]  # 0~5 players, 6 time records

    def player_set_up(self, all_cards, n):
        p = 1 / (n - 1)
        i = self.get_num()
        for card in all_cards:  # put card into different categories, initiate posibility tables
            if card.get_category() == "weapon":
                if card in self.cards_have:
                    self.im_weapons.append(card)
                    self.weapon_p_table[card.num][i] = 1
                else:
                    self.p_weapons.append(card)
                    for index in range(n):
                        if index != i:
                            self.weapon_p_table[card.num][index] = p
            elif card.get_category() == "room":
                self.all_rooms.append(card)
                if card in self.cards_have:
                    self.im_rooms.append(card)
                    self.room_p_table[card.num][i] = 1
                else:
                    self.p_rooms.append(card)
                    for index in range(n):
                        if index != i:
                            self.room_p_table[card.num][index] = p
            else:  # character card
                if card in self.cards_have:
                    self.im_characters.append(card)
                    self.character_p_table[card.num][i] = 1
                else:
                    self.p_characters.append(card)
                    for index in range(n):
                        if index != i:
                            self.character_p_table[card.num][index] = p

    def __lt__(self, other):
        return self.character < other.character

    def change_num(self, num):
        self.num = num

    def get_num(self):
        return self.num

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
        # print("possible choices:")
        # print(*self.p_rooms, sep=" ")
        # print(*self.p_weapons, sep=" ")
        # print(*self.p_characters, sep=" ")
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
            # print("after delete from")
            # print(*self.p_rooms, sep=",")
        elif card.isWeapon():
            self.im_weapons.append(card)
            self.p_weapons = card.delete_from(self.p_weapons)
            # print("after delete from")
            # print(*self.p_weapons, sep=",")
        elif card.isChar():
            self.im_characters.append(card)
            self.p_characters = card.delete_from(self.p_characters)
            # print("after delete from")
            # print(*self.p_characters, sep=",")

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
                    self.room_p_table[room_card.num][6] = v[1]
        self.all_rooms.sort()
        return self.all_rooms

    # functions use to update possibility tables
    def suggestion_update(self, suggestion):  # suggestion = [room, person, weapon]
        self.room_p_table[suggestion[0].num][7] += 1
        self.character_p_table[suggestion[1].num][6] += 1
        self.weapon_p_table[suggestion[2].num][6] += 1

    def zero_out_vertical(self, suggestion, person):  # this person has none of card in suggestion
        i = person.num
        self.room_p_table[suggestion[0].num][i] = 0
        self.character_p_table[suggestion[1].num][i] = 0
        self.weapon_p_table[suggestion[2].num][i] = 0

    def zero_out_horizontal(self, card, person):  # explicitly know this person have this card
        i, card_type, num = person.num, card.get_category(), card.num
        if card_type == "weapon":
            self.weapon_p_table[num][0:6] = [0 for x in range(6)]
            self.weapon_p_table[num][i] = 1
        elif card_type == "room":
            self.room_p_table[num][0:6] = [0 for x in range(6)]
            self.room_p_table[num][i] = 1
        else:
            self.character_p_table[num][0:6] = [0 for x in range(6)]
            self.character_p_table[num][i] = 1

    def check_1_exist(self, card):
        i, card_type = card.num, card.get_category()
        if card_type == "weapon":
            return 1 in self.weapon_p_table[i][0:6]
        elif card_type == "room":
            return 1 in self.room_p_table[i][0:6]
        else:
            return 1 in self.character_p_table[i][0:6]

    def conditional_probability(self, suggestion, revealor, suggestor):  # suggestion = [room, person, weapon]
        i = revealor.get_num()
        s_i = suggestor.get_num()
        # room_line, char_line, weapon_line
        old_lines = [self.room_p_table[suggestion[0].num], self.character_p_table[suggestion[1].num],
                     self.weapon_p_table[suggestion[2].num]]
        new_lines = old_lines.copy()
        Crr, Ccr, Cwr = old_lines[0][i], old_lines[1][i], old_lines[2][i]  # Crr p(room card owned by revealor)
        if Crr == 0 and Ccr == 0 and Cwr == 0:
            zai = 0.0001
            Crr, Ccr, Cwr = zai, zai, zai

        denominator = self.denominator(Crr, Ccr, Cwr)

        # update revealor first
        numerators_revealor = self.numerator_revealor([Crr, Ccr, Cwr])
        data_revealor = list(map(lambda x: float(x) / denominator, numerators_revealor))
        for x in range(3):
            new_lines[x][i] = data_revealor[x]  # replace revealor data in new line

        # update other players
        for x in range(i + 1, i + self.n):
            player_i = x % self.n
            if player_i == self.num:  # no need to update myself
                continue
            elif player_i == s_i:  # stop at suggestor
                break
            player_card_data = [old_lines[0][player_i], old_lines[1][player_i], old_lines[2][player_i]]
            player_numerators = self.numerators_other_players([Crr, Ccr, Cwr], player_card_data)
            data_player = list(map(lambda x: float(x) / denominator, player_numerators))
            for x in range(3):
                new_lines[x][player_i] = data_player[x]
        self.room_p_table[suggestion[0].num] = new_lines[0]
        self.character_p_table[suggestion[1].num] = new_lines[1]
        self.weapon_p_table[suggestion[2].num] = new_lines[2]

    def denominator(self, Crr, Ccr, Cwr):
        return Crr + Ccr + Cwr - Crr * Ccr - Crr * Cwr - Ccr * Cwr + Crr * Ccr * Cwr

    def numerator_revealor(self, revealor_data):
        # print(revealor_data)
        numerator_result = []
        for i in range(3):
            line1 = list(
                map(lambda x: x * revealor_data[i], [1, revealor_data[(i + 1) % 3], revealor_data[(i + 2) % 3]]))
            # line 2 finds all the subsets of line1 of length 2, find the product of these subsets, sum them up
            line2 = sum(list(map(lambda x: x[0] * x[1], list(combinations(line1, 2)))))
            line3 = math.prod(line1)
            numerator_result.append(sum(line1) - line2 + line3)
        return numerator_result

    def numerators_other_players(self, revealor_data, player_cards_data):
        numerator_result = []
        for i in range(3):
            line1 = list(map(lambda x: x * player_cards_data[i], revealor_data))
            # line 2 finds all the subsets of line1 of length 2, find the product of these subsets, sum them up
            line2 = sum(list(map(lambda x: x[0] * x[1], list(combinations(line1, 2)))))
            line3 = math.prod(line1)
            numerator_result.append(sum(line1) - line2 + line3)
        return numerator_result

    def flatten_table(self, table_type):  # table_type: str weapon, room, char
        if table_type == "weapon":
            return list(chain.from_iterable(self.weapon_p_table))
        elif table_type == "room":
            return list(chain.from_iterable(self.room_p_table))
        else:
            return list(chain.from_iterable(self.character_p_table))

    def __str__(self):
        return self.character.get_name()
