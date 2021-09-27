import Card
class Player(object):
    def __init__(self, char_card, own_card_list, all_cards):
        self.character = char_card
        self.status = True  # active
        self.in_room = False
        self.can_rowdice = True
        self.can_suggest = False
        self.cards_have = own_card_list
        self.p_weapons, self.im_weapons = [], []
        self.p_rooms, self.im_rooms = [], []
        self.p_characters, self.im_characters = [], []
        for card in all_cards:
            match card.category():
                case "weapon":
                    if card in own_card_list:
                        self.p_weapons.append(card)
                    else:
                        self.im_weapons.append(card)
                case "room":
                    if card in own_card_list:
                        self.p_rooms.append(card)
                    else:
                        self.im_rooms.append(card)
                case "character":
                    if card in own_card_list:
                        self.p_characters.append(card)
                    else:
                        self.im_characters.append(card)
            



