#Welcome to Slicing

import numpy as np

# Enter your code here. Read input from STDIN. Print output to STDOUT
def array_slice(n,n_dim,n_row,n_col):
    
    
    x= np.arange(n).reshape(n_dim,n_row,n_col)    
    b=np.array([True, False])
    print(x[b])
    print(x[b,:,1:3])
    
    

if __name__ == '__main__':
    n = int(input())
    n_dim = int(input())
    n_row = int(input())
    n_col = int(input())
    array_slice(n,n_dim,n_row,n_col)