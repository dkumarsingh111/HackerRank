#Welcome to Statistics with Python | 4 | Hypothesis Testing 1.

#!/bin/python3

#Write your code here

from scipy import stats

def perform_ttest(sample1, sample2):

    # Task 1:
    # Consider two independent samples are passed as parameter to this.
    # Compute t-statistic for the above two groups, and return the t-score and p value.

    t_score, p_value = stats.ttest_ind(sample1, sample2)
    
    
    """
   
    - The samples represent the life satisfaction score (computed through a methodology) of older adults and younger adults respectively.
    - Hint: Use the ttest_ind function available in scipy.

    Parameters
    ----------
    sample1 - list
        sample values of age taken from the group1
    sample2 - list
        sample values of age taken from the group2
    
    Returns
    -------
    t_score : float
        t-score of t-test 
    p_value: float
        p-value of t-test 
    """
    return t_score, p_value