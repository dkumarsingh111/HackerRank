#Lab 2: Welcome to Python Array - Determine Attributes - Hands-on

import numpy as np

# Enter your code here. Read input from STDIN. Print output to STDOUTd

def array_attributes(l):
    #write your code here
    
    y = np.array(l)
    
    # Type of the Array
    print(type(y))
    
    # Dimensions of y
    print(y.ndim)
    
    #Shape of y
    print(y.shape)
    
    # Size of y
    print(y.size)
    
    # Type of each data element of y
    print(y.dtype)
    
    #Number of Bytes occupied by each data element of y
    print(y.itemsize)  
    
    

if __name__=="__main__":
    r=int(input())
    l=[]
    for i in range(r):
        n = list(map(int,input().split()))
        l.append(n)
    array_attributes(l)