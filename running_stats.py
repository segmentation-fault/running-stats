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

import sys


class RunningStats(object):
    """
    Implements the running weighted mean and variance as described in:
    D. H. D. West. 1979. Updating mean and variance estimates: an improved method. Commun. ACM 22, 9 (September 1979), 532-535. DOI: https://doi.org/10.1145/359146.359153
    it also provides a fail-safe against numerical overflow by chunking sums, preventing them from numerical overflowing
    """

    def __init__(self) -> None:
        super().__init__()

        self.M = 0
        self.n = 0
        self.sum_w = [0]
        self.T = [0]
        self.i_chunk = 0

    def reset(self):
        """
        resets all the variables
        :return: Nothing
        """
        self.M = 0
        self.n = 0
        self.sum_w = [0]
        self.T = [0]
        self.i_chunk = 0

    def update(self, x, w=1.0):
        """
        Updates the mean with samples x with (optional) weight w
        :param x: sample to update the mean.
        :param w: (optional) weight of the sample. Default w = 1.0.
        :return: Nothing
        """
        if self.n == 0:
            self.M = x
            self.sum_w[0] = w
            self.n += 1
        else:
            if self.sum_w[self.i_chunk] >= sys.float_info.max - w or self.T[self.i_chunk] >= sys.float_info.max - x:
                self.i_chunk += 1
            q = x - self.M
            temp = self.sum_w[self.i_chunk] + w
            r = q * w / temp
            self.M += r
            self.T[self.i_chunk] += r * self.sum_w[self.i_chunk] * q
            self.sum_w[self.i_chunk] = temp
            self.n += 1

    def get_mean(self) -> float:
        """
        Returns the current value of the mean
        :return: the current value of the mean
        """
        return self.M

    def get_variance(self) -> float:
        """
        returns the current value of the variance
        :return: the current value of the variance
        """
        res = 0.0
        if self.n > 0:
            det = 0.0
            K = (self.n - 1.0) / self.n
            for i in range(0, self.i_chunk + 1):
                det += K * self.sum_w[i]

            if det > 0:
                for i in range(0, self.i_chunk + 1):
                    res += self.T[i] / det

        return res

    def get_std(self) -> float:
        """
        returns the current value of the standard deviation
        :return: the current value of the standard deviation
        """
        var = self.get_variance()
        return np.sqrt(var)

    def get_95_conf_intrv(self) -> float:
        """
        returns the current value of the 95% confidence interval
        :return: the current value of the 95% confidence interval
        """
        if self.n > 0:
            std = self.get_std()
            return 1.96 * std / np.sqrt(self.n)
        else:
            return 0.0

    def __str__(self) -> str:
        ret_str = "running weighted mean : " + str(self.get_mean()) + " ,\n" + "running weighted variance : " + str(
            self.get_variance()) \
                  + " , \n" + "number of samples : " + str(self.n) + " . \n"
        return ret_str


import numpy as np


if __name__ == "__main__":
    S = RunningStats()
    n_samples = int(1e5)

    print("Test with no weights, " + str(n_samples) + " samples. \n")

    my_rate = 2.0
    X = np.random.exponential(1.0 / my_rate, n_samples)

    for i in range(0, X.size):
        S.update(X[i])

    print(S)
    print("numpy mean : " + str(np.mean(X)) + " , \n" + "numpy variance : " + str(np.var(X)) + " . \n")
    print("true mean : " + str(1.0 / my_rate) + " , \n" + "true variance : ", str(1.0 / my_rate ** 2.0) + " . \n")

    print("Test with weights, " + str(n_samples) + " samples. \n")
    S.reset()

    w_rate = 4.0
    W = np.random.exponential(1.0 / w_rate, n_samples)
    for i in range(0, X.size):
        S.update(X[i], W[i])

    print(S)

    M = np.average(X, weights=W)
    V = np.average((X - M) ** 2.0, weights=W)
    print("numpy weighted mean : " + str(M) + " , \n" + "numpy weighted variance : " + str(V) + " . \n")
