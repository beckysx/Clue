import math


class Card(object):
    def __init__(self, name, num, image):
        self.category = None
        self.name = name
        self.image = image
        self.have_shown = False
        self.num = num

    def __eq__(self, other):
        return self.name == other.name

    def get_category(self):
        return self.category

    def get_name(self):
        return self.name

    def isRoom(self):
        return self.category == 'room'

    def isWeapon(self):
        return self.category == 'weapon'

    def isChar(self):
        return self.category == 'character'

    def delete_from(self, card_list):
        for c in card_list:
            if self.name == c.name:
                card_list.remove(c)
                return card_list
        return card_list

    def __str__(self):
        return self.name


class Weapon(Card):
    def __init__(self, name, num, image=None):
        super().__init__(name, num, image)
        self.category = 'weapon'


class Character(Card):
    def __init__(self, name, num, image=None):
        super().__init__(name, num, image)
        self.category = 'character'

    def __lt__(self, other):
        return self.num < other.num

    def get_num(self):
        return self.num


class Room_card(Card):
    def __init__(self, name, num, image=None):
        super().__init__(name, num, image)
        self.category = 'room'
        self.distance = math.inf

    def __lt__(self, other):
        return self.distance < other.distance
