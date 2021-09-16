class Card(object):
    def __init__(self, category, name, image):
        self.category = category
        self.name = name
        self.image = image


class Weapon(Card):
    def __init__(self, name, image):
        self.category = 'weapon'
        self.name = name
        self.image = image


class Character(Card):
    def __init__(self, name, image):
        self.category = 'character'
        self.name = name
        self.image = image


class Room(Card):
    def __init__(self, name, image, door_list, secrete_pass=False):
        self.category = 'room'
        self.name = name
        self.image = image
        self.door_list = door_list
        self.secrete_pass = secrete_pass
        self.occupied = False
        self.blocked = False

    def check_blocked(self):
        return self.blocked

    def check_occupied(self):
        return self.occupied

    def change_occupied(self):
        self.occupied = not self.occupied

    def change_blocked(self):
        self.blocked = not self.blocked
