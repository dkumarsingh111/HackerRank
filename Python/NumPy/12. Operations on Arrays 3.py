#Welcome to Operations on Arrays 3

import ast
import numpy as np

# Enter your code here. Read input from STDIN. Print output to STDOUT
def array_oper(n,m,sd):
    
    np.random.seed(100)
    
    x=m + sd*np.random.randn(n)
    print(np.mean(x))
    print(np.std(x))
    print(np.var(x))
    
    
    

if __name__ == '__main__':
    num = ast.literal_eval(input())
    mean = ast.literal_eval(input())
    sd = ast.literal_eval(input())
    array_oper(num,mean,sd)