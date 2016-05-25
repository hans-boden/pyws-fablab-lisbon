# python3
"""
    This is a solver for the Towers-of-Hanoi puzzle

    The module can be imported. Then the call to the solver() function must
    provide a queue, where the steps of the solution are inserted.
    The module can be run as a main program. Then there is a dummy queue,
    which just prints out the inserted moves.
"""

class G():
    queue = None  # command queue
    idtab = {}    # table of names and column numbers
    
def solver(queue):
    G.queue = queue

    a, b, c = [7,6,5,4,3,2,1], [], []
    G.idtab = {id(a): ('A',0), id(b): ('B',1), id(c): ('C',2)}

    move_better(a, c, b, len(a))
    # print the final columns
    for col in (a,b,c):
        cid, cnr = G.idtab[id(col)]
        print("col {}({}): {}".format(cid, cnr, col))

def move_better(src, trg, tmp, depth):
    if depth > 1:
        move_better(src, tmp, trg, depth-1)

    disk = src.pop()
    record(disk, src, trg)
    trg.append(disk)

    if depth > 1:
        move_better(tmp, trg, src, depth-1)

def record(disk, src, trg):
    # protocol of individual moves: write to command queue
    sname, scol = G.idtab[id(src)]  # for printing only
    tname, tcol = G.idtab[id(trg)]
    print("move {} from {} to {}".format(disk, sname, tname))  # optional print
    G.queue.put("disk{} {} {lvl}".format(disk, tcol, lvl=len(trg)))

class DummyQueue():
    # fake the "Queue" class, providing the 'put()' method, which is the only
    # method needed for the local application.
    def put(self, string):
        print("dummyQ: {}".format(string))

if __name__ == '__main__':
    dq = DummyQueue()  # this is "duck typing" - provide some object, which behaves
    solver(dq)

