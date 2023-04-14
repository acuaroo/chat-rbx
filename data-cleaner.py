import pandas as pd
import numpy as np

import os
import re
from os import path

directory = 'training-data'
valid_words = set(x[:-1].lower() for x in open('assets/dictionary.txt').readlines())

cleaned_data = []

for filename in os.listdir(directory):
    df = pd.read_csv(path.join(directory, filename), header=None, on_bad_lines='skip')
    pruned = 0 

    for index, row in df.iterrows():
        for word in re.findall(r"\w+|[^\w\s]", row[0], re.UNICODE):
            if word.lower() not in valid_words:
                row[0] = row[0].replace(word, '')
                pruned += 1

    cleaned_data.append(df)

    print(filename, "pruned: "+str(pruned))

cleaned_data = pd.concat(cleaned_data)
cleaned_data = cleaned_data.replace(r'^\s*$', np.nan, regex=True)
cleaned_data = cleaned_data.dropna()

cleaned_data = cleaned_data.apply(lambda x: x.str.strip())

cleaned_data = cleaned_data.replace(r'\s+', ' ', regex=True)
cleaned_data = cleaned_data.drop_duplicates()

cleaned_data.to_csv('clean-data/clean-4-14-23.csv', index=False, header=False)