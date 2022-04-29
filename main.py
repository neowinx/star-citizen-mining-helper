import re
import time

import cv2
import pytesseract
from numpy import ndarray

from vision import Vision
from windowcapture import WindowCapture
import tkinter as tk
from tkinter import ttk, Frame, BOTTOM, TOP

import keyboard

# WindowCapture.list_window_names()
# exit()

wincap = WindowCapture()

vision = Vision(None)

pytesseract.pytesseract.tesseract_cmd = "D:\\Program Files\\Tesseract-OCR\\tesseract.exe"

MASS_ROI = {"x1": 185, "y1": 443, "x2": 420, "y2": 590}
MINERALS_ROI = {"x1": 1488, "y1": 464, "x2": 1714, "y2": 600}
MASS_RE = re.compile(r"Mass: (.+)")
MINERALS_RE = {
        "Quantainium": {"re": re.compile(r"Quantainium \(Raw\): (.+)%"), "price": 88.00},
        "Bexalite": {"re": re.compile(r"Bexalite \(Raw\): (.+)%"), "price": 44.00},
        "Taranite": {"re": re.compile(r"Taranite \(Raw\): (.+)%"), "price": 35.21},
        "Borase": {"re": re.compile(r"Borase \(Ore\): (.+)%"), "price": 35.21},
        "Laranite": {"re": re.compile(r"Laranite \(Raw\): (.+)%"), "price": 31.00},
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
        "Aluminum": {"re": re.compile(r"Aluminum \(Ore\): (.+)%"), "price": 1.30},
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


def get_minerals_values():
    img = wincap.get_screenshot()

    # hsv_filter = HsvFilter(80, 0, 174, 110, 151, 255, 0, 0, 0, 0)
    # img = vision.apply_hsv_filter(img, hsv_filter)

    mass_result = search_text(roi(img, MASS_ROI), MASS_RE)
    minerals_img = roi(img, MINERALS_ROI)
    minerals_text = pytesseract.image_to_string(minerals_img)

    data = []
    total_auec = 0

    for key in MINERALS_RE.keys():
        mineral_result: str = try_to_find(MINERALS_RE[key]['re'], minerals_text)

        # this is not really the best approach but I am in a hurry right now
        if mineral_result and mass_result:
            try:
                units = float(mineral_result) * 0.02 * float(mass_result)
                auec = MINERALS_RE[key]['price'] * units
                # print(f"{key} | units: {units} auec: {int(auec):,}")
                data.append({'mineral': key, 'auec': int(auec)})
                total_auec += auec
            except ValueError:
                total_auec = total_auec

    if total_auec > 0:
        # print(f"Total aUEC: {int(total_auec):,}")
        # print()

        return {'data': data, 'total': int(total_auec)}


class SCMHW(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('SCMH')
        self.resizable(0, 0)
        self.geometry('320x240')
        self.attributes('-alpha', 0.5)
        self.attributes('-topmost', True)
        # change the background color to black
        self['bg'] = 'black'

        self.mainFrame = Frame(self)
        self.mainFrame.pack(side=TOP)
        self.mainFrame.style = ttk.Style(self)
        self.mainFrame.style.configure(
            'TLabel',
            background='black',
            foreground='white')
        self.mainFrame.labels = []

        label = ttk.Label(text='papa')
        label.pack()
        self.mainFrame.labels.append(label)

        self.logFrame = Frame(self)
        self.logFrame.pack(side=BOTTOM)
        self.logFrame.labels = []

        label = ttk.Label(text='mama')
        label.pack()
        self.logFrame.labels.append(label)

        keyboard.add_hotkey('alt+r', self.destroy)
        keyboard.add_hotkey('alt+t', self.update_values)
        keyboard.add_hotkey('alt+p', lambda: self.add_label('mloso'))

    def add_label(self, text, foreground='white'):
        label = ttk.Label(
              self,
              text=text,
              foreground=foreground,
              font=('Digital-7', 15))
        label.pack(expand=True)
        self.mainFrame.labels.append(label)

    def clear_labels(self):
        for label in self.labels:
            label.destroy()
        self.mainFrame.labels = []

    def update_values(self):
        mineral_data = get_minerals_values()
        if mineral_data:
            self.clear_labels()
            for md in mineral_data['data']:
                self.add_label(f"{md['mineral']}: {int(md['auec']):,}")
            if mineral_data['total'] > 100000:
                self.add_label(f"TOTAL: {int(mineral_data['total']):,}", 'green')
            elif mineral_data['total'] > 50000:
                self.add_label(f"TOTAL: {int(mineral_data['total']):,}", 'yellow')
            else:
                self.add_label(f"TOTAL: {int(mineral_data['total']):,}", 'red')


if __name__ == '__main__':
    scmhw = SCMHW()
    scmhw.mainloop()

