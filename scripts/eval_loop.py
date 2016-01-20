# python3
""" Interpret text lines from a file and produce output similar to the Python shell

Each line is treated ether as expression (v=evaluate) or as statement (x=execute)
"""
filename, tag = 'shell_commands_01.txt', 'A'
#filename, tag = 'shell_commands_02.txt', 'B'

def main():
    print("          ###   Python Shell Simulator   ###")
    print("          Execute statements from '{}' as '{}'".format(filename, tag))
    print()

    prepend = ''
    lino = 0
    for line in get_lines(filename):
        # line = line.strip()
        if not line:
            print()
            continue
        ltype = line[0]
        text = line[2:]
        text = text.replace('°', '"')
        
        if ltype == '#':
            print('     #', text)
            continue

        if ltype == 'j':
            if prepend:
                print("     ...", text)
            else:
                lino += 1
                print("{}{:03d} >>>".format(tag, lino), text)
            prepend += text + '\n'
            
        if ltype == 'v':
            if prepend:
                print("     ...", text)
                text = prepend + text
                prepend = ''
            else:
                lino += 1
                print("{}{:03d} >>>".format(tag, lino), text)

            try:
                r = eval(text)
                if not r is None:
                    print("    ", repr(r))
            except Exception as e:
                print("    ",repr(e))
            continue
        
        if ltype == 'x':
            if prepend:
                print("    ...", text)
                text = prepend + text + '\n'
                prepend = ''
            else:
                lino += 1
                print("{}{:03d} >>>".format(tag, lino), text)
            try:
                exec(text)
            except Exception as e:
                print("    ", repr(e))

def get_lines(filename):
    with open(filename, mode='r', encoding="utf-8") as fi:
        for line in fi:
            yield line.rstrip()
        
main()        
