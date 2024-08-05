#Welcome to Array Indexing

import numpy as np

# Enter your code here. Read input from STDIN. Print output to STDOUT
def array_index(n,n_row,n_col):
    x=  np.arange(n).reshape(n_row,n_col)
    
    print(x[-1])
    print(x[:,2])
    print(x[ :2, 2:])
    

if __name__ == '__main__':
    n = int(input())
    n_row = int(input())
    n_col = int(input())
    array_index(n,n_row,n_col)