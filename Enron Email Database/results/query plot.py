import os
import matplotlib.pyplot as plt


# find all the folders and set up nltk
directory  = "./"
files      = ['1', '5', '10', '20', '50', '100']

plt.title('Percentage of emails returned by single keyword queries')
plt.ylabel('Percentage')

for file in files:
    fp = open(directory + file, 'r')
    freq_text = fp.readline().split(',')
    fp.close()
    freq = [float(freq_text[ii]) for ii in range(len(freq_text))]
    plt.plot(freq, label=file)
plt.legend()
plt.show()

