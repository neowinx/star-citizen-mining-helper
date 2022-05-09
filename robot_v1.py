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
import pydirectinput

from main import wincap
from windowcapture import WindowCapture

scan_result_in_space = cv2.cvtColor(cv2.imread('vision/templates/scan_result_in_space.png'), cv2.COLOR_BGR2GRAY)
steering_cursor = cv2.cvtColor(cv2.imread('vision/templates/steering_cursor.png'), cv2.COLOR_BGR2GRAY)

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

def template_match(template):
    print('getting screenshot')
    scrsht_rgb = wincap.get_screenshot()

    print('finding scanned points')
    scr_gray = cv2.cvtColor(scrsht_rgb, cv2.COLOR_BGR2GRAY)

    locations = cv2.matchTemplate(scr_gray, template, cv2.TM_CCOEFF_NORMED)
    # threshold = 0.5
    # locations = np.where(res >= threshold)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(locations)
    return max_loc, scr_gray

def detect_objects(img):
    locations, scr_gray = template_match(scan_result_in_space)
    # threshold = 0.5
    # locations = np.where(res >= threshold)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(locations)
    return max_loc, scr_gray

def center_of_image(img):
    centerx = int(img.shape[0] / 2)
    centery = int(img.shape[1] / 2)
    return centerx, centery

def steer_towards(toX, toY, fromX, fromY, step=1, duration=1):
    steering = True
    print(f'steering towards {toX, toY}')

    x, y = fromX, fromY

    while steering:
        dx = step if fromX > toX else (step * -1)
        dy = step if fromY > toY else (step * -1)

        pydirectinput.moveTo(fromX - dx, fromY - dy)
        time.sleep(duration)

        if abs(fromX - toX) <= 10 and abs(fromY - toY) <= 10:
            break

def center_steering():
    print('centering steering')
    steering_cursor_loc, scr_gray = template_match(steering_cursor)
    centerx, centery = center_of_image(scr_gray)
    steer_towards(centerx, centery, steering_cursor_loc[0], steering_cursor_loc[1])

def mining_noproblem():
    print('scanning')
    # keyboard.send('tab')

    print('waiting scan results')
    # time.sleep(5)

    center_steering()
    return

    location, img_gray = detect_objects()

    print(f'stearing to: {location}')

    centerx, centery = center_of_image(img_gray)

    step = 1

    steering = True

    #pydirectinput.moveTo(centerx, centery)
    time.sleep(1)

    print('steering')
    while steering:
        dx = step if centerx > location[0] else (step * -1)
        dy = step if centery > location[1] else (step * -1)
        x, y = pydirectinput.position()

        pydirectinput.moveTo(x - dx, y - dy)

        time.sleep(1)

        location, img_gray = detect_objects()

        if abs(centerx - location[0]) <= 10 and abs(centery - location[1]) <= 10:
            break

    print('done steering')
    #keyboard.press('w')


if __name__ == '__main__':
    keyboard.add_hotkey('shift+p', position)
    keyboard.add_hotkey('alt+q', exit)
    keyboard.add_hotkey('alt+e', hail_landing_services)
    keyboard.add_hotkey('control+w', mining_noproblem)
    mouse.on_button(focus_toggle, (), [mouse.X2], [mouse.UP])
    mouse.on_middle_click(autorun_toggle)
    #keyboard.wait()
    while True:
        time.sleep(1)
