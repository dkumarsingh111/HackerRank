# ==========================================================
# IIT KHARAGPUR AI4ICPS HUB FOUNDATION
# Hands-on Approach to AI, Cohort-4, November 2025
# Programming Assignment 1
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
    pass

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
