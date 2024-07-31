#Lab 1 : Try it Out - Array Creation [Welcome to Array Creation - Hands-on]

import numpy as np

# Enter your code here. Read input from STDIN. Print output to STDOUT


def array_operations(l):
    #Write your code below
    x = np.array(l)
    
    print(type(x))
    print(x.ndim)
    print(x.shape)
    print(x.size)
    
    

if __name__ == "__main__":
    l = list(map(int,input().split()))
    array_operations(l)