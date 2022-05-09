# stearing tests using pydirect input

import time

import keyboard
import mouse
import pydirectinput


def mimi():
    print(f'starting')
    time.sleep(3)

    mouse.click()

    position = pydirectinput.position()
    print(f'position: {position}')

    time.sleep(1)

    pydirectinput.moveTo(882, 501)
    #pydirectinput.drag(100, 0, duration=0.5)

    position = pydirectinput.position()
    print(f'new position: {position}')


if __name__ == '__main__':
    keyboard.add_hotkey('control+w', mimi)
    keyboard.wait()
