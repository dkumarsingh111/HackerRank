#Welcome to Operations on Arrays 1

import numpy as np

# Enter your code here. Read input from STDIN. Print output to STDOUT
def array_oper(num1,num2):
       
    y= np.arange(num1,num2+1)
    print(y)
    y=y.reshape(2,3)
    y=y**2
    y=y+5
    print(y)
    
    

if __name__ == "__main__":
    num1 = int(input())
    num2 = int(input())
    array_oper(num1,num2)