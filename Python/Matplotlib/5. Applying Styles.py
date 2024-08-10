# Welcome to Matplotlib -5 - Applying Styles

import numpy as np
import matplotlib.pyplot as plt


def generate_plot_with_style1():

    # Write your functionality below

    with plt.style.context('ggplot'):
        fig = plt.figure(figsize=(9,7))
        ax = fig.add_subplot(111)

        sepal_len = [6.01, 6.94, 7.59]
        sepal_wd = [4.42, 3.77, 3.97]
        petal_len = [2.46, 5.26, 6.55]
        petal_wd = [1.24, 2.33, 3.03]
        species = ['setosa', 'versicolor', 'virginica']
        species_index1 = [0.8, 1.8, 2.8]
        species_index2 = [1.0, 2.0, 3.0]
        species_index3 = [1.2, 2.2, 3.2]
        species_index4 = [1.4, 2.4, 3.4]

        
        ax.bar(species_index1, height=sepal_len, label='Sepal Length', width=0.2)
        ax.bar(species_index2, height=sepal_wd, label='Sepal Width', width=0.2)
        ax.bar(species_index3, height=petal_len, label='Petal Length', width=0.2)
        ax.bar(species_index4, height=petal_wd, label='Petal Width', width=0.2)
    
        ax.set(title='Mean Measurements of Iris Species', 
              xlabel='Species', ylabel='Iris Measurements (cm)',
              xlim=(0.5, 3.7), ylim=(0, 10))
        
    
        xticks = [1.0, 2.0, 3.0]
        xlables = ['setosa', 'versicolor', 'virginica']
        ax.set_xticks(xticks, xlables)
        plt.legend()
        plt.show()

    return fig


def generate_plot_with_style2():

    # Write your functionality below
    with plt.style.context('seaborn-colorblind'):
        fig = plt.figure(figsize=(9,7))
        ax = fig.add_subplot(111)

        sepal_len = [6.01, 6.94, 7.59]
        sepal_wd = [4.42, 3.77, 3.97]
        petal_len = [2.46, 5.26, 6.55]
        petal_wd = [1.24, 2.33, 3.03]
        species = ['setosa', 'versicolor', 'virginica']
        species_index1 = [0.8, 1.8, 2.8]
        species_index2 = [1.0, 2.0, 3.0]
        species_index3 = [1.2, 2.2, 3.2]
        species_index4 = [1.4, 2.4, 3.4]

        
        ax.bar(species_index1, height=sepal_len, label='Sepal Length', width=0.2)
        ax.bar(species_index2, height=sepal_wd, label='Sepal Width', width=0.2)
        ax.bar(species_index3, height=petal_len, label='Petal Length', width=0.2)
        ax.bar(species_index4, height=petal_wd, label='Petal Width', width=0.2)
    
        ax.set(title='Mean Measurements of Iris Species', 
              xlabel='Species', ylabel='Iris Measurements (cm)',
              xlim=(0.5, 3.5), ylim=(0, 10))
        
    
        xticks = [1.0, 2.0, 3.0]
        xlables = ['setosa', 'versicolor', 'virginica']
        ax.set_xticks(xticks, xlables)
        plt.legend()
        plt.show()

    return fig


def generate_plot_with_style3():

    # Write your functionality below
    with plt.style.context('grayscale'):
        fig = plt.figure(figsize=(9,7))
        ax = fig.add_subplot(111)

        sepal_len = [6.01, 6.94, 7.59]
        sepal_wd = [4.42, 3.77, 3.97]
        petal_len = [2.46, 5.26, 6.55]
        petal_wd = [1.24, 2.33, 3.03]
        species = ['setosa', 'versicolor', 'virginica']
        species_index1 = [0.8, 1.8, 2.8]
        species_index2 = [1.0, 2.0, 3.0]
        species_index3 = [1.2, 2.2, 3.2]
        species_index4 = [1.4, 2.4, 3.4]

        
        ax.bar(species_index1, height=sepal_len, label='Sepal Length', width=0.2)
        ax.bar(species_index2, height=sepal_wd, label='Sepal Width', width=0.2)
        ax.bar(species_index3, height=petal_len, label='Petal Length', width=0.2)
        ax.bar(species_index4, height=petal_wd, label='Petal Width', width=0.2)
    
        ax.set(title='Mean Measurements of Iris Species', 
              xlabel='Species', ylabel='Iris Measurements (cm)',
              xlim=(0.5, 3.5), ylim=(0, 10))
        
    
        xticks = [1.0, 2.0, 3.0]
        xlables = ['setosa', 'versicolor', 'virginica']
        ax.set_xticks(xticks, xlables)
        plt.legend()
        plt.show()

    return fig


# Note: Do Not modify the below code
if __name__ == '__main__':
    import sys
    import subprocess
    # subprocess.check_call(
    #     [sys.executable, "-m", "pip", "install", 'test_plot5-0.1-py3-none-any.whl'], stdout=subprocess.DEVNULL)
    # from test_plot5 import matplotlib5
    usr_fig1 = generate_plot_with_style1()
    usr_fig2 = generate_plot_with_style2()
    usr_fig3 = generate_plot_with_style3()
    # matplotlib5.save_answer(usr_fig1, usr_fig2, usr_fig3)

