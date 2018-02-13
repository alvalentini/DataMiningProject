import matplotlib.pyplot as plt
#lsh
plt.plot([5000, 15000, 25000, 35000, 45000], [133.656, 256.376, 349.724, 480.184, 572.376], 'ro-', label="clustering with lsh")
#no lsh
plt.plot([5000, 15000, 25000, 35000, 45000], [84.172, 100.752, 117.284, 134.480, 148.704], 'bo-', label="normal clustering")
#plt.axis([0, 6, 0, 20])
plt.title('Maximum memory usage')
plt.legend(loc='upper right')
plt.ylabel('Memory (MB)')
plt.xlabel('Mumber of tweets')
#plt.plot(x,y,'bo-',markevery=100)
plt.show()



