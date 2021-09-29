class Card(object):
    def __init__(self, category, name, image):
        self.category = category
        self.name = name
        self.image = image

    def __eq__(self, other):
        return self.name == other.name

    def category(self):
        return self.category

    def name(self):
        return self.name


class Weapon(Card):
    def __init__(self, name, image=None):
        self.category = 'weapon'
        self.name = name
        self.image = image


class Character(Card):
    def __init__(self, name, num, image=None):
        self.category = 'character'
        self.name = name
        self.image = image
        self.num = num

    def __lt__(self, other):
        return self.num < other.num

    def change_num(self, num):
        self.num = num

    def get_num(self):
        return self.num

    def get_name(self):
        return self.name


class Room_card(Card):
    def __init__(self, name, image=None):
        self.category = 'room'
        self.name = name
        self.image = image
