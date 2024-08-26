#Welcome to Statistics with Python | 5 | Hypothesis Testing 2

#!/bin/python3

#Write your code here
from scipy import stats

def perform_ttest(sample1, sample2):
    
    # Task 1:
    # A researcher noted the number of chocolate chips consumed by 10 rats, with and without electrical stimulation.
    # Compute t-statistic for the above samples, and return the t-score and p-value.
    
    t_score, p_value = stats.ttest_rel(sample1, sample2)
    
    """
    
    - The samples represent the number of chocolate chips consumed by 10 rats. `sample1` represents consumption with stimulation, and `sample2` without simulation.
    - Hint: Use the ttest_rel function available in scipy.

    Parameters
    ----------
    sample1 - list
        sample represents chocolate chips consumption with stimulation
    sample2 - list
        sample represents chocolate chips consumption without stimulation
    
    Returns
    -------
    t_score : float
        t-score of t-test 
    p_value: float
        p-value of t-test 
    """
    return t_score, p_value
