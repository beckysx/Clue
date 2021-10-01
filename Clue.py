from Card import *
from Player import *
import random
from Board import *


class Clue(object):
    def __init__(self, n, weapons, room_names, character_names):
        room_vertices = [Room(room_name) for room_name in room_names.keys()]
        start_vertices = [GreenStart(char_name) for char_name in character_names.keys()]
        blank_vertices = self.generate_blank_vertices()
        room_cards = [Room_card(room_name) for room_name in room_names]
        char_cards = [Character(name=k, num=v[0]) for k, v in character_names.items()]
        weapon_cards = [Weapon(weapon) for weapon in weapons]
        # handle cards, generate players
        self.all_cards = weapon_cards + room_cards + char_cards
        self.real_answer = [random.choice(char_cards), random.choice(weapon_cards), random.choice(room_cards)]
        random_n_characters = random.sample(char_cards, n)  # randomly choose n characters as agents
        self.fake_cards = self.get_fake_cards()
        card_piles = self.distribute_cards(n)
        players = self.generate_players(random_n_characters, card_piles)
        # handle vertices, add neighbors to all vertices
        room_vertices, blank_vertices = self.neighbors_for_rooms(room_vertices, blank_vertices,
                                                                 room_names)  # neighbors for all rooms
        start_vertices, blank_vertices = self.neighbors_for_starts(start_vertices, blank_vertices,
                                                                   character_names)  # neighbors for all starts
        blank_vertices = self.neighbors_for_blanks(blank_vertices)
        V = room_vertices + start_vertices + blank_vertices
        for i in range(5):
            print(V[i])
        #self.board = Board(V, players)

    def blank_exist(self, x, y):  # check blank exist, used for generate blank vertices
        if y == 0:
            if 0 <= x <= 5 or 9 <= x <= 12 or 16 <= x <= 21:
                return False
        elif y == 1 or y == 2 or y == 3:
            if 0 <= x <= 4 or 7 <= x <= 14 or 17 <= x <= 21:
                return False
        elif y == 4:
            if 0 <= x <= 3 or 7 <= x <= 14 or 17 <= x <= 21:
                return False
        elif y == 5:
            if 7 <= x <= 14 or 17 <= x <= 21:
                return False
        elif y == 6:
            if 7 <= x <= 14:
                return False
        elif y == 7:
            if 0 <= x <= 4:
                return False
        elif y == 8:
            if 0 <= x <= 4 or 18 <= x <= 21:
                return False
        elif y == 9 or y == 10 or y == 11 or y == 13:
            if 0 <= x <= 4 or 8 <= x <= 12 or 15 <= x <= 21:
                return False
        elif y == 12:
            if 8 <= x <= 12 or 15 <= x <= 21:
                return False
        elif y == 14:
            if 0 <= x <= 5 or 8 <= x <= 12 or 15 <= x <= 21:
                return False
        elif y == 15:
            if 0 <= x <= 5 or 8 <= x <= 12:
                return False
        elif y == 16:
            if 0 <= x <= 5:
                return False
        elif y == 17:
            if 0 <= x <= 4 or 8 <= x <= 13:
                return False
        elif y == 18 or y == 19:
            if 8 <= x <= 13 or 16 <= x <= 21:
                return False
        elif y == 20 or y == 21 or y == 22:
            if 0 <= x <= 5 or 8 <= x <= 13 or 16 <= x <= 21:
                return False
        else:
            return True

    def generate_blank_vertices(self):  # generate all blank vertices
        blank_vertices = []
        for y in range(23):
            for x in range(22):
                if self.blank_exist(x, y):
                    blank_vertices.append(Blank(x, y))
        blank_vertices.append(Blank(6, 23))
        blank_vertices.append(Blank(22, 6))

        return blank_vertices

    def coor_to_label(self,
                      coordinate):  # turn a length 2 list into blank vertex label, use to conveniently add neighbors
        return "Blank_" + coordinate[0] + "_" + coordinate[1]

    def getV(self, v_label, v_list):
        for v in v_list:
            if v.label == v_label:
                return v
        return False

    def getV(self, v, v_list):
        for vertex in v_list:
            if vertex == v:
                return vertex

    def get_fake_cards(self):  # exclude real answer, card that need to give to players
        return [card for card in self.all_cards if card not in self.real_answer]

    def distribute_cards(self, n):  # distribute fake cards to all players
        random.shuffle(self.fake_cards)
        card_piles = [[] for i in range(n)]
        for i in range(len(self.fake_cards)):
            card_piles[i % n].append(self.fake_cards[i])
        return card_piles

    def generate_players(self, char_list, card_piles):  # generate all players
        player_list = []
        for i in range(len(char_list)):
            player_list.append(Player(char_list[i], card_piles[i], self.all_cards))
        return player_list

    def neighbors_for_rooms(self, room_vertices, blank_vertices, room_names):
        for room_vertex in room_vertices:
            doors = room_names.get(room_vertex.get_label)
            for door in doors:
                door_vertex = self.getV(self.coor_to_label(door), blank_vertices)
                room_vertex.add_neighbor(door_vertex)
        return room_vertices, blank_vertices

    def neighbors_for_starts(self, start_vertices, blank_vertices, character_names):
        for k, v in character_names.items():
            label = "Start_" + k
            neighor_coor = v[1]
            blank_vertex = self.getV(self.coor_to_label(neighor_coor), blank_vertices)
            self.getV(label, start_vertices).add_neighbor(blank_vertex)
        return start_vertices, blank_vertices

    def neighbors_for_blanks(self, blank_vertices):
        for vertex in blank_vertices:
            coor = vertex.get_coor()
            x, y = coor[0], coor[1]
            check_list = [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]
            for check in check_list:
                if self.blank_exist(check[0], check[1]):
                    vertex.add_neighbor(self.getV(self.coor_to_label(check), blank_vertices))

        return blank_vertices
