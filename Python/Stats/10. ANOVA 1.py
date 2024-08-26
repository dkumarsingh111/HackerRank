#Welcome to Statistics with Python | 10 | ANOVA 1.

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

    # Task 2: Build a linear regression model with independent variable `wt`, and dependent variable `mpg`
    mtcars_model = smf.ols('mpg ~ wt', mtcars_data).fit()

    # Task 3: Fit the model with data, and perform ANOVA on the linear model.(Hint:Use anova.anova_lm)
    f1_score= float(anova.anova_lm(mtcars_model).F["wt"])

    """
    - Return the F-statistic value as float.

    Returns
    -------
    f1_score : float
        F-statistic value of the ANOVA model
    """
    return f1_score