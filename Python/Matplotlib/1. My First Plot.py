import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def sine_wave_plot():

    # Write your functionality below

    fig = plt.figure(figsize=(13,4))
    ax = fig.add_subplot(111)
    
    ax.set(title='Sine Wave',
      xlabel='Time (seconds)', ylabel='Voltage (mv)',
      xlim=(0, 2), ylim=(-1, 1))

    arr_t = linspace(0.0,3.0,250)
    arr_v = np.sin(2.5*np.pi*arr_t)

    ax.plot(arr_t, arr_v, color='red', marker='o', label='sin(arr_t)', linestyle='--')
    plt.legend()
    return fig


def multi_curve_plot():

    # Write your functionality below
    fig = plt.figure(figsize=(13,4))
    ax = fig.add_subplot(111)
    
    ax.set(title='Linear, Quadratic, & Cubic Equations',
      xlabel='arr_x', ylabel='f(arr_x)')

    arr_x = linspace(0.0,7.0,25)
    arr_y1 = arr_x
    arr_y2 = arr_x**2
    arr_y3 = arr_x**3

    ax.plot(arr_x, arr_y1, color='green', marker='^', label='y=arr_x', linestyle='--')
    ax.plot(arr_x, arr_y2, color='blue', marker='^', label='y=arr_x**2', linestyle='--')
    ax.plot(arr_x, arr_y3, color='red', marker='^', label='y=arr_x**3', linestyle='--')
    plt.legend()    

    return fig


def scatter_plot():

    # Write your functionality below
    fig = plt.figure(figsize=(13,4))
    ax = fig.add_subplot(111)
    
    ax.set(title="Cars Sold by Company 'Z' in 2021",
      xlabel='Months', ylabel='No. of Cars Sold',
      xlim=(0, 13), ylim=(10, 110))

    car_sales =[40, 65, 70, 40, 55, 60, 75, 60, 80, 95, 96, 105]
    arr_v = np.sin(2.5*np.pi*arr_t)
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    ax.plot(months, car_sales, color='green', marker='o', label='sin(arr_t)', linestyle='--')
    plt.legend()
    return fig


# Note: Do Not modify the below code
if __name__ == '__main__':
    import sys
    import subprocess
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", 'test_plot2-0.1-py3-none-any.whl'], stdout=subprocess.DEVNULL)
    from test_plot2 import matplotlib2
    usr_fig1 = sine_wave_plot()
    usr_fig2 = multi_curve_plot()
    usr_fig3 = scatter_plot()
    matplotlib2.save_answer(usr_fig1, usr_fig2, usr_fig3)
