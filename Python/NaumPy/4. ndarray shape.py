#Lab-4: Welcome to Python - ndarray shape - Hands-on

import numpy as np

# Enter your code here. Read input from STDIN. Print output to STDOUT
def ndshape(d, shape1):
    #Write your code here
    
    x1 = np.eye(d)
    print(x1)
    
    x2 = np.ones(shape1)
    print(x2)

if __name__ == "__main__":
    d=int(input())
    shape1=list(map(int,input().split()))
    ndshape(d, shape1)