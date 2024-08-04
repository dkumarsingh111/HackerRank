import numpy as np
import matplotlib.pyplot as plt


def test_the_plot():

    # Write your functionality below

    fig = plt.figure(figsize=(12,6))
    ax = fig.add_subplot(111)
    t = [7, 14, 21, 28, 35]
    d = [i*6 for i in t]

    ax.set(title='Time vs Distance Covered', xlabel='time (seconds)', ylabel='distance (meters)', xlim=(0, 40), ylim=(0,220))

    plt.plot(t, d, label='d = 6t')
    plt.legend()
    plt.show()
    
    
    return fig


# Note: Do Not modify the below code
if __name__ == '__main__':
    import sys
    import subprocess
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", 'test_plot1-0.2-py3-none-any.whl'], stdout=subprocess.DEVNULL)
    from test_plot1 import matplotlib1
    usr_fig = test_the_plot()
    matplotlib1.save_answer(usr_fig)
