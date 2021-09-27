from Vertex import Room, Blank, GreenStart


def blank_exist(x, y):
    match y:
        case 0:
            if 0 <= x <= 5 or 9 <= x <= 12 or 16 <= x <= 21:
                return False
        case 1 | 2 | 3:
            if 0 <= x <= 4 or 7 <= x <= 14 or 17 <= x <= 21:
                return False
        case 4:
            if 0 <= x <= 3 or 7 <= x <= 14 or 17 <= x <= 21:
                return False
        case 5:
            if 7 <= x <= 14 or 17 <= x <= 21:
                return False
        case 6:
            if 7 <= x <= 14:
                return False
        case 7:
            if 0 <= x <= 4:
                return False
        case 8:
            if 0 <= x <= 4 or 18 <= x <= 21:
                return False
        case 9 | 10 | 11 | 13:
            if 0 <= x <= 4 or 8 <= x <= 12 or 15 <= x <= 21:
                return False
        case 12:
            if 8 <= x <= 12 or 15 <= x <= 21:
                return False
        case 14:
            if 0 <= x <= 5 or 8 <= x <= 12 or 15 <= x <= 21:
                return False
        case 15:
            if 0 <= x <= 5 or 8 <= x <= 12:
                return False
        case 16:
            if 0 <= x <= 5:
                return False
        case 17:
            if 0 <= x <= 4 or 8 <= x <= 13:
                return False
        case 18 | 19:
            if 8 <= x <= 13 or 16 <= x <= 21:
                return False
        case 20 | 21 | 22:
            if 0 <= x <= 5 or 8 <= x <= 13 or 16 <= x <= 21:
                return False
    return True


def generate_blank_vertices():
    blank_vertices = []
    for y in range(23):
        for x in range(22):
            if blank_exist(x, y):
                blank_vertices.append(Blank(x, y))
    return blank_vertices


if __name__ == '__main__':
    room_names = ["Ballroom", "Kitchen", "Conservatory", "Billiard", "Library", "Dining", "Study", "Hall", "Lounge"]
    character_names = ["Mr.Green", "Mrs.White", "Col.Mustard", "Prof.Plum", "Miss.Scarlett", "Mrs.Peacock"]
    weapon = ["Candlestick", "Dagger", "Lead_Pipe", "Revolver", "Rope", "Wrench"]
    room_vertices = [Room(room_name) for room_name in room_names]
    start_vertices = [GreenStart(char_name) for char_name in character_names]
    blank_vertices = generate_blank_vertices()
