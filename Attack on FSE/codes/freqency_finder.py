from collections import Counter
import math

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

# get two columns of the database as pairs
def get_pairs(db, col1, col2):
        pairs = []
        for ii in range(len(db)):
                pairs.append((db[ii][col1], db[ii][col2]))

        return(pairs)

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
			lower = math.floor(2**r_min * cdf)
			upper = math.floor(2**r_min * (cdf + hist[ii][jj][1])) - 1
			range_local.append([hist[ii][jj][0], int(lower), int(upper)])
			cdf = cdf + hist[ii][jj][1]
		
		ranges.append(range_local)

	return(ranges)

# from ranges work out the number of 'urns' for given pairs
def get_sizes(ranges, col1, col2):
        sizes = []
        att1 = ranges[col1]
        att2 = ranges[col2]

        for ii in range(len(att1)):
                for jj in range(len(att2)):
                        area = (att1[ii][2] - att1[ii][1] + 1) * (att2[jj][2] - att2[jj][1] + 1)
                        sizes.append([(att1[ii][0], att2[jj][0]), area])

        return sizes

def get_dist(pairs, sizes):
        dist = []

        for ii in range(len(pairs)):
                idx = 0
                for jj in range(len(sizes)):
                        if pairs[ii][0] == sizes[jj][0]:
                                idx = jj
                                break
                mean = float(pairs[ii][1]) / float(sizes[idx][1])
                var  = float(pairs[ii][1]) / float(sizes[idx][1]) * (1 - 1/float(sizes[idx][1]))
                dist.append([pairs[ii][0], mean, var])

        return(dist)

# main code
col1 = 0
col2 = 1
new_db = get_file()
hist = get_histogram(new_db)
ranges = get_ranges(hist)
pairs = Counter(get_pairs(new_db, col1, col2)).items()
sizes = get_sizes(ranges, col1, col2)
dist = get_dist(pairs, sizes)

			

