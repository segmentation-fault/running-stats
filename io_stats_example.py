__author__ = 'antonio franco'

'''
Copyright (C) 2019  Antonio Franco (antonio_franco@live.it)
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

"""
Script to demonstrate the usage of running mean. Plots an animation representing the average write speed on dev/null
 (or nul in windows), where file sizes are drawn from a discrete uniform distribution between 1024 and 2056 bytes.
"""

import os
import time
from running_stats import RunningStats
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# import matplotlib as mpl
# mpl.rcParams['errorbar.capsize'] = 3  # To restore the old behaviour of the returned values of errorbar


class IOAnimation(object):
    """
    Object to update an animation representing the average write speed on dev/null (or nul in windows), where file sizes
     are drawn from a discrete uniform distribution between a and b, with b > a. It displays both the running average and
     the running 95% confidence interval
    """

    def __init__(self, a, b, w_length) -> None:
        """
        :param a (int): value of the lower bound of the uniform distribution
        :param b (int):  value of the upper bound of the uniform distribution
        :param w_length (int): length, in samples, of the window in the plot for one frame.
        """
        super().__init__()
        assert (isinstance(a, int))
        assert (isinstance(b, int))
        assert (isinstance(w_length, int))
        assert (b > a)

        self.a = a
        self.b = b
        self.w_length = w_length

        self.S = RunningStats()

        fig, ax = plt.subplots()
        self.fig = fig
        self.ax = ax

        self.x = np.arange(0, self.w_length)
        self.y = np.zeros(self.w_length)
        self.yerr = np.zeros(self.w_length)

        line1, (bottoms, tops), _ = ax.errorbar(self.x, self.y, self.yerr, capsize = 3)

        self.ax.set_ylabel('avg write speed (Mbytes/sec)')

        self.ax.set_xticks([])

        self.line = [line1, bottoms, tops]

    def get_rand_byte_size(self) -> int:
        """
        random byte size between a and b
        :return (int): byte size
        """
        return np.random.randint(self.a, high=self.b)

    def animate(self, i):
        """
        main loop for the FuncAnimation function of matlplotlib
        :param i: frame number
        """
        byte_size = self.get_rand_byte_size()

        start = time.time()
        f = open(os.devnull, "wb")
        f.write(os.urandom(byte_size))
        elapsed = time.time() - start

        self.S.update(byte_size / elapsed)

        self.y[i % self.w_length] = self.S.get_mean() / 1e6
        self.yerr[i % self.w_length] = self.S.get_95_conf_intrv() / 1e6

        self.line[0].set_ydata(self.y)
        self.line[1].set_ydata(self.y - self.yerr)
        self.line[2].set_ydata(self.y + self.yerr)

        self.ax.set_ylim(0, np.max(self.y + self.yerr) * 2.0 + 0.1)

        return self.line

    def init(self):
        """
        init for the FuncAnimation function of matlplotlib
        """
        self.line[0].set_ydata(self.y)
        self.line[1].set_ydata(self.y - self.yerr)
        self.line[2].set_ydata(self.y + self.yerr)
        self.ax.set_ylim(0, 1)

        return self.line


def animate(i, I):
    return I.animate(i)


def init():
    return my_animation.init()


if __name__ == "__main__":
    my_animation = IOAnimation(1024, 2056, 100)

    ani = animation.FuncAnimation(my_animation.fig, animate, np.arange(1, 200), fargs=(my_animation,),
                                  init_func=init, interval=100, blit=False)

    plt.show()
