# Tests of BoppreH keyboard and mouse modules to automate some things in Start Citizen
#
# IMPORTANT!: IF YOU WANT TO TEST THIS SCRIPT ON WINDOWS, DONT USE GIT-BASH, CYGWYN, MINGW, ETC.
#             OR THE OUTPUT MESSAGES ARE ALL HOLD UP UNTIL THE MAIN THREAD IS STOPPED
#             AND YOU WILL BE CONFUSED, BELIEVE ME
#
import keyboard
import mouse
import time

running = False

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

keyboard.add_hotkey('shift+p', position)
keyboard.add_hotkey('shift+i', exit)
keyboard.add_hotkey('shift+o', hail_landing_services)
mouse.on_button(autorun_toggle, (), [mouse.X2], [mouse.UP])
#keyboard.wait()
while True:
    time.sleep(1)
