# python3
"""
    Try to import and run a Kivy App
    use the kivy window for the RPS game
"""

import random

import basicgui as app

class G():
    upoints = 0
    cpoints = 0
    valid = ('r', 'p', 's')
    firstwin = ('rs', 'sp', 'pr')

def main():
    app.config(dict(title="Rock - Paper - Scissor",
                    cmdhdl=command_handler,
                    inithdl=init_handler))
    app.start()

def init_handler():
    app.put_console('~clr~')
    app.put_console('''Welcome to the Rock-Paper-Scissor game

You play against me, who first gets 10 points is the winner.
You enter your bet: 'r', 'p' or 's', I make my own bet.
Rock wins agains Scissor, Scissor wins against Paper,
Paper wins against Rock, two equal bets are a draw.
So lets start (you can enter 'x' to end the game at any time

Your first bet, please
''')
    app.put_message('~clr~')
    app.put_message('Status of the game:\n')

    G.state = 'g'
    G.rounds = 10  # maximum 10 rounds
    G.upoints = 0
    G.cpoints = 0

    write_status()

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
        app.put_console("wrong bet: '{}', must be 'r', 'p' or 's'".format(ubet))
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
    app.put_console(msg.format(ubet, cbet, result))

    if G.cpoints >= 10:
        app.put_message("\nGame over, I have won")
        game_end()
        return
    if G.upoints >= 10:
        app.put_message("\nGame over, You have won")
        game_end()
        return

def game_end():
    G.state = 'x'
    app.put_console("\nDo you want to play again? (y/n)")

def askagain(answer):
    if answer == 'y':
        init_handler(answer)
        return
    if answer == 'n':
        app.stop()
        return
    game_end()

def write_status():
    ustr = '>'*G.upoints + '.'*10
    cstr = '.'*10 + '<'*G.cpoints
    game = "you: {}win{} :me".format(ustr[:10], cstr[-10:])
    app.put_message(game)

if __name__ == '__main__':
    main()
