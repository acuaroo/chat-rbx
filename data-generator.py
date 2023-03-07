import pandas as pd
import os
from os import path
import numpy as np

directory = 'training-data'
valid_words = set(x[:-1].lower() for x in open('assets/dictionary.txt').readlines())
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

    df = df.iloc[:,0]
    
    for sentence in df.str.split():
        for word in sentence:
            if not (word.lower() in valid_words):
                old_scentence = ' '.join(sentence)

                sentence.remove(word)
                new_scentence = ' '.join(sentence)
                
                print(word)
                df = df.str.replace(old_scentence, new_scentence, regex=False)

    dfs.append(df)

df = pd.concat(dfs)

df = df.str.replace('[', '', regex=False)
df = df.str.replace(']', '', regex=False)
df = df.str.replace('{', '', regex=False)
df = df.str.replace('}', '', regex=False)
df = df.str.replace('(', '', regex=False)
df = df.str.replace(')', '', regex=False)
df = df.str.replace(':', '', regex=False)
df = df.str.replace('_', '', regex=False)

df = df.str.strip()

df.replace('', np.nan, inplace=True)

df.dropna(inplace=True)

df.to_csv('clean-data/clean.csv', index=False, header=False)
