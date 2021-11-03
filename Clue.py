from Card import *
from Player import *
import random
from Board import *


class Clue(object):
    def __init__(self, n, weapons, room_names, character_names):
        self.n = n
        room_cards, char_cards, weapon_cards = self.set_up_cards(weapons, room_names, character_names)

        # handle cards, generate players
        self.all_cards = weapon_cards + room_cards + char_cards
        self.room_cards = room_cards
        self.real_answer = [random.choice(room_cards), random.choice(char_cards), random.choice(weapon_cards)]
        self.Y = None
        self.X = [[] for i in range(3)]
        self.set_Y(self.real_answer)
        print("real answer:")
        self.print_cardlist(self.real_answer)
        random_n_characters = random.sample(char_cards, n)  # randomly choose n characters as agents
        self.fake_cards = self.get_fake_cards()
        card_piles = self.distribute_cards(n)
        players = self.generate_players(random_n_characters, card_piles)
        self.players = players
        print("players:")
        self.print_cardlist(self.players)
        self.board = Board(room_names, character_names, players)
        self.players_set_up()
        self.status = True  # no one win

    def set_Y(self, real_answer):
        Yr, Yc, Yw = [0 for i in range(9)], [0 for i in range(6)], [0 for i in range(6)]
        Y = [Yr, Yc, Yw]
        for i in range(3):
            Y[i][real_answer[i].num] = 1
        self.Y = Y

    def get_Y(self):
        return self.Y

    def set_up_cards(self, weapons, room_names, char_names):
        char_cards = [Character(name=k, num=v[0]) for k, v in char_names.items()]
        weapon_cards = [Weapon(name=k, num=v) for k, v in weapons.items()]
        room_cards = []
        i = 0
        for room_name in room_names:
            room_cards.append(Room_card(name=room_name, num=i))
            i += 1
        return room_cards, char_cards, weapon_cards

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
            player_list.append(Player(char_list[i], card_piles[i], self.n))
        player_list.sort()
        return player_list

    def players_set_up(self):
        if len(self.players) < 6:
            for player in self.players:
                order_in_game = self.players.index(player)
                player.change_num(order_in_game)
        for player in self.players:
            self.player_move_to(player, "Start_" + player.get_name())
            player.player_set_up(self.all_cards, self.n)

    def accusation_process(self, player, combination):
        if self.answer_check(combination):
            print(str(player) + " win")
            self.status = False
            return True
        print(str(player) + " lost")
        return False

    def answer_check(self, combination):  # match the accusation with real answer
        for i in range(3):
            if combination[i].name != self.real_answer[i].name:
                return False
        self.status = False
        return True

    def find_room_card(self, card_label):
        for card in self.room_cards:
            if card.name == card_label:
                return card

    def player_move_to(self, player, position_name):
        current_position = player.curr_location
        new_position = self.board.getV_label(position_name, self.board.vertices)
        player.move_to(new_position)
        self.board.player_moveto(current_position, new_position)

    def seggestion_move(self, suggestion):  # suggestion = [room, person, weapon]
        room_name = suggestion[0].get_name()
        for player in self.players:
            if player.character == suggestion[1] and player.curr_location.get_label != room_name:
                self.player_move_to(player, room_name)

    def disprove_process(self, player, suggestion):
        i = player.get_num()
        for x in range(i + 1, i + self.n):
            player_i = x % self.n
            card = self.players[player_i].disprove(suggestion)
            print(self.players[player_i].get_name() + " show " + player.get_name() + str(card))
            if card is not None:
                self.players[i].elliminate(card, self.players[player_i])
                for y in range(player_i, player_i + self.n):
                    update_i = x % self.n
                    self.players[update_i].conditional_probability(suggestion, self.players[update_i], player)
                self.append_X()  # save X data
                return True
            for player in self.players:
                player.zero_out_vertical(suggestion, self.players[player_i])
        return False

    def row_die(self):
        return random.randint(1, 6)

    def suggestion_update(self, suggestion, suggestor):  # add number of times mentioned by player for each card
        for player in self.players:
            player.suggestion_update(suggestion)  # update time mentions
            player.zero_out_vertical(suggestion, suggestor)  # suggestor doesn't have these cards

    def game_still_active(self):  # check if still have players active or not
        for i in range(self.n):
            if self.players[i].isActive():
                return True
        self.status = False
        return False

    def one_turn(self, turn_num):
        for player in self.players:
            print(player.character.name + "'s turn:")
            curr_place = player.curr_location
            secrete_pass = self.board.have_secrete_pass(curr_place)
            if not player.isActive():
                continue
            # 四个选择[stay make suggestion, secrete pass, accusation, dice]
            elif player.only_one_combination():  # make accusation
                accusation = player.make_accusation()
                print("Accusation: ")
                self.suggestion_update(accusation, player)
                self.print_cardlist(accusation)
                if self.accusation_process(player, accusation):
                    return
            elif player.can_make_suggest():  # make suggestion
                room_card = self.find_room_card(curr_place.get_label())
                suggestion = player.make_suggestion(room_card)  # suggestion = [room, person, weapon]

            elif player.is_p_room(secrete_pass):  # use secrete pass, give suggestion
                self.player_move_to(player, secrete_pass)
                room_card = self.find_room_card(curr_place.get_label())
                suggestion = player.make_suggestion(room_card)
            else:  # use dice, if a room give suggestion
                step = self.row_die()
                print("row die get:" + str(step) + " steps")
                reachable_vertices, sorted_rooms, path_dictionary = self.board.get_reachable_vertex(player, step)
                player.update_room_distance(path_dictionary)
                for room in sorted_rooms:
                    if player.is_p_room(room.get_name()):
                        new_position = reachable_vertices[room.get_name()]
                        if new_position is not None:
                            self.player_move_to(player, new_position.get_label())
                            break
                if player.curr_location.isRoom():  # new position is room
                    room_card = self.find_room_card(player.curr_location.get_label())
                    suggestion = player.make_suggestion(room_card)
                else:  # new position not room
                    print("move to blank")
                    continue
            # records num of times mentioned in suggestion
            print("real answer:")
            self.print_cardlist(self.real_answer)
            print("suggestion:")
            self.print_cardlist(suggestion)
            self.suggestion_update(suggestion, player)
            self.seggestion_move(suggestion)
            disprove = self.disprove_process(player, suggestion)
            if disprove:
                if player.only_one_combination():  # make accusation
                    accusation = player.make_accusation()
                    self.suggestion_update(accusation, player)
                    print("Accusation: ")
                    self.print_cardlist(accusation)
                    if self.accusation_process(player, accusation):
                        return
            else:
                accusation = player.make_accusation(suggestion)
                self.suggestion_update(accusation, player)
                print("Accusation: ")
                self.print_cardlist(accusation)
                if self.accusation_process(player, accusation):
                    return
            if not self.game_still_active():
                return

    def cardlist_to_label(self, card_list):
        return [card.get_name() for card in card_list]

    def print_cardlist(self, card_list):
        print(*card_list, sep=", ")

    def append_X(self):
        for player in self.players:
            self.X[0].append(player.flatten_table("room"))
            self.X[1].append(player.flatten_table("char"))
            self.X[2].append(player.flatten_table("weapon"))

    def get_X(self):
        return self.X
