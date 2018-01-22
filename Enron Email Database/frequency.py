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
for file in files:
    fp = open(directory + '/' + file)

    for ii in range(16):
        line = fp.readline()
    
    words = set(word_tokenize(fp.read()))
    for word in words:
        if word.lower() not in stop_words:
            tokens.add(word)

print(len(tokens))

# obtain frequency
#keywords  = list(tokens)
#frequency = [0 for ii in len(tokens)] 
#for ii in len(keywords):
#    for file in files:
#        fp = open(directory + '/' + file)
#        d  = fp.read()
#        if keywords[ii] in d:
#            frequency[ii] = frequency[i] + 1
#sorted(frequency, reverse=True)
#plt.plot(frequency)
#plt.show()
