from Card import *
from Player import *
import random
from Board import *


class Clue(object):
    def __init__(self, n, weapons, room_names, character_names):
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
        players.sort()
        self.players = players
        self.players_set_up()
        self.board = Board(room_names, character_names, players)
        result = self.board.get_can_reach(0, 4)


    def blank_exist(self, x, y):  # check blank exist, used for generate blank vertices
        if x < 0 or x > 21 or y < 0 or y > 22:
            return False
        elif y == 0:
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

    def players_set_up(self):
        if len(self.players) < 6:
            for player in self.players:
                order_in_game = self.players.index(player)
                if player.get_num() != order_in_game:
                    player.change_num(order_in_game)
