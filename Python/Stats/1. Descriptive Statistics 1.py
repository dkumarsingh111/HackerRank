#Welcome to Statistics with Python | 1 | Descriptive Statistics

#Write your code here
import numpy as np
from scipy import stats
def compute_descriptive_stats(data):
    sample = np.array(data)
    '''
    Compute the following statistical parameters, and retun them
    '''
    # Task 1:
    # Calculate Mean value for the given parameter 'data'.
    mean = np.mean(sample)
    
    # Task 2:
    # Calculate Median value for the given parameter 'data'.
    median = np.median(sample)
    
    # Task 3:
    # Calculate Mode value for the given parameter 'data'.
    mode = stats.mode(sample)[0]
    
    # Task 4:
    # Calcuate 25th and 75th percentile value for given parameter `data` and return as a numpy array.
    percentile = np.percentile(sample, [25, 75], interpolation='lower')
    
    # Task 5:
    # Calcuate Inter quartile range value for given parameter `data`
    iqr = stats.iqr(sample, interpolation='lower')
    
    # Task 6:
    # Calcuate Skewness value for given parameter `data`
    skew = stats.skew(sample)
    
    # Task 7
    # Calcuate Kurtosis value for given parameter `data`
    kutrosis = stats.kurtosis(sample)
    
    """
    Returns
    -------
    mean : float
        Mean value for the sample data `data`
    median : float
        Median value for the sample data `data`
    mode : int
        Mode value for the sample data `data`
    percentile : list
        25th and 75th percentile values for the sample data `data`
    iqr : float
        Inter quartile range value for the sample data `data`
    skew : float
        Skewness value for the sample data `data`
    kutrosis : float
        Kurtosis value for the sample data `data`
    """
    return mean, median, mode, percentile, iqr, skew, kutrosis