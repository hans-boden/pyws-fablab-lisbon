# python 3
import os, os.path

path = 'data'  # a subfolder of the folder, where this script is stored

def main():
    io_write_file()
    io_read_file()


def io_write_file():
    filename = os.path.join(path, 'firstdata.txt')
    print(filename)
    if os.path.exists(filename):  # the overwrite test is optional
        print("dont overwrite")   # often overwriting existing files
        return                    # is the right choice
    fo = open(filename, mode='w')
    for num in range(1, 21):
        fo.write("number: {:3d}, squared: {:4d}\n".format(num, num*num))
    fo.close()

def io_read_file():
    filename = os.path.join(path, 'firstdata.txt')
    fi = open(filename, mode='r')
    for line in fi:   # !!! fi can be iterated and returns line by line
        print(line.rstrip())   # rstrip() removes the 'newline' endings
    fi.close()
              
main()        
