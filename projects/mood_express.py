# python3
"""
    This script imports the random module and introduces the ``if`` statement
    It shows a function definition with argument and return value
    It shows the while loop with break and else
"""
import random
import time

def main():
    print("How do I feel?")
    counter = 10    # express the mood 7 times
    #random.seed(2685199) #('bored')  # ('nice')
    while counter:
        counter = counter - 1
        time.sleep(0.1) # (1.5)
        mood = random.random()
        emotion = express_mood(mood)
        if emotion == 'sad':
            print("I don't want to talk anymore")
            break
        print("I am", emotion)
    else:
        print("Good bye")

def express_mood(level):
    # translate a mood-level into a text
    if level > 0.7:
        mood_text = 'happy'
    elif level > 0.5:
        mood_text = 'fine'
    elif level > 0.2:
        mood_text = 'ok'
    else:
        mood_text = 'sad'
    return mood_text


def test():
    # find a seed, which produces 10 iterations of random.random() with > 0.7
    reps = 7
    r = random.random
    for x in range(10000000):
        random.seed(x)
        for y in range(reps):
            if r() <= 0.7:
                break
        else:
            print(x)
            break
    else:
        return
    random.seed(x)
    for y in range(reps):
        print(y+1, r())

#test()
main()
