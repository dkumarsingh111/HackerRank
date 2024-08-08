#Which of the following statements is correct, based on figure generated with below code?


import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111, title="My Plot")
x = [0, 1, 2, 3, 4]
y = [0, 3, 6, 9, 12]
plt.scatter(x, y, s=[20, 60], c=['r', 'g'])
plt.show()


# A. Alteranative data points are marked with different color and size
# Answer: B. Results in Error
# C. All data points are marked in green color with size 60
# D. All data points are marked in red color with size 20   