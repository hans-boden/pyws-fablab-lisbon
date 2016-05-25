"""
    show some class basics
"""

class Room():
    def __init__(self, name):
        self.name = name
        self.neighbors = []

    def add_room(self, other_room):
        self.neighbors.append(other_room)


fn = r"c:\path1\path2\mad_hotel_room.txt"
fn = "c:\\path1\\path2\\mad_hotel_room.txt"
fn = "c:/path1/path2/mad_hotel_room.txt"

fi = open(fn)
for line in fi:

    print(line, end='')
    
    line = line.rstrip() # strip newlines !
    if line == '':
        continue
    if line[0] == '#':
        continue

    if line[0] != ' ':  # this is a room name
        name = line.split(None, 1)[1]
        # do something
        # create a room object
        # save it as the last room object
        continue

    # this is a room line
    tup = line.split(None,3)
    color, _, _, nbr = tup

    # add this name to the 'last saved'
    
    

    
        

mumbay = Room("Mumbay")
paris  = Room("Paris")
lisbon = Room("Lisbon")

mumbay.add_room(lisbon)
mumbay.add_room(paris)

for nbr in mumbay.neighbors:
    print(nbr.name)

a = [1,2,3]
for what_t_f_is_this in a:
    print(what_t_f_is_this)
print([x.name for x in mumbay.neighbors])

