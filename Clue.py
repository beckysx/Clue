from Card import *
from Player import *
import random
from Board import *


class Clue(object):
    def __init__(self, n, weapons, rooms, characters, V):
        self.all_cards = weapons + rooms + characters
        self.real_answer = [random.choice(characters), random.choice(weapons), random.choice(rooms)]
        random_n_characters = random.sample(characters, n)
        self.fake_cards = self.get_fake_cards()
        card_piles = self.distribute_cards(n)
        players = self.generate_players(random_n_characters, card_piles)
        self.board = Board(V, players)

    def get_fake_cards(self):
        return [card for card in self.all_cards if card not in self.real_answer]

    def distribute_cards(self, n):
        self.fake_cards = random.shuffle(self.fake_cards)
        card_piles = [[] for i in range(n)]
        for i in range(len(self.fake_cards)):
            card_piles[i % n].append(self.fake_cards[i])
        return card_piles

    def generate_players(self, char_list, card_piles):
        player_list = []
        for i in range(len(char_list)):
            player_list.append(Player(char_list[i], card_piles[i], self.all_cards))
        return player_list
