# -*- coding: utf-8 -*-
import numpy as np
import glumpy
from pytfd import stft

class GLSpectrogram():
    window_size = 128
    buffer_len = 2048
    update_rate = 15 # Hz
    series_display_res = 128
    colormap = glumpy.colormap.Hot

    def __init__(self, data_func):
        self.series = np.zeros(self.buffer_len)
        self.dat_b = np.zeros((self.series_display_res, self.buffer_len))
        self.dat_s = np.zeros((self.window_size, self.buffer_len))
        self.fig_b, self.fig_s = \
                glumpy.figure( (self.buffer_len,self.buffer_len) ).split(position='vertical')
        self.fig_s.event('on_draw')(self.on_draw_s)
        self.fig_b.event('on_draw')(self.on_draw_b)
        self.fig_s.timer(self.update_rate)(self.receive)
        self.data_func = data_func
        glumpy.show()

    def receive(self, td):
        newdata = self.data_func(td)
        self.series = np.append(self.series[len(newdata):], newdata)
        assert len(self.series) == self.buffer_len
        self.update(len(newdata))

    def update(self, n):
        self.dat_s = np.roll(self.dat_s, -n)
        l = n + self.window_size * 3
        c = n + self.window_size * 2
        newpart = stft.spectogram(self.series[-l:], np.ones(self.window_size))
        self.dat_s[:,-c:] = newpart[:,-c:]
        self.fig_s.redraw()

        self.dat_b = np.roll(self.dat_b, -n)
        self.dat_b[:,-n:] = np.zeros((self.series_display_res,n))

        for idx in range(self.buffer_len - n - 1, self.buffer_len):
            self.dat_b[int(self.series[idx]*self.series_display_res),idx] = 0.5

    def on_draw_s(self):
        self.fig_s.lock()
        self.fig_s.clear()
        if self.dat_s != None:
            self.img_s = glumpy.image.Image(self.dat_s.astype(np.float32), colormap=self.colormap)
            self.img_s.update()
            self.img_s.draw( x=0, y=0, z=0, width=self.fig_s.width, height=self.fig_s.height )
        self.fig_s.unlock()

    def on_draw_b(self):
        self.fig_b.lock()
        self.fig_b.clear()
        if self.dat_b != None:
            self.img_b = glumpy.image.Image(self.dat_b.astype(np.float32), colormap=self.colormap)
            self.img_b.update()
            self.img_b.draw( x=0, y=0, z=0, width=self.fig_b.width, height=self.fig_b.height )
        self.fig_b.unlock()

if __name__ == '__main__':
    random_sin = lambda td: np.sin(np.arange(100)*np.random.random(1)*5.0)
    s = GLSpectrogram(random_sin)

