# ==========================================================
# IIT KHARAGPUR AI4ICPS HUB FOUNDATION
# Hands-on Approach to AI, Cohort-4, November 2025
# Programming Assignment 1
# Assignment submitted by Deepak Singh
# ==========================================================

import sys

# ----------------------------------------------------------
# Function: frac
# Description: Computes the factorial of a number recursively.
# You are allowed to edit inside this function only.
# ----------------------------------------------------------
def frac(n):
    # TODO: Implement the recursive factorial function
    if n <= 1:
        return 1
    return n * frac(n - 1)


# ----------------------------------------------------------
# Function: series
# Description: Computes the alternating factorial series
# S = Σ (-1)^(k+1) * (frac(k)^2) / (frac(k) + k)
# ----------------------------------------------------------
def series(ip):
    # TODO: Implement the logic for computing the series
    if ip < 0:
        return 999.0

    total = 0.0
    for k in range(1, ip + 1):
        term = (-1)**(k+1) * (frac(k)**2) / (frac(k) + k)
        total += term

    return f"{round(total, 2):.2f}"


# ----------------------------------------------------------
# Main function: DO NOT MODIFY
# ----------------------------------------------------------
if __name__ == "__main__":
    ip = int(sys.argv[1])
    print(series(ip))
    