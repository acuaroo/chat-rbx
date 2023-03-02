import pandas as pd
import os
from os import path
import numpy as np
import re

directory = 'training-data'
valid_words = set(x[:-1].lower() for x in open('dictionary.txt').readlines())
ban_characters = "|:[]"

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

    for sentence in df.str.split():
        for word in sentence:
            if not (word in valid_words):
                df.replace(word, '', inplace=True)
                #print(word)

    dfs.append(df)

df = pd.concat(dfs)
df.to_csv('clean-data/clean.csv', index=False, header=False)
