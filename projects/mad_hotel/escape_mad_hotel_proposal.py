# python3
"""
    read the flor plan of the mad hotel
    find a way (the shortest) from the current position to the exit
"""

floor_file = 'data\\mad_hotel_rooms.txt'

def main():
    room_plan = get_room_plan()
    allways = {}
    start = "Rijadh"
    target = "Exit"    
    first = room_plan[start.lower()]

    crawl(first, [], allways)

    steps = allways[target.lower()]
    print("from {} to {} in {} steps:".format(start, target, len(steps)))
    for color, room in steps:
        print("use {} door to {}".format(color, room.name))

def crawl(here, myway, allways):
    # follow all doors
    for door, room in here.doors:
        check(room, myway + [(door, room)], allways)
        
def check(here, myway, allways):
    # check if a better way is already known
    key = here.key
    if key in allways:
        if len(myway) >= len(allways[key]):
            return
    allways[key] = myway
    crawl(here, myway, allways)
    

def oldmain():
    room_plan = get_room_plan()
    print("Try to escape from the mad hotel")
    answer = input("In which room are you now? ").strip().lower()
    if not answer in room_plan:
        print("Room '{}' is not known, sorry".format(answer))
        return

    from_room = answer

    way_out = find_exit(room_plan, from_room)

    if way_out is None:
        print("Sorry, no way out found, you are lost")
        return

    print("You have to go thru {} doors".format(len(way_out)-1))
    print("Follow this way:  You are in room ...")
    for color, name in way_out:
        if color:
            print("{:15s}, the {:5s} door, leads to ...".format(name, color))
        else:
            print("... the Exit")

    print("Congratulations, you reached the Exit")


def find_exit(plan, room, visited=set(), lvl=0, moreparms=True):
    print("arrive at {}, lvl={}".format(room, lvl))
    way_out = None
    here = plan[room]

    if here.name == 'exit':
        return [(None, here.name)]
    if id(here) in visited:
        return None
    prev_visits = set(visited)
    prev_visits.add(id(here))

    used_door = None
    for color, there in here.doors:
        print("   lvl={}   use {} door".format(lvl, color))

        result = find_exit(plan, there, visited=prev_visits, lvl=lvl+1)

        print("   lvl={}   {} door returned '{}'".format(lvl, color, result))
        if result is None:
            continue
        if way_out == None:
            way_out = result
            used_door = color
        else:
            if len(result) < len(way_out):
                way_out = result
                used_door = color

    if way_out is not None:
        way_out.insert(0, (used_door, here.name))
    return way_out


def get_room_plan():
    known_rooms = {}
    # get_room(known_rooms, 'Exit')  # for a soft landing

    for item, name in gen_rooms_and_doors():
        if item == 'room':
            room = get_room(known_rooms, name)
            continue
        color = item
        nbr = get_room(known_rooms, name)
        room.add_door(color, nbr)
    return known_rooms

def get_room(map, name):
    # get Room by name, eventually create
    key = name.lower()
    if key in map:
        return map[key]
    room = Room(name)
    map[key] = room
    return room
    

def gen_rooms_and_doors():
    # generator: return names of rooms and doors
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
        self.key = room_name.lower()
        self.doors = []

    def add_door(self, color, other_room):
        # other_room is a room object
        assert type(self) == type(other_room), "only a Room object accepted"
        self.doors.append((color, other_room))

    def __repr__(self):
        return "<Room {}, name:{}, {} doors>".format(id(self), self.name, len(self.doors))


main()
