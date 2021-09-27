class Vertex(object):
    def __init__(self):
        self.occupied = False
        self.neighbors = []

    def add_neighbor(self, neighbor):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)
            neighbor.neighbors.append(self)

    def add_neighbors(self, neighbors):
        for neighbor in neighbors:
            if neighbor.label not in self.neighbors:
                self.neighbors.append(neighbor)
                neighbor.neighbors.append(self)

    def occupy(self):
        self.occupied = True
        for neighbor in self.neighbors:
            neighbor.neighbors.remove(self)

    def de_occupy(self):
        self.occupied = False
        for neighbor in self.neighbors:
            neighbor.neighbors.append(self)




class Blank(Vertex):
    def __init__(self, x, y):
        self.coordinate = [x, y]
        self.label = "Blank_" + x + "_" + y


class GreenStart(Vertex):
    def __init__(self, char_name):
        self.label = "Start_" + char_name


class Room(Vertex):
    def __init__(self, room_name):
        self.label = room_name
