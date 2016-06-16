# python3
"""
    Mastermind without kivy
"""

import random
import re

class D():
    valid_digits = (1,2,3,4,5,6)
    c_sequence = 0
    output = ""

def main():
    answer_generator()
    #print(('Cheat -> Answer is {}').format(Hidden_seq))
    print('Enter your guess of 4 digits, each in the range of 1 to 6:')
    while D.output != '++++':
        D.output = ""
        
        user_seq=user_guess()
        handle_game(D.c_sequence,user_seq)

        result_msg = ('{}  ->  {}')
        print(result_msg.format(user_seq, D.output))

    print('You have found the answer! Goodbye!')

def handle_game(answer,guess):
    answer_s=str(answer)
    guess_s=str(guess)
    aux=[0, 0, 0, 0]
    for i in range(0,len(answer_s)):
        if answer_s[i]==guess_s[i]:
            D.output= D.output + '+'
            
            aux[i]=1 #correct position marker

            #replace answer character by a non recognizable one (i.e. "9")
            #so that it is not compared again by other guess character
            answer_s=answer_s.replace(answer_s[i], "9", 1)
            
    if D.output == '++++':
            pass
    else:   
        for i in range (0,4):
            if aux[i]==1:
                pass
            else:
                if guess_s[i] in answer_s:
                    u=answer_s.index(guess_s[i]) #index of character that is equal

                    #replace answer character by a non recognizable one (i.e. "9")
                    #so that it is not compared again by other guess character
                    answer_s=answer_s.replace(answer_s[u], "9", 1)

                    D.output= D.output + '-'
                   
def user_guess():
    ask_user = ''
    response = ''
    while response == '':
        response = input(ask_user)
        if len(str(response)) == 4 and response.isdigit() and re.match("^[1-6]*$", str(response)):
            break
        print('wrong input, please try again ...')
        response = ''         
    return response

def answer_generator(): # Creates random sequence of 4 digits, ranging from 1 to 6
    while len(str(D.c_sequence))<4:
        c_hidden = random.choice(D.valid_digits)
        if D.c_sequence == 0:
            D.c_sequence=c_hidden
        else:
            D.c_sequence=D.c_sequence*10+c_hidden
      
if __name__ == '__main__':
    main()
