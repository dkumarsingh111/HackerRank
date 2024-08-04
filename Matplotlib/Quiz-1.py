#What is the expected output of the following code?


import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot([10, 12, 14, 16])
plt.show()

#Output: A line passing through points : (0, 10), (2, 14)