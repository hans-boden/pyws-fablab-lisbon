# python3
''' Rock, Paper, Scissor – a small computer game
	Written by Tom Dewly, 2016
'''
import random
match_points = 10
comp_points = user_points = 0
valid_bets = 'rps'
msg = '''Hello User – let's play 'Rock, Paper, Scissor'
Who first gets {} points, wins the match.
Let's start!'''
print(msg.format(match_points))

while user_points < match_points and comp_points < match_points:
    comp_bet = random.choice(valid_bets)
    
    ask_user = 'Enter your bet: r, p or s. Enter x to end the game '
    user_bet = ''
    while user_bet == '':  # input loop
        user_bet = input(ask_user)
        if user_bet in valid_bets or user_bet == 'x':
            break
        print('wrong input, please try again ...')
        user_bet = ''   # stay in the input loop

    if user_bet == 'x':
        print('you give up? - ok, see you soon') 
        break

    if user_bet == comp_bet:
        print('your bet was {}, my bet was {}, '
              'that\'s a draw'.format(user_bet, comp_bet))
        continue

    if comp_bet+user_bet in 'rs sp pr'.split():
        who_wins = 'I win'
        comp_points += 1
    else:
        who_wins = 'you win'
        user_points += 1

    result_msg = ('Your bet: {}, my bet: {}, {}  - '
                  'your points: {}, my points:{}' )
    print(result_msg.format(user_bet, comp_bet, who_wins,
                            user_points, comp_points))

if user_points >= match_points:
    print('You won, sure that was pure luck, pah!')
if comp_points >= match_points:
    print('I won! - hey, I am smarter than you, loooser!')
    
