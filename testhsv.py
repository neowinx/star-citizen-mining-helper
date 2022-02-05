import cv2 as cv
import numpy as np
import os
from time import time

import pytesseract
pytesseract.pytesseract.tesseract_cmd = "D:\\Program Files\\Tesseract-OCR\\tesseract.exe"

from vision import Vision
from hsvfilter import HsvFilter

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# initialize the Vision class
vision = Vision(None)
# initialize the trackbar window
vision.init_control_gui()

# limestone HSV filter
hsv_filter = HsvFilter(0, 180, 129, 15, 229, 243, 143, 0, 67, 0)

loop_time = time()
while True:

    # get an updated image of the game
    screenshot = cv.imread("C:\\Users\\pdavi\\Videos\\Squadron 42 - Star Citizen\\Squadron 42 - Star Citizen Screenshot 2022.02.03 - 01.08.22.64.png")

    # pre-process the image
    processed_image = vision.apply_hsv_filter(screenshot)

    # do object detection
    # rectangles = vision.find(processed_image, 0.46)

    # draw the detection results onto the original image
    # output_image = vision.draw_rectangles(screenshot, rectangles)

    # display the processed image
    cv.imshow('Processed', processed_image)
    # cv.imshow('Matches', output_image)

    # debug the loop rate
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # text_from_roi = pytesseract.image_to_string(processed_image)
    # print(text_from_roi)

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')
