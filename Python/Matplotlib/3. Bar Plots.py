#Welcome to Matplotlib -3 - Bar Plots

import numpy as np
import matplotlib.pyplot as plt


def barplot_of_iris_sepal_length():

    # Write your functionality below
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111)

    species = ['setosa', 'versicolor', 'virginica']
    index = [0.4, 1.4, 2.4]
    sepal_len = [6.01, 6.94, 7.69]

    ax.bar(index, height=sepal_len, label='Sepal Length', width=0.4, color='blue', edgecolor='red')

    ax.set(title='Mean Sepal Length of Iris Species', 
          xlabel='Species', ylabel='Sepal Length (cm)',
          xlim=(0, 3), ylim=(0, 9))
    
    xticks = [0.4, 1.4, 2.4]
    xlables = ['setosa', 'versicolor', 'virginica']
    ax.set_xticks(xticks, xlables)
    plt.legend()
    #plt.show()
    return fig


def barplot_of_iris_measurements():

    # Write your functionality below
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111)

    sepal_len = [6.01, 6.94, 7.59]
    sepal_wd = [4.42, 3.77, 3.97]
    petal_len = [2.46, 5.26, 6.55]
    petal_wd = [1.24, 2.33, 3.03]
    species = ['setosa', 'versicolor', 'virginica']
    species_index1 = [0.7, 1.7, 2.7]
    species_index2 = [0.9, 1.9, 2.9]
    species_index3 = [1.1, 2.1, 3.1]
    species_index4 = [1.3, 2.3, 3.3]

    ax.bar(species_index1, height=sepal_len, label='Sepal Length', width=0.2, color='m', edgecolor='grey')
    ax.bar(species_index2, height=sepal_wd, label='Sepal Width', width=0.2, color='y', edgecolor='grey')
    ax.bar(species_index3, height=petal_len, label='Petal Length', width=0.2, color='c', edgecolor='grey')
    ax.bar(species_index4, height=petal_wd, label='Petal Width', width=0.2, color='orange', edgecolor='grey')

    ax.set(title='Mean Measurements of Iris Species', 
          xlabel='Species', ylabel='Iris Measurements (cm)',
          xlim=(0.5, 3.5), ylim=(0, 10))
    

    xticks = [1.0, 2.0, 3.0]
    xlables = ['setosa', 'versicolor', 'virginica']
    ax.set_xticks(xticks, xlables)
    plt.legend()
    #plt.show()

    return fig


def hbarplot_of_iris_petal_length():

    # Write your functionality below
    fig = plt.figure(figsize=(15, 5))
    ax = fig.add_subplot(111)

    species = ['setosa', 'versicolor', 'virginica']
    index = [0.1, 1.1, 2.1]
    petal_len = [2.67, 5.49, 6.37]

    ax.barh(index, petal_len, label='Petal Length', height=0.4, color='m', edgecolor='c')

    ax.set(title='Mean Petal Length of Iris Species', 
          xlabel='Petal Length (cm)', ylabel='Species')
    
    yticks = [0.10, 1.10, 2.10]
    ylables = ['setosa', 'versicolor', 'virginica']
    ax.set_yticks(yticks, ylables)
    plt.legend()
    #plt.show()
    return fig


# Note: Do Not modify the below code
if __name__ == '__main__':
    import sys
    import subprocess
    #subprocess.check_call(
    #    [sys.executable, "-m", "pip", "install", 'test_plot3-0.1-py3-none-any.whl'], stdout=subprocess.DEVNULL)
    #from test_plot3 import matplotlib3
    usr_fig1 = barplot_of_iris_sepal_length()
    usr_fig2 = barplot_of_iris_measurements()
    usr_fig3 = hbarplot_of_iris_petal_length()
    #matplotlib3.save_answer(usr_fig1, usr_fig2, usr_fig3)
