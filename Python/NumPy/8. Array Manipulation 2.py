#Welcome to Array Manipulation2

import ast
import numpy as np

# Enter your code here. Read input from STDIN. Print output to STDOUT
def array_split(n,n_row,n_col):
    
    x =np.arange(n)
    z= np.array(x, ).reshape(n_row,n_col)
    a,b=np.vsplit(z,2)
    print(a)
    print(b)
    
    

if __name__ == "__main__":
    n = ast.literal_eval(input())
    n_row = ast.literal_eval(input())
    n_col = ast.literal_eval(input())
    array_split(n,n_row,n_col)