# python3

import random

list_of_cities = """
Beijing, Shanghai, Lagos, Delhi, Istanbul, Tokyo, Moscow, Mumbai, Sao Paulo, Jakarta,
Seoul, Cairo, Mexico City, Lima, London, New York, Bangkok, Nanjing, Teheran, Bogota,
Hong Kong, Hanoi, Baghdad, Rio de Janeiro, Santiago, Rijadh, Singapore, St. Petersburg,
Chennai, Alexandria, Lisbon, Berlin, Madrid, Paris, Rome, Athens, Ankara, Amsterdam,
Johannesburg, Taipei, Los Angeles, Durban, Kyoto, Casablanca, Nairobi, Buenos Aires,
Chicago, Helsinki, Sidney, Manila, Cape Town, Washington, San Francisco, Havanna
"""
list_of_doors = ((3,0,3,2,1,2),
                 (3,1,0,3,1,2),
                 (2,1,1,1,2,2),
                 (2,1,3,1,0,2),
                 (3,1,1,3,1,0),
                 (1,1,0,1,1,0))

def main():
    matrix = make_matrix()
    define_doors(matrix)
    matrix[5][5].door(Room('Exit'), False)
    write_room_plan(matrix)

    print_matrix()

def write_room_plan(matrix):
    fn = r'data\mad_hotel_rooms.txt'

    with open(fn, mode='w', encoding='utf-8') as fo:
        def print(x):
            fo.write(x+'\n')
        print("#   You are in room: {}".format(matrix[2][2].name))
        print("#   The exit is from room: {}".format(matrix[5][5].name))
        print("#   Every room has one or more doors of different colors")
        print("#   This is the room plan:")
        rooms = []
        for row in matrix:
            for room in row:
                rooms.append((room.name, room))
        for name, room in sorted(rooms):
            print("\nRoom: {}".format(room.name))
            for color, neighbor in room.doors:
                print("    {} door ==> {}".format(color, neighbor.name))


def print_matrix():
    for row in list_of_doors:
        print('\n   ', end='')
        for doors in row:
            if doors & 1:
                print("O---", end='')
            else:
                print("O   ", end='')
        print('\n   ', end='')
        for doors in row:
            if doors & 2:
                print("|   ", end='')
            else:
                print("    ", end='')

def make_matrix():
    cities = gen_city_names()
    mat = [[Room(next(cities)) for x in range(6)] for y in range(6)]
    return mat

def gen_city_names():
    cities = [x.strip() for x in list_of_cities.split(',')]
    nodups = set()
    for name in cities:
        if name in nodups:
            print("duplicate", name)
        else:
            nodups.add(name)

    random.shuffle(cities)
    for name in cities:
        yield name

def define_doors(mat):
    for y in range(6):
        for x in range(6):
            doors = list_of_doors[y][x]
            room = mat[y][x]
            if doors & 1:
                room.door(mat[y][x+1])
            if doors & 2:
                room.door(mat[y+1][x])

class Room():
    def __init__(self, name):
        self.name = name
        self.doors = []
        self.colors = "black white green red blue".split()

    def door(self, neighbor, reversed=True):
        color = self.colors.pop(random.randrange(len(self.colors)))
        self.doors.append((color, neighbor))
        if reversed:
            neighbor.door(self, False)

main()
