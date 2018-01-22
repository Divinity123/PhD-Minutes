import os
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import random


# method to get keyword set for the last document in the set
def pad_documents(documents, document_set, random_cycles, c):
    # gather keyword sets
    keyword_sets = []
    for idx in document_set:
        keyword_sets.append(documents[idx][1])

    # perform permutation on target sets of keywords to compute the keyword set for the last document
    keyword_set = set()
    for ii in range(c):
        keyword_set.update(permute(keyword_sets[ii], random_cycles, c-ii-1))

    # assign keywords to the documents
    partial_documents = []
    for ii in range(c):
        jj = (ii + c - 1) % c
        partial_documents.append((documents[document_set[jj]], keyword_set))
        keyword_set = permute(keyword_set, random_cycles, 1)

    return(partial_documents)


# method to permute a keyword set for a given number of times
def permute(keyword_set, random_cycles, times):
    new_keyword_set = set()
    for keyword in keyword_set:
        new_keyword = keyword
        for ii in range(times):
            new_keyword = random_cycles[new_keyword]
        new_keyword_set.add(new_keyword)
    return(new_keyword_set)

# ------------------------------------------------------------------- #
# main procedures
# find all the folders and set up nltk
directory  = "./DB/"
users      = os.listdir(directory)

nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))
stop_words.update(list(string.punctuation))
stop_words.update(['Subject', '--', '...'])


# obtain set of keywords
user_folders = ['sent']
documents = []
ctr = 0
for user in users:
    ctr = ctr+1
    prt_str = 'Users scanned: ' + str(ctr) + '/' + str(len(users))
    print(prt_str)
   
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
                        if t.lower() not in stop_words and t.isnumeric() is False:
                            tokens.add(t.lower())
                line = fp.readline()
                            
            documents.append((directory + user + '/' + folder + '/' + file, tokens))


# keep a copy of keyword set just in case
keyword_set = set()
for doc in documents:
    keyword_set.update(doc[1])
print('No. of keywords (raw): %d.' %(len(keyword_set)))


# optional pre-processing of most frequent keywords
most_frequent = 5000
frequency = {}
for keyword in keyword_set:
    frequency[keyword] = 0
    for document in documents:
        if keyword in document[1]:
            frequency[keyword] = frequency[keyword] + 1
frequency = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
frequency = frequency[0:most_frequent]

# reform keyword set
keyword_set = set()
for item in frequency:
    keyword_set.add(item[0])

# filter documents
filtered_documents = []
for document in documents:
    intersection = document[1].intersection(keyword_set)
    if len(intersection) > 0:
        filtered_documents.append((document[0], intersection))


# actual padding scheme
# c - size of cycle
c = 5
tmp_count = 0
while len(keyword_set) % c is not 0:
    keyword_set.add('null' + str(tmp_count))
    tmp_count = tmp_count + 1


# generate keyword list
keyword_list = list(keyword_set)
index_set = [ii for ii in range(len(keyword_list))]
print('No. of keywords (processed): %d.' %(len(keyword_list)))


# generate random cycles
secure_random = random.SystemRandom()
random_cycles = {}
while len(index_set) > 0:
    cycle = []
    for tmp in range(c):
        idx = secure_random.choice(index_set)
        cycle.append(idx)
        index_set.remove(idx)
    for ii in range(c):
        jj = (ii + 1) % c
        random_cycles[keyword_list[cycle[ii]]] = keyword_list[cycle[jj]] 


# pick c documents at random and perform padding
padded_documents = []
secure_random = random.SystemRandom()

tmp_count = 0
while len(filtered_documents) % c is not 0:
    filtered_documents.append(('null'+str(tmp_count), set()))
    tmp_count = tmp_count + 1
index_set = [ii for ii in range(len(filtered_documents))]

while len(index_set) > 0:
    # randomly select c documents
    document_set = []
    for tmp in range(c):
        idx = secure_random.choice(index_set)
        document_set.append(idx)
        index_set.remove(idx)

    # compute set of keywords for each document
    padded_documents = padded_documents + pad_documents(filtered_documents, document_set, random_cycles, c)


# ----------------------------------------------------------------
# put padded documents into an inverted index
index = {}
for keyword in keyword_set:
    index[keyword] = set()
    for document in padded_documents:
        if keyword in document[1]:
            index[keyword].add(document[0])



                


