from pynput.keyboard import Key, Controller
from time import sleep
import random

keyboard = Controller()

oppisite = {
    "w":"s",
    "a":"d",
    "s":"w",
    "d":"a"
}

def random_move():
    #make it press alt tab every other time this function is called
    keyboard.press(Key.alt)
    sleep(0.1)
    keyboard.press(Key.tab)

    choice = random.choice(["w","a","s","d"])
    keyboard.press(choice)
    sleep(0.1)
    keyboard.release(choice)
    sleep(0.1)
    keyboard.press(oppisite[choice])
    sleep(0.1)
    keyboard.release(oppisite[choice])

while True:
    random_move()
    sleep(5)
