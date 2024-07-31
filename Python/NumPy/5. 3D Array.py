# Welcome to Python - 3D Array - Hands-on

import numpy as np

# Enter your code here. Read input from STDIN. Print output to STDOUT
def array_3d(n, x, y, z):
    #Write your code below
    
    np.random.seed(100)
    x1 = 5 + 2.5*np.random.randn(n) # random normal distribution with mean=5 and standard deviation=2.5
    A=x1.nbytes
    
    m = np.random.uniform(0,1,x*y*z)
    x2 = m.reshape(x,y,z)
    print(A)
    print(x2)
    

if __name__ == "__main__":
    n=int(input())
    x, y, z=list(map(int,input().split()))
    array_3d(n, x, y, z)