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
    def __init__(self, name, image):
        self.category = 'weapon'
        self.name = name
        self.image = image


class Character(Card):
    def __init__(self, name, image):
        self.category = 'character'
        self.name = name
        self.image = image

class Room_card(Card):
    def __init__(self, name, image):
        self.category = 'room'
        self.name = name
        self.image = image