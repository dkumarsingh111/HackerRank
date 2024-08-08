#Welcome to Matplotlib -4 - Histograms and Box Plots

import numpy as np
import matplotlib.pyplot as plt


def hist_of_a_sample_normal_distribution():

    # Write your functionality below

    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111)

    np.random.seed(100)  
    dist_arr = 35 + 3.0*np.random.randn(1000)

    ax.set(title="Histogram of a Single Dataset",
      ylabel='Bin Count', xlabel='dist_arr')
    
    ax.hist(dist_arr, bins=35, density=True)
    

    return None


def boxplot_of_four_normal_distribution():

    # Write your functionality below
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111)

    np.random.seed(100)  
    arr_1 = 35 + 6.0*np.random.randn(2000)
    arr_2 = 25 + 4.0*np.random.randn(2000)
    arr_3 = 45 + 8.0*np.random.randn(2000)
    arr_4 = 55 + 10.0*np.random.randn(2000)

    ax.set(title="Box plot of Multiple Dataset",
      ylabel='Value', xlabel='Dataset')
    
    ax.boxplot([arr_1, arr_2, arr_3, arr_4], labels = ['arr_1', 'arr_2', 'arr_3', 'arr_4'], notch=True, bootstrap=10000, patch_artist=True, )

    return fig


# Note: Do Not modify the below code
if __name__ == '__main__':
    import sys
    import subprocess
    # subprocess.check_call(
    #     [sys.executable, "-m", "pip", "install", 'test_plot4-0.1-py3-none-any.whl'], stdout=subprocess.DEVNULL)
    # from test_plot4 import matplotlib4
    usr_fig1 = hist_of_a_sample_normal_distribution()
    usr_fig2 = boxplot_of_four_normal_distribution()
    #matplotlib4.save_answer(usr_fig1, usr_fig2)
