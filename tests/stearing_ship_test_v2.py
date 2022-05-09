# stearing tests using pyautogui
import time

import keyboard
import mouse
import pyautogui


def mimi():
    print(f'starting')
    time.sleep(3)

    mouse.click()

    position = pyautogui.position()
    print(f'position: {position}')

    time.sleep(1)

    # pyautogui.moveTo(882, 501)
    pyautogui.drag(100, 0, duration=0.5)

    position = pyautogui.position()
    print(f'new position: {position}')


if __name__ == '__main__':
    keyboard.add_hotkey('control+w', mimi)
    keyboard.wait()
