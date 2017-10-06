from collections import Counter
import math
from random import randint

# function to get part of the database (for simplicity)
def get_file():
	fields_name = ['249: Risk_mortality', '250: Illness_severity']
	fields = [249, 250]

	new_file = []
	with open('PUDF_base1q2010_tab.txt', 'r') as file:
		file.next()
		for line in file:
			line = line.split('\t')
			new_line = []
			for ii in range(len(fields)):
				new_line.append(line[fields[ii]])
			new_file.append(new_line)

	return(new_file)


# get histogram on the selected columns
def get_histogram(array):
	x = len(array)
	y = len(array[0])

	new_array = [[0 for ii in range(x)] for jj in range(y)]

	for ii in range(x):
		for jj in range(y):
			new_array[jj][ii] = array[ii][jj]

	hist = []
	for ii in range(len(new_array)):
		attrib_hist_raw = Counter(new_array[ii]).items()
		attrib_hist = []
		for jj in range(len(attrib_hist_raw)):
			attrib_hist.append([attrib_hist_raw[jj][0], float(attrib_hist_raw[jj][1]) / x])
		hist.append(attrib_hist)
	
	return(hist)

# assign endpoints of encryption for each column
def get_ranges(hist):
	ranges = []
	for ii in range(len(hist)):
		freq = []
		for jj in range(len(hist[ii])):
			freq.append(hist[ii][jj][1])
		freq.sort()
		r_min = int(max(math.ceil(-math.log(freq[0], 2)), math.ceil(-math.log(freq[1], 2))))

		range_local = []
		cdf = 0

		for jj in range(len(hist[ii])):
			lower = math.ceil(2**r_min * cdf)
			upper = math.ceil(2**r_min * (cdf + hist[ii][jj][1])) - 1
			range_local.append([hist[ii][jj][0], lower, upper])
			cdf = cdf + hist[ii][jj][1]
		
		ranges.append(range_local)

	return(ranges)


# function to encrypt an entry given its column number and its encryption interval
def enc(val, col, ranges):
	range_local = ranges[col]

	idx = 0
	for ii in range(len(range_local)):
		if range_local[ii][0] == val:
			idx = ii
			break

	if range_local[idx][1] == range_local[idx][2]:
		return(range_local[idx][1])
	else:
		return(randint(range_local[idx][1], range_local[idx][2]))

# function to encrypt the entire database
def enc_db(db, ranges):
	edb = []

	for ii in range(len(db)):
		row = []
		for jj in range(len(db[0])):
			row.append(enc(db[ii][jj], jj, ranges))

		edb.append(row)
	
	return(edb)


# output the encrypted database as csv
def output_edb(edb):
	edb_file = open('edb.csv', 'w')

	edb_file.write('Risk_mortality,Illness_severity\n')
	for ii in range(len(edb)):
		for jj in range(len(edb[0])-1):
			edb_file.write('%d,' %(edb[ii][jj]))
		edb_file.write('%d\n' %(edb[ii][len(edb[0])-1]))

	edb_file.close()

# main code
new_db = get_file()
hist = get_histogram(new_db)
ranges = get_ranges(hist)
edb = enc_db(new_db, ranges)
output_edb(edb)

			

