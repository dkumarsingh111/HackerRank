#Lab-3: Welcome to Python - ndarray - hands-on

import numpy as np

# Enter your code here. Read input from STDIN. Print output to STDOUT

def ndarray(array_input):
    #Write your code here
    x1=np.array(array_input)
   
    print(x1.ndim)
    print(x1.shape)
    print(x1.size)
    
    

if __name__ == "__main__":

    s = input()
    if s == "a":
        array_input = [[[-1, 1], [-2, 2]],
        [[-3, 3], [-4, 4]],
        [[-3, 3], [-4, 4]]]

    elif s == "b":
        array_input = [[[-1, 1], [-2, 2]],
        [[-3, 3], [-4, 4]]]
        
    elif s == "c":
        array_input = [[[-1, 1], [-2, 2], [-2, 2]],
        [[-3, 3], [-4, 4], [-2, 2]],
        [[-1, 1], [-2, 2], [-2, 2]]]

    elif s == "d":
        array_input = [[[[-1, 1], [-2, 2]],
        [[-3, 3], [-4, 4]]],
        [[[-1, 1], [-2, 2]],
        [[-3, 3], [-4, 4]]]]

    elif s == "e":
        array_input = [[[[[-1, 1], [-2, 2]],
        [[-3, 3], [-4, 4]]],
        [[[-1, 1], [-2, 2]],
        [[-3, 3], [-4, 4]]]],
        [[[[-1, 1], [-2, 2]],
        [[-3, 3], [-4, 4]]],
        [[[-1, 1], [-2, 2]],
        [[-3, 3], [-4, 4]]]]]

    ndarray(array_input)