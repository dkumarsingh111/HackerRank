#Welcome to Statistics with Python | 11 | ANOVA 2.

#!/bin/python3

#Write your code here

import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats import anova
import numpy as np
import pandas as pd
def build_anova():
	# Task 1: Load the R dataset `mtcars`. and capture the data as a pandas dataframe.
    mtcars_dataset = sm.datasets.get_rdataset("mtcars", "datasets")
    mtcars_data = mtcars_dataset.data
    df = pd.DataFrame(mtcars_data)
    
    # Task 2: Build a linear regression model by considering the `log` of independent variable `wt`, and log of dependent variable mpg.
    model=  smf.ols(formula='np.log(mpg) ~ np.log(wt)', data=df).fit()
    
    # Task 3: Fit the model with data, and perform ANOVA on the linear model. (Hint:Use anova.anova_lm)
    f1_score= float(anova.anova_lm(model).F["np.log(wt)"])
    
    """
    - Return the F-statistic value as a float

    Returns
    -------
    f1_score : float
       F-statistic value of the ANOVA model
    """
    return f1_score
