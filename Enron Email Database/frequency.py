import os
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import words as nltk_words


# find all the folders and set up nltk
directory  = "./enron_mail_20150507/maildir/"
users      = os.listdir(directory)

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('words')
stop_words = set(stopwords.words('english'))
stop_words.update(list(string.punctuation))
dictionary = set(nltk_words.words())

# obtain set of keywords
user_folders = ['sent']
documents = []
for user in users:
    for folder in user_folders:
        if os.path.exists(directory + user + '/' + folder) is False:
            break
        
        fileList = os.listdir(directory + user + '/' + folder)
        for file in fileList:
            tokens = set()
            fp = open(directory + user + '/' + folder + '/' + file, 'r')

            for ii in range(16):
                fp.readline()

            line = fp.readline()
            while line is not '':
                if '@' not in line:
                    tokens_raw = word_tokenize(line)
                    for t in tokens_raw:
                        if t.lower() in dictionary and t.lower() not in stop_words:
                            tokens.add(t.lower())
                line = fp.readline()
                            
            documents.append((directory + user + '/' + folder + '/' + file, tokens))

# keep a copy of keyword set
keyword_set = set()
for doc in documents:
    keyword_set.update(doc[1])
keyword_list = list(keyword_set)


# use an index to remember index of tokens
index = {}
for ii in range(len(keyword_list)):
    index[keyword_list[ii]] = ii

# compute frequency
frequency = [0 for ii in range(len(keyword_set))]
for doc in documents:
    for keyword in doc[1]:
        frequency[index[keyword]] = frequency[index[keyword]] + 1

file_size = len(documents)
for ii in range(len(frequency)):
    frequency[ii] = frequency[ii] / file_size * 100

# link frequency to keywords
linked_frequency = [(keyword_list[ii],frequency[ii]) for ii in range(len(frequency))]

# sort and remove most frequent keywords
most_frequent = 100
linked_frequency = sorted(linked_frequency, key=lambda linked: linked[1], reverse=True)
linked_frequency = linked_frequency[most_frequent:len(linked_frequency)]

#-------------------------------------------------------------------------
# output to file
file_name = './results/1.txt'
fp = open(file_name, 'w')
frequency = [linked_frequency[ii][1] for ii in range(len(linked_frequency))]
for ii in range(len(linked_frequency)-1):
    fp.write('%f,' %(frequency[ii]))
fp.write('%f\n' %(frequency[-1]))
fp.close()
