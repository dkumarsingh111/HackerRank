#Welcome to Join Arrays - Hands-on

import ast
import numpy as np

# Enter your code here. Read input from STDIN. Print output to STDOUT
def join_array(list1,list2):
    
    p= np.array(list1).reshape(2,2)
    q= np.array(list2).reshape(2,3)

    print(np.hstack((p,q))) 
    

if __name__ == "__main__":
    l1 = ast.literal_eval(input())
    l2 = ast.literal_eval(input())
    join_array(l1,l2)