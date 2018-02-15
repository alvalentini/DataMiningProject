import matplotlib.pyplot as plt
#lsh
plt.plot([5000, 15000, 25000, 35000, 45000, 70000, 100000], [8.85, 25.94, 43.20, 62.66, 82.38, 148.04, 226.20], 'ro-', label="clustering with lsh")
#no lsh
plt.plot([5000, 15000, 25000, 35000, 45000, 70000, 100000], [3.26, 17.58, 43.20, 81.56, 132.54, 330.43, 633.01], 'bo-', label="normal clustering")
#plt.axis([0, 6, 0, 20])
plt.title('Execution time')
plt.legend(loc='upper left')
plt.ylabel('Time (seconds)')
plt.xlabel('Number of tweets')
#plt.plot(x,y,'bo-',markevery=100)
plt.tight_layout()
plt.show()



