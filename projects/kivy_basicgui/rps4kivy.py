# python3
"""
    Try to import and run a Kivy App
    use the kivy window for the RPS game
"""

import random

import basicgui as app

class G():
    putcons = lambda msg: print(msg)
    putmsg = lambda msg: print(msg)

    upoints = 0
    cpoints = 0
    valid = ('r', 'p', 's')
    firstwin = ('rs', 'sp', 'pr')

def main():
    app.config(dict(title="Rock - Paper - Scissor", cmdhdl=command_handler,
                    inithdl=init_handler))
    G.putcons = app.get_console_window()
    G.putmsg  = app.get_message_window()

    app.main()

def init_handler(text):
    G.putcons('~clr~')
    G.putcons('''Welcome to the Rock-Paper-Scissor game

You play against me, who first gets 10 points is the winner.
You enter your bet: 'r', 'p' or 's', I make my own bet.
Rock wins agains Scissor, Scissor wins against Paper,
Paper wins against Rock, two equal bets are a draw.
So lets start (you can enter 'x' to end the game at any time

Your first bet, please
''')
    G.putmsg('~clr~')
    G.putmsg('Status of the game:\n')

    G.state = 'g'
    G.rounds = 10  # maximum 10 rounds
    G.upoints = 0
    G.cpoints = 0

    write_status()

def term_handler(text):
    print("term_handler: {}".format(text))

def command_handler(text):
    if text == 'x':
        app.G.app.stop()
        return
    if G.state == 'g':
        handle_game(text)
        return
    if G.state == 'x':
        askagain(text)
        return

def handle_game(ubet):
    if not ubet in G.valid:
        G.putcons("wrong bet: '{}', must be 'r', 'p' or 's'")
        return
    cbet = random.choice(G.valid)
    if cbet == ubet:
        result = "that's a draw"
    elif cbet+ubet in G.firstwin:
        result = 'I win'
        G.cpoints += 1
        write_status()
    else:
        result = 'you win'
        G.upoints += 1
        write_status()
    msg = "Your bet was '{}', my bet was '{}':  {}"
    G.putcons(msg.format(ubet, cbet, result))

    if G.cpoints >= 10:
        G.putmsg("\nGame over, I have won")
        game_end()
        return
    if G.upoints >= 10:
        G.putmsg("\nGame over, You have won")
        game_end()
        return

def game_end():
    G.state = 'x'
    G.putcons("\nDo you want to play again? (y/n)")

def askagain(answer):
    if answer == 'y':
        init_handler(answer)
        return
    if answer == 'n':
        app.G.app.stop()
        return
    game_end()

def write_status():
    ustr = '>'*G.upoints + '.'*10
    cstr = '.'*10 + '<'*G.cpoints
    game = "you: {}win{} :me".format(ustr[:10], cstr[-10:])
    G.putmsg(game)

if __name__ == '__main__':
    main()
