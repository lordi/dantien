# -*- coding: utf-8 -*-
"""
This is the data model for the EEG data. It stores the time series and calculates
the spectrogram and other things.
"""
import numpy as np
from pytfd import stft

class TimeSeries():
    window_size = 128
    buffer_len = 1024

    def __init__(self, feed_func):
        self.series = np.zeros(self.buffer_len)
        self.dat_s = np.zeros((self.window_size, self.buffer_len))
        self.feed_func = feed_func

    def eat(self):
        newdata = self.feed_func()
        self.series = np.append(self.series[len(newdata):], newdata)
        assert len(self.series) == self.buffer_len
        self.update(len(newdata))

    def update(self, n):
        self.dat_s = np.roll(self.dat_s, -n)
        l = n + self.window_size * 3
        c = n + self.window_size * 2
        newpart = stft.spectogram(self.series[-l:], np.ones(self.window_size))
        self.dat_s[:,-c:] = newpart[:,-c:]

if __name__ == '__main__':
    from feeders import random_sinoids
    s = TimeSeries(random_sinoids)
    for _i in range(5): s.eat()
    print s.dat_s

