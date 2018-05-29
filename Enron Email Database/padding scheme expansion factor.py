import os
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import words as nltk_words
import random
import time


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
        partial_documents.append((documents[document_set[jj]][0], keyword_set))
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
t0 = time.clock()
c = 10
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


# ------------------------------------------------------------------- #
# preprocessing to remove most frequent words
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
most_frequent = [linked_frequency[ii][0] for ii in range(most_frequent)]
keyword_set = keyword_set.difference(most_frequent)

# update keyword index for the documents
for ii in range(len(documents)):
    documents[ii] = (documents[ii][0], documents[ii][1].intersection(keyword_set))
    

# ------------------------------------------------------------------- #
# actual padding scheme
# c - size of cycle
tmp_count = 0
while len(keyword_set) % c is not 0:
    keyword_set.add('null' + str(tmp_count))
    tmp_count = tmp_count + 1


# generate keyword list
keyword_list = list(keyword_set)
index_set = [ii for ii in range(len(keyword_list))]
print('No. of keywords (processed): %d.' %(len(keyword_list)))

t1 = time.clock() - t0
print('Time spent: %d (s)' %(t1))


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

# ----------------------------------------------------------------
# get ready to compute new frequency of keywords
index = {}
for ii in range(len(keyword_list)):
    index[keyword_list[ii]] = ii
frequency = [0 for ii in range(len(keyword_set))]

# ----------------------------------------------------------------
# pick c documents at random and perform padding, processed documents are thrown away to save memory
kw_size_padded = 0
secure_random = random.SystemRandom()

tmp_count = 0
while len(documents) % c is not 0:
    documents.append(('null'+str(tmp_count), set()))
    tmp_count = tmp_count + 1
index_set = [ii for ii in range(len(documents))]

while len(index_set) > 0:
    # randomly select c documents
    document_set = []
    for tmp in range(c):
        idx = secure_random.choice(index_set)
        document_set.append(idx)
        index_set.remove(idx)

    # compute set of keywords for each document, retain keyword counts
    padded_documents = pad_documents(documents, document_set, random_cycles, c)
    kw_size_padded = kw_size_padded + sum([len(padded_documents[ii][1]) for ii in range(len(padded_documents))])

    # accumulate keyword frequencies
    for doc in padded_documents:
        for keyword in doc[1]:
            frequency[index[keyword]] = frequency[index[keyword]] + 1

# ----------------------------------------------------------------
# post-processing frequency information
file_size = len(documents)
for ii in range(len(frequency)):
    frequency[ii] = frequency[ii] / file_size * 100

# link frequency to keywords
linked_frequency = [(keyword_list[ii],frequency[ii]) for ii in range(len(frequency))]
linked_frequency = sorted(linked_frequency, key=lambda linked: linked[1], reverse=True)

# ----------------------------------------------------------------
# print number of keywords in real documents, padded documents, and expansion factor
kw_size = sum([len(documents[ii][1]) for ii in range(len(documents))])
print("Number of keywords before padding: %d" %(kw_size))
print("Number of keywords after padding: %d" %(kw_size_padded))
print("Expansion factor: %f" %(kw_size_padded / kw_size))

t1 = time.clock() - t0
print('Time spent: %d (s)' %(t1))


# ----------------------------------------------------------------
# write frequencies to file
file_name = './results/' + str(c) + '.txt'
fp = open(file_name, 'w')
frequency = [linked_frequency[ii][1] for ii in range(len(linked_frequency))]
for ii in range(len(linked_frequency)-1):
    fp.write('%f,' %(frequency[ii]))
fp.write('%f\n' %(frequency[-1]))
fp.close()


