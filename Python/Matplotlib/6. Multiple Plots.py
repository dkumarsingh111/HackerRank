# Welcome to Matplotlib -6 - Multiple Plots

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def generate_figure1():

    # Write your functionality below
    x = np.arange(0.0, 10.0, 0.01)
    arr_s1 = np.sin(3*np.pi*x)
    arr_s2 = np.sin(6*np.pi*x)

    fig = plt.figure(figsize=(12,7))
    axes1 = plt.subplot(2, 1, 1, title='Sin(3*pi*x)')
    axes1.plot(x, arr_s1)
    
    axes2 = plt.subplot(2, 1, 2, title='Sin(6*pi*x)')
    axes2.plot(x, arr_s2)

    return fig


def generate_figure2():

    # Write your functionality below
    np.random.seed(1500)
    x = np.random.rand(10)
    y = np.random.rand(10)
    z = np.sqrt(x**2 + y**2)

    fig = plt.figure(figsize=(9,7))
    
    axes1 = plt.subplot(2, 2, 1, title='Scatter plot with Diamond Markers')
    axes1.scatter(x, y, s=80, c=z, marker='d')
    axes1.set_xticks([0.0, 0.5, 1.0, 1.5]);
    axes1.set_yticks([-0.2, 0.2, 0.6, 1.0])

    axes2 = plt.subplot(2, 2, 2, title='Scatter plot with Circle Markers')
    axes2.scatter(x, y, s=80, c=z, marker='o')
    axes2.set_xticks([0.0, 0.5, 1.0, 1.5]);
    axes2.set_yticks([-0.2, 0.2, 0.6, 1.0])

    axes3 = plt.subplot(2, 2, 3, title='Scatter plot with Plus Markers')
    axes3.scatter(x, y, s=80, c=z, marker='+')
    axes3.set_xticks([0.0, 0.5, 1.0, 1.5]);
    axes3.set_yticks([-0.2, 0.2, 0.6, 1.0])

    axes4 = plt.subplot(2, 2, 4, title='Scatter plot with Triangle Markers')
    axes4.scatter(x, y, s=80, c=z, marker='^')
    axes4.set_xticks([0.0, 0.5, 1.0, 1.5]);
    axes4.set_yticks([-0.2, 0.2, 0.6, 1.0])
    
    plt.tight_layout()
    
    return fig


def generate_figure3():

    # Write your functionality below
    x = np.arange(1, 301, 3)
    y1 = x
    y2 = x**2
    y3 = x**3

    fig = plt.figure(figsize=(9,7))
    gr = gridspec.GridSpec(2,2)

    axes1 = plt.subplot(gr[0,:-1], title='y = x')
    axes1.plot(x, y1)

    axes2 = plt.subplot(gr[1,:-1], title='y = x**2')
    axes2.plot(x, y2)

    axes3 = plt.subplot(gr[:, 1], title='y = x**3')
    axes3.plot(x, y3)

    plt.tight_layout()

    return fig


# Note: Do Not modify the below code
if __name__ == '__main__':
    import sys
    import subprocess
    # subprocess.check_call(
    #     [sys.executable, "-m", "pip", "install", 'test_plot6-0.2-py3-none-any.whl'], stdout=subprocess.DEVNULL)
    # from test_plot6 import matplotlib6
    usr_fig1 = generate_figure1()
    usr_fig2 = generate_figure2()
    usr_fig3 = generate_figure3()
    # matplotlib6.save_answer(usr_fig1, usr_fig2, usr_fig3)
