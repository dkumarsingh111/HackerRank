import numpy as np
import matplotlib.pyplot as plt



def sine_wave_plot():

    # Write your functionality below

    fig = plt.figure(figsize=(13, 4))
    ax = fig.add_subplot(111)
    
    ax.set(title='Sine Wave',
          xlabel='Time (seconds)', ylabel='Voltage (mv)',
          xlim=(0, 2), ylim=(-1, 1))

    arr_t = np.linspace(0.0, 3.0, 250)
    arr_v = np.sin(2.5*np.pi*arr_t)

    ax.plot(arr_t, arr_v, color='red', label='sin(arr_t)')
    xticks = [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
    xlabels = xticks
    ax.set_xticks(xticks, xlabels)
    yticks = [-1, 0, 1]
    ylabels = [str(y) for y in yticks]
    ax.set_yticks(yticks, ylabels)
    plt.legend()
    plt.grid(linestyle = '--')
    #plt.show()
    return fig


def multi_curve_plot():

    # Write your functionality below
    fig = plt.figure(figsize=(13, 4))
    ax = fig.add_subplot(111)
    
    ax.set(title='Linear, Quadratic, & Cubic Equations',
      xlabel='arr_x', ylabel='f(arr_x)')

    arr_x = np.linspace(0.0, 7.0, 25)
    arr_y1 = arr_x
    arr_y2 = arr_x**2
    arr_y3 = arr_x**3

    ax.plot(arr_x, arr_y1, color='green', marker='^', label='y=arr_x')
    ax.plot(arr_x, arr_y2, color='blue', marker='s', label='y=arr_x**2')
    ax.plot(arr_x, arr_y3, color='red', marker='o', label='y=arr_x**3')
    plt.legend()    
    #plt.show()
    return fig


def scatter_plot():

    # Write your functionality below
    fig = plt.figure(figsize=(13, 4))
    ax = fig.add_subplot(111)
    
    ax.set(title="Cars Sold by Company 'Z' in 2021",
      xlabel='Months', ylabel='No. of Cars Sold',
      xlim=(0, 13), ylim=(10, 110))

    car_sales = [40, 65, 70, 40, 55, 60, 75, 60, 80, 95, 96, 105]
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    ax.scatter(months, car_sales, color='green', marker='o', label='car sales')
    xticks = [1, 3, 5, 7, 9, 11]
    xlabels = ['January', 'March', 'May', 'July', 'September', 'November']
    ax.set_xticks(xticks, xlabels)
    plt.legend()
    #plt.show()
    return fig


# Note: Do Not modify the below code
if __name__ == '__main__':
    import sys
    import subprocess
    # subprocess.check_call(
    #     [sys.executable, "-m", "pip", "install", 'test_plot2-0.1-py3-none-any.whl'], stdout=subprocess.DEVNULL)
    # from test_plot2 import matplotlib2
    usr_fig1 = sine_wave_plot()
    usr_fig2 = multi_curve_plot()
    usr_fig3 = scatter_plot()
    # matplotlib2.save_answer(usr_fig1, usr_fig2, usr_fig3)
