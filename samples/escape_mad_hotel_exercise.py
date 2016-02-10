# python3
"""
    read the flor plan of the mad hotel
    find a way (the shortest) from the current position to the exit
"""

floor_file = 'data\\mad_hotel_rooms.txt'

def main():
    room_plan = get_room_plan()
    print("Try to escape from the mad hotel")
    answer = input("In which room are you now? ").strip().lower()
    if not answer in room_plan:
        print("Room '{}' is not known, sorry".format(answer))
        return

    way_out = find_exit(room_plan, from_room=answer)
    if not way_out:
        print("Sorry, no way out found, you are lost")
        return

    print("follow this way:")
    for color, name in way_out:
        print("{} door, leads to room: {}".format(color, name))

    print("Congratulations, you reached the Exit")


def find_exit(plan, from_room, moreparms=True):
    return []


def get_room_plan():
    known_rooms = {}
    known_rooms['exit'] = Room('exit')  # for a soft landing

    for item, name in get_rooms_and_doors():
        if item == 'room':
            room = known_rooms.get(name, None)
            if room is None:
                room = Room(name)
                known_rooms[name.lower()] = room
            continue
        color = item
        room.add_door(color, name.lower())
    return known_rooms

def get_rooms_and_doors():
    with open(floor_file) as fi:
        for line in fi:
            line = line.split('#')[0].strip()
            if line == '':  # skip empty lines and comment lines
                continue

            if line.startswith('Room'):
                room_name = line.split(None,1)[1]
                yield 'room', room_name
                continue
            # other lines should be doors...
            color, txt, _, name = line.split(None,3)
            assert txt == 'door'
            yield color, name

class Room():
    def __init__(self, room_name):
        self.name = room_name
        self.doors = []

    def add_door(self, color, other_room):
        self.doors.append((color, other_room))


main()
