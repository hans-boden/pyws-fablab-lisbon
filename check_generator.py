# python3
""" try to find out the internals of a generator """

ignore = ['__abs__', '__add__', '__and__', '__bool__', '__call__',
          '__ceil__', '__class__', '__getitem__', 
          '__del__', '__delattr__', '__dir__', '__divmod__', '__doc__',
          '__eq__', '__float__', '__floor__', '__floordiv__', '__format__',
          '__new__', '__ge__', '__getattribute__',
          '__gt__', '__hash__', '__index__', '__init__', '__int__',
          '__iter__', '__invert__', '__le__', '__len__', '__lshift__', '__lt__', '__mod__', '__mul__',
          '__ne__', '__neg__', '__next__', '__objclass__', '__or__', '__pos__', '__pow__', '__qualname__',
          '__radd__', '__rand__', '__reduce__', '__rdivmod__',
          '__reduce_ex__', '__repr__', '__rfloordiv__', '__rlshift__', '__rmod__',
          '__rmul__', '__ror__', '__rpow__', '__rrshift__', '__rshift__', '__rsub__', '__rtruediv__', '__rxor__',
          '__setattr__', '__sizeof__',
          '__str__', '__sub__', '__subclasshook__', '__truediv__', '__xor__',
          'f_builtins', 'f_globals', 'gi_code', '###']
others = ['__name__', 'close',
          'gi_code', 'gi_frame', 'gi_running',
          'send', 'throw']

print(ignore)

def main():

    known = set()
    stack = []
    gn = numbers()
    print(next(gn), next(gn))

    stack.append(('gn', gn))

    while stack:
        name, obj = stack.pop(0)
        objid = id(obj)
        objstr = strip_addr(repr(obj))
        print("process:", name, objid, objstr)

        for subname in dir(obj):
            if subname in ignore:
                continue
            sub = getattr(obj, subname)
            if id(sub) in known:
                continue
            known.add(id(sub))
            value_text = strip_addr(str(sub))
            print("obj: {} has attrib {} with value {}"
                  .format(name, subname, value_text))
            if -1 == value_text.find("built-in "):
                if len(stack) < 10:
                    stack.append((subname, sub))

def numbers():
    i = 0
    while True:
        yield i
        i += 1

def strip_addr(text):
    pp = text.find(' at ')
    if pp == -1:
        return text
    newtext = text[:pp] + text[pp+22:]
    return newtext

main()
                          
                          
