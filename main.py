import cv2
import numpy as np
from PIL import ImageGrab
import pytesseract
from numpy import ndarray
import re

from hsvfilter import HsvFilter
from vision import Vision
from windowcapture import WindowCapture

# WindowCapture.list_window_names()
# exit()

wincap = WindowCapture()

vision = Vision(None)

pytesseract.pytesseract.tesseract_cmd = "D:\\Program Files\\Tesseract-OCR\\tesseract.exe"

MASS_ROI = {"x1": 185, "y1": 443, "x2": 420, "y2": 590}
MINERALS_ROI = {"x1": 1488, "y1": 464, "x2": 1714, "y2": 600}
MASS_RE = re.compile(r"Mass: (.+)")
MINERALS_RE = {
        "Quantanium": {"re": re.compile(r"Quantanium \(Raw\): (.+)%"), "price": 88.00},
        "Bexalite": {"re": re.compile(r"Bexalite \(Raw\): (.+)%"), "price": 44.00},
        "Taranite": {"re": re.compile(r"Taranite \(Raw\): (.+)%"), "price": 35.21},
        "Borase": {"re": re.compile(r"Borase \(Ore\): (.+)%"), "price": 35.21},
        "Laranite": {"re": re.compile(r"Laranite \(Ore\): (.+)%"), "price": 31.00},
        "Agricium": {"re": re.compile(r"Agricium \(Ore\): (.+)%"), "price": 27.41},
        "Hephaestanite": {"re": re.compile(r"Hephaestanite \(Raw\): (.+)%"), "price": 15.85},
        "Titanium": {"re": re.compile(r"Titanium \(Ore\): (.+)%"), "price": 8.90},
        "Diamond": {"re": re.compile(r"Diamond \(Raw\): (.+)%"), "price": 7.35},
        "Gold": {"re": re.compile(r"Gold \(Ore\): (.+)%"), "price": 6.41},
        "Copper": {"re": re.compile(r"Copper \(Ore\): (.+)%"), "price": 6.15},
        "Beryl": {"re": re.compile(r"Beryl \(Raw\): (.+)%"), "price": 4.35},
        "Tungsten": {"re": re.compile(r"Tungsten \(Ore\): (.+)%"), "price": 4.06},
        "Corundum": {"re": re.compile(r"Corundum \(Raw\): (.+)%"), "price": 2.71},
        "Quartz": {"re": re.compile(r"Quartz \(Raw\): (.+)%"), "price": 1.55},
        "Aluminium": {"re": re.compile(r"Aluminium \(Ore\): (.+)%"), "price": 1.30},
}


def listfiles(path):
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    return onlyfiles


def roi(img: ndarray, roi: dict):
    return img[roi['y1']:roi['y2'], roi['x1']:roi['x2']]


def search_text(img, pattern):
    text_from_roi = pytesseract.image_to_string(img)
    return try_to_find(pattern, text_from_roi)


def try_to_find(pattern, text_from_roi):
    txt_found = pattern.search(text_from_roi)
    if txt_found:
        return txt_found.group(1)


if __name__ == '__main__':
    while True:
        img = wincap.get_screenshot()

        # hsv_filter = HsvFilter(80, 0, 174, 110, 151, 255, 0, 0, 0, 0)
        # img = vision.apply_hsv_filter(img, hsv_filter)

        mass_result = search_text(roi(img, MASS_ROI), MASS_RE)
        minerals_img = roi(img, MINERALS_ROI)
        minerals_text = pytesseract.image_to_string(minerals_img)

        total_auec = 0

        for key in MINERALS_RE.keys():
            mineral_result: str = try_to_find(MINERALS_RE[key]['re'], minerals_text)

            # this not really the best approach but I am in a hurry right now
            if mineral_result:
                try:
                    total_auec += float(mineral_result) * 2.00 * float(mass_result)
                except ValueError:
                    total_auec = total_auec

        if total_auec > 0:
            print(f"Total aUEC: {total_auec}")

        cv2.imshow("Unnamed", minerals_img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            cv2.destroyAllWindows()
            break
