# -*- coding: utf-8 -*-
'''
Dantien application
'''
from itertools import product
import glumpy

def dantien(feed_func, layout, update_rate=20):
    ts = TimeSeries(feed_func)

    cols = len(layout[0])
    rows = len(layout)

    fig = glumpy.figure()
    for x, y in product(range(cols), range(rows)):
        cons = layout[y][x]
        subfig = fig.add_figure(cols=cols, rows=rows, position=[x,rows-y-1])
        cons(subfig, ts)

    @fig.timer(update_rate)
    def update(_):
        ts.eat()
        fig.redraw()

    glumpy.show()

if __name__ == '__main__':
    import sys
    from views import Cube, Spectrogram, SeriesPlot, FFTPlot, \
            SpectrogramAxis, Scaleogram, Blank as _
    from model import TimeSeries
    import feeders

    if len(sys.argv) >= 2 and sys.argv[1] == '--spectrogram-only':
        layout = [
            [SpectrogramAxis, Spectrogram]
        ]
    else:
        layout = [
            [FFTPlot, SeriesPlot],
            [_, Spectrogram],
            [_, Scaleogram],
        ]

    dantien(feeders.modeeg(), layout)

