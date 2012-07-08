# -*- coding: utf-8 -*-
'''
Dantien
'''
import numpy as np
import OpenGL.GL as gl

from glumpy import figure, show, Trackball
from glumpy.graphics import VertexBuffer

from views import Cube, Spectrogram, SeriesPlot, FFTPlot
from model import TimeSeries
from feeders import random_sinoids

from itertools import product

update_rate = 20 # Hz
size = (512,512)
ts = TimeSeries(random_sinoids)

def build_figure(layout):
    cols = len(layout[0])
    rows = len(layout)

    fig = figure(size=size)
    for x, y in product(range(cols), range(rows)):
        cons = layout[y][x]
        subfig = fig.add_figure(cols=cols, rows=rows, position=[x,rows-y-1])
        cons(subfig, ts)
    return fig

def update(_):
    ts.eat()
    fig.redraw()

fig = build_figure(layout=[
        [SeriesPlot],
        [Spectrogram],
        [FFTPlot]
    ])
fig.timer(update_rate)(update)
show()
