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

# obtain documents
user_folders = ['sent/'] #, 'sent_items/']
d_user = []
for user in users:
    print(user)
    for folder in user_folders:
        fileList = os.listdir(directory + user + '/' + folder)
        for file in fileList:
            fp = open(directory + user + '/' + folder + '/' + file, 'r')
            
            # skip unwanted lines
            document = []
            line = fp.readline()
            while 'Subject' not in line:
                line = fp.readline()
            line = fp.readline()
            while 'Subject' not in line:
                line = fp.readline()
            
            tokens = word_tokenize(line)
            tokens.extend(word_tokenize(fp.read()))
            document = list(set(tokens))
            document = [w.lower() for w in document if w.lower() not in stop_words]
            d_user.append(document)
    break


print(d_user[1])
            
