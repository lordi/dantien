# -*- coding: utf-8 -*-
"""
This is the data model for the EEG data. It stores the time series and calculates
the spectrogram and other things.
"""
import numpy as np
import pywt
from pytfd import stft

class TimeSeries():
    window_size = 64
    buffer_len = 256

    def __init__(self, feed_func):
        # Actual time series buffer
        self.series = np.zeros(self.buffer_len)
        # Spectrogram data (STFT)
        self.dat_s = np.zeros((self.window_size, self.buffer_len))
        # Scaleogram data (Wavelet transform)
        self.dat_w = np.zeros((32, 32)) # TODO

        self.feed_func = feed_func
        self.window = np.ones(self.window_size)

    def eat(self):
        newdata = self.feed_func()
        self.series = np.append(self.series[len(newdata):], newdata)

        assert len(self.series) == self.buffer_len
        self.update(len(newdata))

    def update(self, n):
        self.dat_s = np.roll(self.dat_s, -n)
        self.update_w(n)
        self.update_s(n)

    def update_w(self, n):
        " Update wavelet transform data "
        level = 5
        wp = pywt.WaveletPacket(self.series, 'db2', 'sym', maxlevel=level)
        nodes = wp.get_level(level, order='freq')
        values = np.abs(np.array([nx.data for nx in nodes]))
        self.dat_w = np.clip(values, 0.0, 0.3)
        self.dat_w = np.flipud(self.dat_w) # TODO: do this during the visualisation

    def update_s(self, n):
        " Update STFT spectrogram data "
        l = n + self.window_size * 3
        c = n + self.window_size * 2
        newpart = stft.spectogram(self.series[-l:], self.window)
        newpart = np.clip(newpart, 0.0, 2.0)
        newpart = np.flipud(newpart) # TODO: do this during the visualisation
        self.dat_s[:,-c:] = newpart[:,-c:]

if __name__ == '__main__':
    from feeders import random_sinoids
    s = TimeSeries(random_sinoids)
    for _i in range(5): s.eat()
    print s.dat_s

