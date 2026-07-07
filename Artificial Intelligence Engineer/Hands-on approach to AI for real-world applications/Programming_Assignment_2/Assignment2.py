# ==========================================================
# IIT KHARAGPUR AI4ICPS HUB FOUNDATION
# Hands-on Approach to AI, Cohort-4, November 2025
# Programming Assignment 2
# Assignment submitted by Deepak Singh
# ==========================================================

import sys
import numpy as np

def advanced_numpy_calculator(x):
    """
    Perform a mathematical calculation based on the value of x.
    Students should only modify this function.
    Output is rounded to 4 decimal places.
    """
    if x < 0:
        return np.exp(x)
    
    elif x >= 0 and x < 10:
        radians = np.radians(x)
        return (np.sin(radians) + np.cos(2 * radians))
    
    elif x >= 10 and x < 50:
        log1p_x = np.log1p(x)
        sqrt_x = np.sqrt(x)
        return (log1p_x * sqrt_x)

    elif x >= 50 and x < 100:
        return np.linalg.det(np.array([[x, x/2], [x/3, x/4]]))

    elif x >= 100:
        coeffs = [1, -2, 3, -4]
        return np.polyval(coeffs, x)



def main():
    if len(sys.argv) != 2:
        print("Usage: python assignment2.py <number>")
        sys.exit(1)

    try:
        x = float(sys.argv[1])
    except ValueError:
        print("Please enter a valid number.")
        sys.exit(1)

    result = advanced_numpy_calculator(x)
    print(f"Output from main: {result:.4f}\n")

if __name__ == "__main__":
    main()
