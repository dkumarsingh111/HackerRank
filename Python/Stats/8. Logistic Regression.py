#Welcome to Statistics with Python | 8 | Logistic Regression

#!/bin/python3

#Write your code here
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd

def build_log_reg():
    # Task 1: Load the R dataset biopsy from the MASS package and capture the data as a pandas dataframe.
    biopsy_dataset = sm.datasets.get_rdataset("biopsy", "MASS")
    biopsy_data = biopsy_dataset.data
    df = pd.DataFrame(biopsy_data)
    
    # Task 2: Rename the column name class to Class. 
    df = df.rename(columns={'class': 'Class'})
    
    # Task 3: Transform the Class column values benign and malignant to '0' and '1' respectively.
    df['Class'].replace(['benign','malignant'],[0,1] ,inplace=True)
    
    # Task 4: Build a logistic regression model with independent variable 'V1' and dependent variable 'Class'.
    
    model = smf.logit("Class ~ V1", data=df).fit()

    # Task 5: Fit the model with data, and return the pseudo R-squared value as float.    
    r_squared= float(model.prsquared)
    
    
    
    """
    Returns
    -------
    r_squared : float
        r-squared value of the trained logistic regression model
    """
    return r_squared
