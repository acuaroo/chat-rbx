from time import sleep
from datetime import datetime

import cv2
import mss
import signal
import sys

import numpy as np
import pytesseract as pytes
import pandas as pd

pytes.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR\\tesseract.exe"
session_id = "SID_"+datetime.now().strftime("%Y%m%d%H%M%S")

selection = {'top': 0, 'left': 0, 'width': 150, 'height': 150}

print({'top': 0, 'left': 0, 'width': 150, 'height': 150})
input("["+session_id+"] is the SID, press enter to start...")

def signal_handler(signal, frame):
    print("saving data...")

    filename = session_id+".csv"
    data_frame = pd.DataFrame(data)
    data_frame.to_csv(filename, mode='a', index=False, header=False)

    print("data saved in "+filename)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

data = {
    "text": [],
}

with mss.mss() as sct:
    while True:
        sleep(1)

        im = np.asarray(sct.grab(selection))
        text = pytes.image_to_string(im)

        text = text.replace('\n', ' ').replace('\r', '')

        print("text read: "+text)

        data["text"].append(text)
    