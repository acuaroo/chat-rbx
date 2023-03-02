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
tesseract_location = open("tesseract_path", "r").read()
tesseract_location = r'{}'.format(tesseract_location)

pytes.pytesseract.tesseract_cmd = tesseract_location

name = input("what's your username?\n")

session_id = name+datetime.now().strftime("%Y%m%d%H%M%S")

selection = {'top': 260, 'left': 0, 'width': 475, 'height': 45}

print(selection)
input("["+session_id+"] is the SID, press enter to start...")

def filter_text(string):
    string = string.replace("[","*[")
    string = string.replace("]:","]:*")

    split_string = string.split("*")

    res = []

    for i in split_string:
        if len(i) != 0:
            if (i.find("[") and i.find("]:")):
                res.append(i)
                
    res=" ".join(res)
    
    res = res.encode("ascii", "ignore").decode()

    return res

def signal_handler(signal, frame):
    print("saving data...")

    filename = session_id+".csv"
    data_frame = pd.DataFrame(data)
    data_frame.to_csv("training-data/"+filename, mode='a', index=False, header=False)

    print("session complete. data generated: "+str(len(data["text"])))
    print("data saved in training-data/"+filename)
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

        if text == "":
            print("empty text, skipping")
            continue

        text = text.replace('\n', ' ').replace('\r', '')
        
        if len(data["text"]) > 0 and data["text"][-1] == text:
            print("skipping duplicate text...")
        else:
            print("text read: "+text)

            data["text"].append(text)
    