#Welcome to Python - Array Manipulation 1 - Hands-on


import numpy as np

# Enter your code here. Read input from STDIN. Print output to STDOUT
def array_split(i,r,c):
    #Write your code below
    
    x=np.arange(i)
    y = np.array(x).reshape(r,c)    
    a,b = np.hsplit(y,2)
    print(a)
    print(b)
    

if __name__=="__main__":
    i=int(input())
    r,c = list(map(int,input().split()))
    array_split(i,r,c)