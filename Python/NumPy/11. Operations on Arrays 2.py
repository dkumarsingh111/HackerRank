#Welcome to Operations on Arrays 2

import numpy as np

# Enter your code here. Read input from STDIN. Print output to STDOUT
def array_oper(num1,num2):
    
    np.random.seed(100)
    r=np.random.randint(num1,num2,  30).reshape(5,6)
    x= np.sum(r,axis=0)
    y=np.sum(r,axis=1)
    print(x[-1])
    print(y[-1]) 
    
    
    

if __name__ == "__main__":
    num1 = int(input())
    num2 = int(input())
    array_oper(num1,num2)