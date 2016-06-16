# python3
"""
    Mastermind without kivy - by Luis
    merciless edited by hans
"""

import random
import re

class G():
    valid_chars = '123456'
    secret_len = 5
    solved = '+' * secret_len
    regex_str = "^[{0}]{{{1},{1}}}$".format(valid_chars, secret_len)
    valid_input = re.compile(regex_str) # regular expression for user input
    
def main():
    secret = answer_generator()
    print('Enter your guess of {} of these symbols: ({})'
          .format(G.secret_len, G.valid_chars))
    
    while True:
        user_seq = user_guess()
        output = handle_game(secret, user_seq)

        result_msg = ('{}  ->  {}')
        print(result_msg.format(user_seq, output))
        if output == G.solved:
            break
        
    print('You have found the answer! Goodbye!')

def handle_game(answer, guess):
    answer = list(answer)  # no need to str() or to assign a new name
    guess = list(guess)
    
    output = ''
    for i, ch in enumerate(guess):
        if ch == answer[i]:
            # eliminate hits from both lists, but leave position untouched
            guess[i] = '°'   # any char which is not in valid_chars
            answer[i] = '^'
            output += '+'
    
    for ch in guess:
        if ch in answer:
            # remove hit from answer, position is no longer important
            answer.remove(ch)
            output += '-'
            
    return output
                   
def user_guess():
    while True:
        response = input()   # no argument needed, default is ''
        if G.valid_input.match(response):
            return response
        print("wrong input...")

def answer_generator(): # Creates random sequence of n characters 
    seq = ''
    for _ in range(G.secret_len):  # '_': we dont care for the value
        seq += random.choice(G.valid_chars)  # valid_chars string is iterable
    return seq
      
if __name__ == '__main__':
    main()
