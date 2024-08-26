#Welcome to Statistics with Python | 2 | Random Distributions

#!/bin/python3

#Write your code here
from scipy import stats 
import numpy as np 

def compute_absolute_difference(mean, std, seed):
    #Task 1:
    # Create a normal distribution with  mean of `mean` and standard deviation of `std`.
    normal_distribution = stats.norm(loc=mean, scale=std)

    # Task 2:
    # Set the random seed of `seed`, and create a random sample of 100 elements from the above defined distribution.
    np.random.seed(seed)
    random_sample = normal_distribution.rvs(100)
    
    # Task 3:
    # Compute the absolute difference between the sample mean and the distribution mean.
    distribution_mean = np.mean(random_sample)
    absolute_difference = distribution_mean - mean


    """
    Parameters
    ----------
    mean - float
        mean value for the normal distribution
    std - float
        standard deviation value for the normal distribution
    seed - int
        seed valure for randomness
    
    Returns
    -------
    absolute_difference : float
        absolute difference between the sample mean and the distribution mean.
    """
    return absolute_difference