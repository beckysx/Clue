from Vertex import *
from Card import *
from Player import *
import numpy as np
from scipy import sparse
import networkx as nx


def blank_exist(x, y):  # check blank exist, used for generate blank vertices
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


class Board(object):
    def __init__(self, room_names, character_names, players):
        room_vertices = [Room(room_name) for room_name in room_names.keys()]
        start_vertices = [GreenStart(char_name) for char_name in character_names.keys()]
        blank_vertices = self.generate_blank_vertices()
        # handle vertices, add neighbors to all vertices
        room_vertices, blank_vertices = self.neighbors_for_rooms(room_vertices, blank_vertices,
                                                                 room_names)  # neighbors for all rooms
        start_vertices, blank_vertices = self.neighbors_for_starts(start_vertices, blank_vertices,
                                                                   character_names)  # neighbors for all starts
        blank_vertices = self.neighbors_for_blanks(blank_vertices)
        self.vertices = np.array(room_vertices + start_vertices + blank_vertices)
        self.players = players
        self.players_set_up()
        self.ad_matrix = None

    def generate_blank_vertices(self):  # generate all blank vertices
        blank_vertices = []
        for y in range(23):
            for x in range(22):
                if blank_exist(x, y):
                    blank_vertices.append(Blank(x, y))
        blank_vertices.append(Blank(6, 23))
        blank_vertices.append(Blank(22, 6))
        return blank_vertices

    def neighbors_for_rooms(self, room_vertices, blank_vertices, room_names):
        for room_vertex in room_vertices:
            doors = room_names.get(room_vertex.get_label())
            for door in doors:
                if type(door) == list:
                    door_vertex = self.getV_label(self.coor_to_label(door), blank_vertices)
                else:
                    door_vertex = self.getV_label(door, room_vertices)
                room_vertex.add_neighbor(door_vertex)
            room_vertex.copy_neighbors()
        return room_vertices, blank_vertices

    def neighbors_for_starts(self, start_vertices, blank_vertices, character_names):
        for k, v in character_names.items():
            label = "Start_" + k
            neighor_coor = v[1]
            blank_vertex = self.getV_label(self.coor_to_label(neighor_coor), blank_vertices)
            start_vertex = self.getV_label(label, start_vertices)
            start_vertex.add_neighbor(blank_vertex)
            start_vertex.copy_neighbors()

        return start_vertices, blank_vertices

    def neighbors_for_blanks(self, blank_vertices):
        for vertex in blank_vertices:
            coor = vertex.get_coor()
            x, y = coor[0], coor[1]
            check_list = [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]
            for check in check_list:
                if blank_exist(check[0], check[1]):
                    vertex.add_neighbor(self.getV_label(self.coor_to_label(check), blank_vertices))
            vertex.copy_neighbors()

        return blank_vertices

    def coor_to_label(self,
                      coordinate):  # turn a length 2 list into blank vertex label, use to conveniently add neighbors
        return "Blank_" + str(coordinate[0]) + "_" + str(coordinate[1])

    def players_set_up(self):
        for player in self.players:
            start_position = self.getV_label("Start_" + player.get_name(), self.vertices)
            self.player_moveto_v(player, start_position)

    def getV_label(self, v_label, v_list):
        for v in v_list:
            if v.label == v_label:
                return v
        return False

    def getV_vertex(self, v, v_list):
        for vertex in v_list:
            if vertex == v:
                return vertex

    def player_moveto_index(self, i, new_location):
        self.players[i].change_location(new_location)

    def player_moveto_v(self, player, new_location):
        player.change_location(new_location)

    def get_v_index(self, v):
        return np.where(self.vertices == v)[0][0]

    def create_adjacency_matrix(self):
        num_v = len(self.vertices)
        ad_matrix = np.zeros((num_v, num_v))
        for i in range(num_v):
            neighbors = self.vertices[i].current_neighbors
            for neighbor in neighbors:
                j = self.get_v_index(neighbor)
                ad_matrix[i][j] = 1
        ad_matrix = sparse.csr_matrix(ad_matrix)
        self.ad_matrix = ad_matrix

    def get_can_reach(self, player_i, step):  # 记得call前创建ad_matrix
        player_curr_index = self.get_v_index(self.players[player_i].curr_location)
        can_reach = self.ad_matrix.getrow(player_curr_index)
        if step > 1:
            for i in range(step - 1):
                can_reach = can_reach.dot(self.ad_matrix)
        can_reach = can_reach.toarray()
        result = []
        for i in range(len(can_reach[0])):
            if can_reach[0][i] != 0:
                result.append(self.vertices[i])
        return result

    def shortest_path(self, start, targets):
        # target probably is a list of string of rooms (self.p_rooms)
        # 记得call前创建ad_matrix
        G = nx.from_numpy_array(self.ad_matrix)
        start_i = self.get_v_index(start)
        path_dictionary = dict.fromkeys(targets, [])
        for room in targets:
            room_i = self.get_v_index(self.getV_label(room))
            minPath = nx.dijkstra_path(G, source=start_i, target=room_i, weight=1)
            path_dictionary[room] = [self.vertices[minPath[i]] for i in range(1, 1, len(minPath))]
        return path_dictionary

    # def add_edge(self, vertex_from, vertex_to):
    # if isinstance(vertex_from, Vertex) and isinstance(vertex_to, Vertex):
    # vertex_from.add_neighbor(vertex_to)

    # if isinstance(vertex_from, Vertex) and isinstance(vertex_to, Vertex):
    # self.vertices[vertex_from.coordinate] = vertex_from.neighbors
    # self.vertices[vertex_to.coordinate] = vertex_to.neighbors

    # def add_edges(self, edges):
    # for edge in edges:
    # self.add_edge(edge[0], edge[1])
