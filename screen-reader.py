from time import sleep
from datetime import datetime

import cv2
import mss
import signal
import sys

import numpy as np
import pytesseract as pytes
import pandas as pd

# https://github.com/UB-Mannheim/tesseract/wiki

#"C:\Users\mmnair01\AppData\Local\Programs\Tesseract-OCR\\tesseract.exe"
pytes.pytesseract.tesseract_cmd = r"C:\Users\mmnair01\AppData\Local\Programs\Tesseract-OCR\\tesseract.exe"
session_id = "SID_"+datetime.now().strftime("%Y%m%d%H%M%S")

selection = {'top': 300, 'left': 0, 'width': 550, 'height': 60}

print(selection)
input("["+session_id+"] is the SID, press enter to start...")

def filter_text(string):
    string = string.replace("[","*[")
    string = string.replace("]:","]:*")

    split_string = string.split("*")

    res = []

    for i in split_string:
        if len(i)!=0:
            if (i.find("[") and i.find("]:")):
                res.append(i)
                
    res=" ".join(res)

    return res

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
        text = filter_text(text)

        text = text.replace('\n', ' ').replace('\r', '')
        
        if len(data["text"]) > 0 and data["text"].pop() == text:
            print("text is the same, skipping...")
        else:
            print("text read: "+text)

            data["text"].append(text)
    