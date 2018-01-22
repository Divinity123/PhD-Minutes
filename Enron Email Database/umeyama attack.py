import numpy as np
import scipy.optimize as optimize

# load input and compute eigven values and eigen vectors
directory = './output/test'
raw = np.loadtxt(directory, skiprows=1, delimiter=',')
eigenVal_raw, eigenVec_raw = np.linalg.eig(raw)
idx = eigenVal_raw.argsort()[::-1]
eigenVal_raw = eigenVal_raw[idx]
eigenVec_raw = eigenVec_raw[:,idx]
eigenVec_raw = np.absolute(eigenVec_raw)


# performs permutation on the co-occurrence matrix
# and compute the corresponding eigven values and eigen vectors
permutation = np.arange(len(eigenVal_raw))
permutation = np.random.permutation(permutation)
permuted = raw[permutation][:,permutation]
eigenVal_permuted, eigenVec_permuted = np.linalg.eig(permuted)
idx = eigenVal_permuted.argsort()[::-1]
eigenVal_permuted = eigenVal_permuted[idx]
eigenVec_permuted = eigenVec_permuted[:,idx]
eigenVec_permuted = np.absolute(eigenVec_permuted)

# compute H*(G^T)
product = np.matmul(eigenVec_permuted, np.transpose(eigenVec_raw))


# apply Hungarian method to find the permutation
profit = np.ones(np.shape(product)) * product.max()
profit = profit - product
idx = optimize.linear_sum_assignment(profit)


# report accuracy of attack
guess = np.zeros(len(eigenVal_raw))
for ii in range(len(eigenVal_raw)):
    guess[idx[0][ii]] = idx[1][ii]

correct = 0
for ii in range(len(guess)):
    if guess[ii] == permutation[ii]:
        correct = correct + 1
print('Percentage of correct guesses: %.2f %%' %(correct / len(guess) * 100))

