#Welcome to Statistics with Python | 9 | Poisson Regression.

#!/bin/python3

#Write your code here
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
import pandas as pd

def build_pos_reg():
    
    # Task 1: Load the R dataset biopsy from the MASS package and capture the data as a pandas dataframe.
    Insurance_dataset = sm.datasets.get_rdataset("Insurance", "MASS")
    Insurance_data = Insurance_dataset.data
    df = pd.DataFrame(Insurance_data)
    
    # Task 2: Build a Poisson regression model with a log of an independent variable `Holders`, and dependent variable `Claims`
    Insurance_data['Holders_New'] = np.log(Insurance_data['Holders'])
    poisson_model = smf.poisson('Claims ~ Holders_New', Insurance_data).fit()
    
    # Task 3: Fit the model with data, and return the sum of the residuals as float.
    residuals_sum= float(np.sum(poisson_model.resid) )
 
    
    """
    Returns
    -------
    residuals_sum : float
        sum of the residuals for the trained poission regression model
    """
    return residuals_sum
