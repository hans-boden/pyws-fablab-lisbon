# python3
"""
    Exercise: Python evaluations

    what you get:           experience in reading and understanding
                            basic Python statements
    what you have to do:    read the Python statements, try to figure out,
                            what happens. Enter the expected result into the
                            assert statement by replacing the underscore.

    a first example:
        ham = 3+4           some value is assigned to 'ham'
        assert ham == _     <== replace the _ by the expected value of 'ham'
        assert ham == 9     wrong: you will get an exception message, and the
                            program execution will stop
        assert ham == 7     good, the program will proceed to the next statement
        # assert ham == _   if you can't find the correct answer, change the line
                            into a comment (#), and continue with the next statement

    attention:
        '='  is an assignment,
             it evaluates the expression on the right side
             and assigns the value to the name of the left
        '==' is a test for 'equality' and is evaluated as
             a boolean value of either False or True

    happy guessing!  ;-)
"""

def main():

    simple_math()
    boolean()
    simple_string()
    index_n_slice()
    split_n_join()

def simple_math():
    # some simple math examples
    ham = 3+4
    assert ham == _
    ham = 3 + 4 * 5
    assert ham == _
    ham = 11 / 4
    assert ham == _
    ham = 11 / (2 * 2)
    assert ham == _
    ham = 11 / 4 * 2
    assert ham == _

    ham = 11 // 4   # integer division
    assert ham == _
    ham = 11 % 4  # modulo division - the rest
    assert ham == _

def boolean():
    # simple boolean operations

    t = True   # assign the 'True' value
    f = False
    # assert t == True    #sample
    # t = 7 == 7   # assign the result of a boolean expression
    # t = bool(7==7)  # sometimes it is better (easier to read) to use the bool() function
    # assert t == True    #sample

    quest = True == False
    assert quest == _
    quest = not t
    assert quest == _
    quest = not f
    assert quest == _
    quest = t and True
    assert quest == _
    quest = t and f     # true if all elements are true
    assert quest == _
    quest = t or f      # true if at least one element is true
    assert quest == _

    # everything is either True or False!
    quest = bool(True)
    assert quest == _
    quest = bool(0)
    assert quest == _
    quest = bool('') or bool([]) or bool({}) or bool()  # string, list, dictionary
    assert quest == _
    # anything, which is zero or empty or 'nothing', is False
    # everything else is True
    quest = bool('False')
    assert quest == _
    quest = bool([0])
    assert quest == _
    quest = bool(7-(6+1))
    assert quest == _

    # True and False are special values that are unique, they exist only once.
    # we can (and recommend) use the 'is' operator to test for boolean values, like:
    # assert t is True
    # '==' tests for equality, 'is' tests for identity
    assert f is False


def simple_string():
    # simple string operations
    # remember: a string is text, but its also an immutable sequence
    name = "Lisbon"
    soup = len(name)
    assert soup == _
    soup = name.lower()  # return a copy with all characters in lower case
    assert soup == _
    soup = name.upper()
    assert soup == _
    egg = name.find('L')
    assert egg == _
    egg = name.find('n')
    assert egg == _
    egg = name.find('z')
    assert egg == _
    really = name.endswith('bon')
    assert really == _
    really = name.startswith('lis')
    assert really == _

    bang = 'abc' + 'def'   # the '+' operator appends strings
    assert bang == _
    bang = 'ab' + "cd" + 'ef'
    assert bang == _
    bang = 'abc' * 3       # The '*' operator multiplies
    assert bang == _


    bang = ' ' + name + ' '    # add some "whitespace"
    assert bang == _
    # the term 'whitespace' is any combination of blanks, tabs and newlines
    # for now the samples only use blanks
    short = bang.strip()  # returns a copy with "whitespace" removed
    assert short == _
    bang = bang + ' x '
    short = bang.rstrip()  # remove "whitespace at the right side
    assert short == _
    short = bang.lstrip()  # remove "whitespace at the right side
    assert short == _
    short = bang.strip()  # remove "whitespace" at both ends
    assert short == _

def index_n_slice():
    # Some exercises about 'indexing' and 'slicing'
    name = "Lisbon"
    soup = name[1]
    assert soup == _
    soup = name[len(name)-1]
    assert soup == _
    soup = name[-1]    # same result, but shorter
    assert soup == _
    soup = name[-2]
    assert soup == _

    # a slice is defined by two numbers:
    #   from the start position (counting from zero)
    #   up to (but not including) the end position
    soup = name[2:4]
    assert soup == _
    soup = name[1:-1]
    assert soup == _
    soup = name[:3]   # there is a default for the first index
    assert soup == _
    soup = name[3:]   # an also for the first index
    assert soup == _
    soup = name[2:9]   # its not an error to specify the second index beyond the end
    assert soup == _
    soup = name[:]
    assert soup == _

def split_n_join():
    # Two important string methods: split() and join()
    snake = "ana con da"
    three = snake.split()   # breaks up at whitespace positions and returns a list
    size = len(three)
    assert size == _
    # Its not always required to use a variable, lets keep it shorter
    assert len(three) == _
    assert three[0] == _
    assert three[2] == _

    longer = '  ana   con da    '
    three = longer.split()    # split() removes all whitespace ==> same result
    assert three[2] == _

    # However ... split() can use arguments
    three = snake.split(' ')   # use a single blank as a splitter
    assert three[0] == _
    assert three[1] == _

    snake = 'anaconda'
    snip = snake.split('n')   # two 'n' ==> 3 parts
    assert len(snip) == _
    assert snip[0] == _
    assert snip[1] == _
    assert snip[-1] == _

    snip = snake.split('a')   # three 'a' ==> 4 parts
    assert len(snip) == _
    assert snip[0] == _
    assert snip[1] == _
    assert snip[2] == _
    assert snip[3] == _

    # there is a second argument to snip: a number giving the maximum number of splits
    snip = snake.split('n', 1)  # one split ==> 2 parts
    assert snip[1] == _
    snip = snake.split('n', 2)  # two splits ==> 3 parts
    assert snip[1] == _
    snip = snake.split('n', 3)  # three splits? but only 2 'n' ==> 3 parts
    assert snip[2] == _

    # how to specify the number of splits for a "whitespace" split?
    long = 'ana con da'
    snip = long.split(None, 1)  # 'None' omits the first argument
    assert len(snip) == _
    assert snip[0] == _
    assert snip[1] == _

    # join is a string method but works with a list.
    chars = list("four")
    assert len(chars) == _
    assert chars[3] == _
    junto = ''.join(chars)  # connect all elements of the list with ''
    assert junto == _
    # strange syntax - maybe ... we get used to it
    junto = '-'.join(chars)
    assert junto == _

def _(): pass  # ignore this line

main()

