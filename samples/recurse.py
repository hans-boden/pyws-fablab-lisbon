# python3
"""
    Use a recursive function to resolve nested expressions
    The input string is not checked for a 'correct' syntax
    'incorrect' data will produce strange results or errors
"""

xpress = '1+2+(3*((4+7))+8/(2*2))*6+(3+7*(8-6))'

def recurs(text, lvl=0):
    evalstr = ''
    while text:
        p = text[0]
        text = text[1:] if text != p else ''
        if p == '(':
            val, text = recurs(text, lvl+1)
            evalstr += str(val)
        elif p == ')':
            break
        else:
            evalstr += p
    print("level {} evaluate: '{}'".format(lvl, evalstr))
    return eval(evalstr) if evalstr else '', text  # eval() never gets any parenthesis

def call_recurs(text):
    print("\nEvaluate: '{}'".format(text))
    val, _ = recurs(text)
    print("Result: '{}'".format(val))

call_recurs('')
call_recurs('()')
call_recurs('(9*(2+3))')
call_recurs(xpress)
print(eval(xpress))

