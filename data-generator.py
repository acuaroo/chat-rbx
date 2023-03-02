import pandas as pd
import os
from os import path
import numpy as np
import re

directory = 'training-data'
valid_words = set(x[:-1].lower() for x in open('dictionary.txt').readlines())
valid_characters = r"-+_?.,!$/1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

dfs = []

for filename in os.listdir(directory):
    pth = directory+'/'+filename

    if not path.exists(pth):
        continue

    csv = pd.read_csv(directory+'/'+filename, on_bad_lines='skip')
    df = pd.DataFrame(data=csv)

    df.replace('', np.nan, inplace=True)
    df.dropna(inplace=True)

    df = df.iloc[:,0].str.lower()

    #df = df.str.replace('[^'+valid_characters+']', ' ')

    for w in df.str.split():
        if not (any(word in w for word in valid_words)):
            df.replace(w, '', inplace=True)
            print(w)

    print(df)
    dfs.append(df)

df = pd.concat(dfs)
df.to_csv('clean-data/cleaned.csv', index=False, header=False)
