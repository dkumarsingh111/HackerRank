#Welcome to Statistics with Python | 6 | Linear Regression 1

#!/bin/python3

#Write your code here

# from collections.abc import KeysView
# from nltk.lm import models
import statsmodels.api as sm
# import statsmodels.formula.api as smf
import pandas as pd
# import numpy as np
# from statsmodels.stats import anova

def build_lr():
    # Task 1: Load the R dataset mtcars and capture the data as a pandas dataframe.
    #
    mtcars_dataset = sm.datasets.get_rdataset("mtcars", "datasets")
    mtcars_data = mtcars_dataset.data
    df = pd.DataFrame(mtcars_data)
    
    # Task 2: Build a linear regression model with independent variable `wt`, and dependent variable `mpg`.
    # df = df[['mpg','wt']]
    x = sm.add_constant(df['wt'])
    y = df['mpg']
    model = sm.OLS(y, x).fit()
    
    # Task 3: Fit the model with data, and return the R-squared value as float.
    r_squared= float(model.rsquared)

    """
    Returns
    -------
    r_squared : float
        r-squared value of the trained linear regression model
    """
    return r_squared