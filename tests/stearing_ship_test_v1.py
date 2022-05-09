# stearing tests using mouse library

import time

import keyboard
import mouse


def mimi():
    print(f'starting')
    time.sleep(3)

    mouse.click()

    position = mouse.get_position()
    print(f'position: {position}')

    time.sleep(1)

    mouse.move(882, 501)

    position = mouse.get_position()
    print(f'new position: {position}')


if __name__ == '__main__':
    keyboard.add_hotkey('control+w', mimi)
    keyboard.wait()
