#Welcome to Statistics with Python | 3 | Random Experiment.

#!/bin/python3

#Write your code here

import sys
import numpy as np
from scipy.stats import binom

def count_random_heads(number_sample, random_state):
    # Simulate a random experiment of tossing a coin n times, and determine the count of Heads returned.
    
    # Task 1: Use binom function from scipy.stats and Set the random state as `random_state'.
    np.random.seed(random_state)

    # Task 2: Draw a sample of `number_sample` elements from a defined distribution. Assume that the values '0' and '1' represent Heads and Tails respectively.
    data_binom = binom.rvs(n=1,p=0.5,size=number_sample)

    # Task 3: Count the number of 'Heads' and return it.
    y = np.bincount(data_binom)
    head_count = y[0]

    """
    Parameters
    ----------
    number_sample - int
        number_sample represents that the number of times the experiments repeats
    random_state - int
        number_sample represents seed/state value for the randomness    

    Returns
    -------
    head_count : int
        Count the number of 'Heads' 
    """
    return head_count