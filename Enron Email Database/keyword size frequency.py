import os
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# find all the folders and set up nltk
directory  = "./DB/arnold-j/sent"
files      = os.listdir(directory)

nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))
stop_words.update(list(string.punctuation))
stop_words.update('Subject')

# obtain keywords
tokens = set()
sizes = []
for file in files:
    fp = open(directory + '/' + file)

    for ii in range(16):
        line = fp.readline()
    
    words = set(word_tokenize(fp.read()))
    sizes.append(len(words))

#sizes = sorted(sizes, reverse=True)
print(sum(sizes)/len(files))

