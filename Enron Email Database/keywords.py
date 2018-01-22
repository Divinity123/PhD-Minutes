import os
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# find all the folders and set up nltk
directory  = "./DB/"
users      = os.listdir(directory)

nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))
stop_words.update(list(string.punctuation))
stop_words.update('Subject')


# obtain set of keywords and fix their order
user_folders = ['sent']
keyword_set = set()
for user in users:
    for folder in user_folders:
        if os.path.exists(directory + user + '/' + folder) is False:
            break
        
        fileList = os.listdir(directory + user + '/' + folder)
        for file in fileList:
            fp = open(directory + user + '/' + folder + '/' + file, 'r')

            for ii in range(16):
                fp.readline()

            tokens_raw = word_tokenize(fp.read())
            tokens = [w.lower() for w in tokens_raw if w.lower() not in stop_words] 
            keyword_set.update(set(tokens))

keywords = list(keyword_set)
    

print(len(keywords))
print(keywords[0])
print(keywords[1])
