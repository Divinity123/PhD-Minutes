# read in csv file
edb = read.csv("edb.csv")

# plot to show correctness of implementation
hist(edb[,1], breaks = seq(0, 256, 32), xlab='Risk mortality', main='Plaintext frequency')
x11()
hist(edb[,2], breaks = seq(0, 256, 32), xlab='Illness severity', main='Plaintext frequency')
x11()

# plot to show correlation is still preserved
size = 10000
plot(edb[1:size,1], edb[1:size,2], xlab='Risk mortality', ylab='Illness severity')