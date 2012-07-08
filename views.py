# -*- coding: utf-8 -*-
'''
Dantien view components: Plots, Spectrograms, ...
'''
import numpy as np
import glumpy
import OpenGL.GL as gl

from glumpy import figure, show, Trackball
from glumpy.graphics import VertexBuffer

class Plot(object):
    def __init__(self, fig, ts, size=0.5):
        self.ts = ts
        self.fig = fig
        self.fig.push(self)

    def on_draw(self):
        self.fig.lock()
        self.fig.clear(.85,.85,.85,1)

        ds = self.get_series()
        if ds is None: return
        cnt = len(ds)

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho( 0, cnt, self.min, self.max, -10, 10)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

        gl.glColor( 0.0, 0.4, 0.4, 0.5 )
        gl.glBegin(gl.GL_QUADS)
        for i in range(cnt):
            gl.glVertex3f(i+0.5,0,0)
            gl.glVertex3f(i+0.5,float(ds[i]),0)
            gl.glVertex3f(i-0.5,float(ds[i]),0)
            gl.glVertex3f(i-0.5,0,0)
        gl.glEnd()

        self.fig.unlock()

class SeriesPlot(Plot):
    min, max = -1, 1
    def get_series(self):
        return self.ts.series

class FFTPlot(Plot):
    min, max = 0, 30
    def get_series(self):
        return self.ts.dat_s[:,-1]

class Spectrogram(object):
    colormap = glumpy.colormap.Hot

    def __init__(self, fig, ts, size=0.5, colormap=None):
        self.fig = fig
        self.ts = ts
        if not colormap is None: self.colormap = colormap
        self.fig.push(self)

    def on_draw(self):
        self.fig.lock()
        self.fig.clear(.25,.85,.85,1)
        if self.ts.dat_s != None:
            self.img_s = glumpy.image.Image(self.ts.dat_s.astype(np.float32), colormap=self.colormap)
            self.img_s.update()
            self.img_s.draw( x=0, y=0, z=0, width=self.fig.width, height=self.fig.height )
        self.fig.unlock()

class Cube(object):
    " Cube from glumpy demo "
    def __init__(self, fig, ts, size=0.5):
        s = size
        p = ( ( s, s, s), (-s, s, s), (-s,-s, s), ( s,-s, s),
              ( s,-s,-s), ( s, s,-s), (-s, s,-s), (-s,-s,-s) )
        n = ( ( 0, 0, 1), (1, 0, 0), ( 0, 1, 0),
              (-1, 0, 1), (0,-1, 0), ( 0, 0,-1) );
        c = ( ( 1, 1, 1), ( 1, 1, 0), ( 1, 0, 1), ( 0, 1, 1),
              ( 1, 0, 0), ( 0, 0, 1), ( 0, 1, 0), ( 0, 0, 0) );
        vertices = np.array(
            [ (p[0],n[0],c[0]), (p[1],n[0],c[1]), (p[2],n[0],c[2]), (p[3],n[0],c[3]),
              (p[0],n[1],c[0]), (p[3],n[1],c[3]), (p[4],n[1],c[4]), (p[5],n[1],c[5]),
              (p[0],n[2],c[0]), (p[5],n[2],c[5]), (p[6],n[2],c[6]), (p[1],n[2],c[1]),
              (p[1],n[3],c[1]), (p[6],n[3],c[6]), (p[7],n[3],c[7]), (p[2],n[3],c[2]),
              (p[7],n[4],c[7]), (p[4],n[4],c[4]), (p[3],n[4],c[3]), (p[2],n[4],c[2]),
              (p[4],n[5],c[4]), (p[7],n[5],c[7]), (p[6],n[5],c[6]), (p[5],n[5],c[5]) ], 
            dtype = [('position','f4',3), ('normal','f4',3), ('color','f4',3)] )
        self.buffer = VertexBuffer(vertices)
        self.trackball = Trackball(65, 135, 1.25, 4.5)
        self.fig = fig
        self.fig.push(self)

    def on_init(self):
        gl.glEnable( gl.GL_BLEND )
        gl.glEnable( gl.GL_LINE_SMOOTH )
        gl.glBlendFunc (gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    def on_mouse_drag(self, x, y, dx, dy, button):
        self.trackball.drag_to(x,y,dx,dy)
        self.fig.redraw()

    def on_draw(self):
        self.fig.lock()
        self.fig.clear(.85,.85,.85,1)
        self.trackball.push()
        gl.glEnable( gl.GL_BLEND )
        gl.glEnable( gl.GL_LINE_SMOOTH )
        gl.glBlendFunc (gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable( gl.GL_POLYGON_OFFSET_FILL )
        gl.glPolygonOffset (1, 1)
        gl.glPolygonMode( gl.GL_FRONT_AND_BACK, gl.GL_FILL )
        self.buffer.draw( gl.GL_QUADS, 'pnc' )
        gl.glDisable( gl.GL_POLYGON_OFFSET_FILL )
        gl.glPolygonMode( gl.GL_FRONT_AND_BACK, gl.GL_LINE )
        gl.glDepthMask( gl.GL_FALSE )
        gl.glEnable(gl.GL_BLEND)
        gl.glEnable(gl.GL_LINE_SMOOTH)
        gl.glColor( 0.0, 0.0, 0.0, 0.5 )
        self.buffer.draw( gl.GL_QUADS, 'p' )
        gl.glDepthMask( gl.GL_TRUE )
        self.trackball.pop()
        gl.glPolygonMode( gl.GL_FRONT_AND_BACK, gl.GL_FILL )
        self.fig.unlock()


