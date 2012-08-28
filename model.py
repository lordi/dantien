# -*- coding: utf-8 -*-
"""
This is the data model for the EEG data. It stores the time series and calculates
the spectrogram and other things.
"""
import numpy as np
import pywt
from pytfd import stft

from datetime import datetime

class TimeSeries():
    window_size = 128
    buffer_len = 512
    frame_rate = 256.0
    zoom = 16

    def __init__(self, feed_func):
        # Actual time series buffer
        self.series = np.zeros(self.buffer_len)
        # Spectrogram data (STFT)
        self.dat_s = np.zeros((self.window_size, self.buffer_len))
        # Scaleogram data (Wavelet transform)
        self.dat_w = np.zeros((32, 32)) # TODO

        self.feed_func = feed_func
        self.window = np.ones(self.window_size)
        self.update_time = datetime.now()

        self.freqs = np.fft.fftfreq(self.window_size) * self.frame_rate / self.zoom

    def eat(self):
        newdata = self.feed_func()

        # take every n-th
        zoomed = newdata[::self.zoom]
        self.series = np.append(self.series[len(zoomed):], zoomed)

        assert len(self.series) == self.buffer_len
        self.update(len(zoomed))

    def update(self, n):
        self.update_time = datetime.now()
        self.dat_s = np.roll(self.dat_s, -n)
        self.update_w(n)
        self.update_s(n)

    def update_w(self, n):
        " Update wavelet transform data "
        level = 5
        wp = pywt.WaveletPacket(self.series, 'coif4', 'sym', maxlevel=level)
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

    def samples_since_last_update(self):
        return (datetime.now() - self.update_time).microseconds / 100.0

if __name__ == '__main__':
    from feeders import random_sinoids
    s = TimeSeries(random_sinoids)
    for _i in range(5): s.eat()
    print s.dat_s

