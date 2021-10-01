from Vertex import *
from Card import *
from Player import *


class Board(object):
    def __init__(self, V, player_list):  # char list is  list of player
        self.vertices = V
        self.player_order = player_list.sort()
        self.players_set_up()

    def players_set_up(self):
        if len(self.player_order) < 6:
            for player in self.player_order:
                order_in_game = self.player_order.index(player)
                if player.get_num() != order_in_game:
                    player.change_num(order_in_game)
                start_position = self.getV("Start_" + player.get_name())
                player.change_location(start_position)
                start_position.occupy()
        else:
            for player in self.player_order:
                start_position = self.getV("Start_" + player.get_name())
                player.change_location(start_position)
                start_position.occupy()

    def getV(self, v_label):
        for v in self.vertices:
            if v.label == v_label:
                return v
        return False

    def getV(self, v):
        for vertex in self.vertices:
            if vertex == v:
                return vertex

    def add_record(self, char, position):  # occupy new positon and de_occupy old one
        char_record = self.moving_record[char.get_num()]
        if len(char_record) < 2:
            char_record

    # def add_edge(self, vertex_from, vertex_to):
    # if isinstance(vertex_from, Vertex) and isinstance(vertex_to, Vertex):
    # vertex_from.add_neighbor(vertex_to)

    # if isinstance(vertex_from, Vertex) and isinstance(vertex_to, Vertex):
    # self.vertices[vertex_from.coordinate] = vertex_from.neighbors
    # self.vertices[vertex_to.coordinate] = vertex_to.neighbors

    # def add_edges(self, edges):
    # for edge in edges:
    # self.add_edge(edge[0], edge[1])
