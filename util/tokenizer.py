import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from tensorflow import keras
# from keras.preprocessing.text import Tokenizer

# read clean-data/clean.csv with pandas
df = pd.read_csv('clean-data/clean.csv', header=None)

df = df.iloc[:,0]

# histogram of word count that has 20 bins and print the bin bounderies

df.str.split().apply(len).hist(bins=20)
plt.show()

# print the bin bounderies of the histogram
print(df.str.split().apply(len).describe())

# turn df into an array of words, where the end of each scentence is marked by a ^
df = df.str.split().apply(lambda x: x + ['^']).values
tokens = np.concatenate(df)

print(tokens[:10])

given_words = 4
guess_words = 1
training_length = given_words + guess_words

text_sequences = []

for i in range(training_length, len(tokens)):
    seq = tokens[i-training_length:i]
    text_sequences.append(seq)

for i in range(10):
    print(' '.join(text_sequences[i]))

# tokenizer = Tokenizer()
# tokenizer.fit_on_texts(text_sequences)
# sequences = tokenizer.texts_to_sequences(text_sequences)

# print(len(sequences[0]))