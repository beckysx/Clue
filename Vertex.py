class Vertex(object):
    def __init__(self):
        self.occupied = False
        self.original_neighbors = []
        self.current_neighbors = []
        self.label = None

    def add_neighbor(self, neighbor):
        if neighbor not in self.original_neighbors:
            self.original_neighbors.append(neighbor)
            neighbor.original_neighbors.append(self)

    def add_neighbors(self, neighbors):
        for neighbor in neighbors:
            if neighbor.label not in self.original_neighbors:
                self.original_neighbors.append(neighbor)
                neighbor.original_neighbors.append(self)

    def copy_neighbors(self):
        self.current_neighbors = self.original_neighbors.copy()

    def delete_neighbor(self, neighbor):
        self.current_neighbors.remove(neighbor)

    def occupy(self):
        self.occupied = True
        for neighbor in self.original_neighbors:
            neighbor.copy_neighbors()
            neighbor.delete_neighbor(self)

    def de_occupy(self):
        self.occupied = False
        for neighbor in self.neighbors:
            neighbor.copy_neighbors()

    def __eq__(self, other):
        return self.label == other.label

    def get_label(self):
        return self.label

    def __str__(self):
        neighbors = [neighbor.get_lable() for neighbor in self.original_neighbors]
        return [self.label].append(neighbors)


class Blank(Vertex):
    def __init__(self, x, y):
        self.coordinate = [x, y]
        self.label = "Blank_" + str(x) + "_" + str(y)
        self.category = "Blank"

    def get_coor(self):
        return self.coordinate


class GreenStart(Vertex):
    def __init__(self, char_name):
        self.label = "Start_" + char_name
        self.category = "Start"


class Room(Vertex):
    def __init__(self, room_name):
        self.label = room_name
        self.category = "Room"
