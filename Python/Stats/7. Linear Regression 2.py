#Welcome toStatistics with Python | 7 | Linear Regression 2

#!/bin/python3

#Write your code here
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd
import numpy as np

def build_lr():
    # Task 1: Load the R dataset mtcars and capture the data as a pandas dataframe.
    mtcars_dataset = sm.datasets.get_rdataset("mtcars", "datasets")
    mtcars_data = mtcars_dataset.data
    df = pd.DataFrame(mtcars_data)
    
    # Task 2: Build a linear regression model with the log of independent variable `wt`, and log of dependent variable `mpg`.
    x = 'wt'
    y = 'mpg'
    model = smf.ols(formula= f'np.log({y}) ~ np.log({x})', data=mtcars_data).fit()
    
    # Task 3: Fit the model with data, and return the R-squared value as float.
    r_squared= float(model.rsquared) # it will also work.

    
    """
    Returns
    -------
    r_squared : float
        r-squared value of the trained linear regression model
    """
    return r_squared