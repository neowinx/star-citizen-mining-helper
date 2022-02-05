import cv2
import numpy as np
from PIL import ImageGrab
import pytesseract
from numpy import ndarray
import re

from hsvfilter import HsvFilter
from vision import Vision

vision = Vision(None)

pytesseract.pytesseract.tesseract_cmd = "D:\\Program Files\\Tesseract-OCR\\tesseract.exe"

MASS_ROI = {"x1": 185, "y1": 443, "x2": 420, "y2": 590}
MINERALS_ROI = {"x1": 1488, "y1": 464, "x2": 1714, "y2": 600}
MASS_RE = re.compile(r"Mass: (.+)")
MINERALS_RE = {
        "Diamond": re.compile(r"Diamond \(Raw\): (.+)"),
        "Aluminium": re.compile(r"Aluminium \(Ore\): (.+)"),
        "Corundum": re.compile(r"Corundum \(Raw\): (.+)"),
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
    testroute = "C:\\Users\\pdavi\\Videos\\Squadron 42 - Star Citizen"
    for file in listfiles(testroute):
        # screenshot = ImageGrab.grab()
        # screenshot = np.array(screenshot)
        # img = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
        fname = f"{testroute}\\{file}"
        print(f"FILENAME: {fname}")
        img = cv2.imread(fname)

        hsv_filter = HsvFilter(80, 0, 174, 110, 151, 255, 0, 0, 0, 0)
        img = vision.apply_hsv_filter(img, hsv_filter)

        mass_txt = search_text(roi(img, MASS_ROI), MASS_RE)

        minerals_roi = roi(img, MINERALS_ROI)
        minerals_text = pytesseract.image_to_string(minerals_roi)

        for key in MINERALS_RE.keys():
            mineral_result = try_to_find(MINERALS_RE[key], minerals_text)
            print(f"{key}: {mineral_result}")

        cv2.imshow("Unnamed", img)

        key = cv2.waitKey()
        if key == ord('q'):
            cv2.destroyAllWindows()
            break
