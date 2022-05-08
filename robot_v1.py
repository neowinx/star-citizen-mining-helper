# Tests of BoppreH keyboard and mouse modules to automate some things in Start Citizen
#
# IMPORTANT!: IF YOU WANT TO TEST THIS SCRIPT ON WINDOWS, DONT USE GIT-BASH, CYGWYN, MINGW, ETC.
#             OR THE OUTPUT MESSAGES ARE ALL HOLD UP UNTIL THE MAIN THREAD IS STOPPED
#             AND YOU WILL BE CONFUSED, BELIEVE ME
#
import cv2
import keyboard
import mouse
import time

import numpy as np

from main import wincap
from windowcapture import WindowCapture

scan_result_in_space = cv2.cvtColor(cv2.imread('vision/templates/scan_result_in_space.png'), cv2.COLOR_BGR2GRAY)

running = False
focusing = False
mining = False

def focus_toggle():
   global focusing
   focusing = not focusing
   if focusing:
       keyboard.press('f')
   else:
       keyboard.release('f')

def autorun_toggle():
   global running
   running = not running
   if running:
       keyboard.press('shift+w')
   else:
       keyboard.release('shift+w')

def hail_landing_services():
   keyboard.send('f11')
   time.sleep(3)
   mouse.click()
   time.sleep(1)
   mouse.move(249, 167)
   time.sleep(1)
   mouse.click()
   time.sleep(1)
   mouse.move(413, 270)
   time.sleep(1)
   mouse.click()
   time.sleep(1)
   keyboard.send('f11')

def position():
    pos = mouse.get_position()
    print(pos)

wincap = WindowCapture()

def mining_noproblem():
    print('scanning')
    #keyboard.send('tab')
    print('waiting scan results')
    time.sleep(5)
    print('getting screenshot')
    img_rgb = wincap.get_screenshot()

    print('finding scanning points')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    locations = cv2.matchTemplate(img_gray, scan_result_in_space, cv2.TM_CCOEFF_NORMED)
    # threshold = 0.5
    # locations = np.where(res >= threshold)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(locations)
    location = max_loc

    # print('gettings closest point to the center')
    # height = img_gray.shape[0]
    # width = img_gray.shape[1]
    # pt = np.array([width / 2, height / 2])
    #
    # nearest_kp = min(locations, key=lambda kp: np.linalg.norm(kp.pt - pt))
    # print(f'nearest point found: {nearest_kp.pt}')
    # print(f'stearing to: {nearest_kp.pt}')
    mouse.move(location[0], location[1])


if __name__ == '__main__':
    keyboard.add_hotkey('shift+p', position)
    keyboard.add_hotkey('shift+i', exit)
    keyboard.add_hotkey('shift+o', hail_landing_services)
    keyboard.add_hotkey('shift+w', mining_noproblem)
    mouse.on_button(focus_toggle, (), [mouse.X2], [mouse.UP])
    mouse.on_middle_click(autorun_toggle)
    #keyboard.wait()
    while True:
        time.sleep(1)
