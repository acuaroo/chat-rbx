from time import sleep
from datetime import datetime

import mss
import signal
import sys

import numpy as np
import pytesseract as pytes
import pandas as pd

# https://github.com/UB-Mannheim/tesseract/wiki

# go into assets, and make a file called "tesseract_path"
# in that file, put the path to your tesseract.exe
# for example, if your tesseract.exe is in C:\Program Files\Tesseract-OCR\tesseract.exe
# then you would put C:\Program Files\Tesseract-OCR\tesseract.exe in the file

tesseract_location = open("assets/tesseract_path", "r").read()
tesseract_location = r'{}'.format(tesseract_location)

pytes.pytesseract.tesseract_cmd = tesseract_location

name = input("what's your username?\n")

session_id = name+datetime.now().strftime("%Y%m%d%H%M%S")

selection = {'top': 258, 'left': 5, 'width': 400, 'height': 25}

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

def save_data():
    filename = session_id+".csv"
    data_frame = pd.DataFrame(data)
    data_frame.to_csv("training-data/"+filename, mode='a', index=False, header=False)

    print("data saved in training-data/"+filename)

def signal_handler(signal, frame):
    print("saving data...")

    save_data()

    print("session complete. data generated: "+str(len(data["text"])))
    
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
        
        if len(data["text"]) >= 2500:
            save_data()
            data["text"] = []
            session_id = name+datetime.now().strftime("%Y%m%d%H%M%S")
    