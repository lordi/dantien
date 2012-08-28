# -*- coding: utf-8 -*-
'''
Dantien view components: Plots, Spectrograms, ...
'''
import numpy as np
import glumpy
import OpenGL.GL as gl
import OpenGL.GLU as glu

from glumpy import figure, show, Trackball
from glumpy.graphics import VertexBuffer

THEME_BG = (0.01, 0.03, 0.05, 1)
THEME_FG = (0.0, 0.4, 0.8, 1)

class BaseView(object):
    def __init__(self, fig, ts, size=0.5):
        self.ts = ts
        self.fig = fig
        self.fig.push(self)

class Blank(BaseView):
    def on_draw(self):
        self.fig.lock()
        self.fig.clear(*THEME_BG)
        self.fig.unlock()

class Plot(BaseView):
    def on_draw(self):
        self.fig.lock()
        self.fig.clear(*THEME_BG)

        ds = self.get_series()
        if ds is None: return
        cnt = len(ds)

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho( 0, cnt, self.min, self.max, -10, 10)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

        gl.glColor(*THEME_FG)
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


from glfreetype import glFreeType

class SpectrogramAxis(BaseView):
    colormap = glumpy.colormap.Hot
    text_vertical_dist = 25.0
    text_size = 12
    brainwaves = [
            ('delta', 0.5, 4.0),
            ('theta', 4.0, 8.0),
            ('alpha', 8.0, 14.0),
            ('beta', 14.0, 30.0)
        ]

    def __init__(self, fig, ts, size=0.5, colormap=None):
        self.fig = fig
        self.ts = ts
        if not colormap is None: self.colormap = colormap
        self.font = glFreeType.font_data ("glfreetype/test.ttf", self.text_size)
        self.window_len = self.ts.dat_s.shape[1]
        self.freqs = np.fft.fftfreq(self.window_len, 1/33.0)[:self.window_len/2]

        self.fig.push(self)

    def on_draw(self):
        self.fig.lock()
        self.fig.clear(*THEME_BG)
        gl.glLoadIdentity ()

        for i in np.arange(0.,1.,self.text_vertical_dist/self.fig.height):
            freq = self.ts.freqs[int(i*self.ts.window_size/2)]
            # i * self.ts.window_size / 2 
            self.font.glPrint (self.fig.width-100, self.fig.height * i, "{0:.2f} Hz".format(freq))

        y = 0
        for name, low, high in self.brainwaves:
            y += 0.1
            center = (low + high) / 2.0
            #freq = self.ts.freqs[int(i*self.ts.window_size/2)]
            ypos = y
            self.font.glPrint (self.fig.width - 200, self.fig.height * ypos, name)
        self.fig.unlock()


class Spectrogram(object):
    colormap = glumpy.colormap.Hot
    text_size = 12
    num_freqs = 10

    def __init__(self, fig, ts, size=0.5, colormap=None):
        self.fig = fig
        self.ts = ts
        if not colormap is None: self.colormap = colormap
        self.fig.push(self)

    def on_draw(self):
        self.fig.lock()
        self.fig.clear(*THEME_BG)

        if self.ts.dat_s != None:
            self.img_s = glumpy.image.Image(self.ts.dat_s.astype(np.float32), colormap=self.colormap)
            self.img_s.update()
            self.img_s.draw( x=-self.ts.samples_since_last_update()/self.ts.buffer_len, y=0, z=0, width=self.fig.width, height=self.fig.height )

        gl.glLoadIdentity ()
        #print self.ts.freqs
        for i in np.arange(0.,1.,1.0/self.num_freqs):
            freq = self.ts.freqs[int(i*self.ts.window_size/2)]
            #print i *100
            #self.font.glPrint (0, 0, "{0:.2f} Hz".format(freq))

        self.fig.unlock()


class Spectrogram3D(Spectrogram):
    i = 0
    def on_draw(self):
        self.fig.lock()
        self.fig.clear(*THEME_BG)
        spect = self.ts.dat_s.astype(np.float32)

        self.i = self.i + 1
        xxx = np.sin(self.i/30.0)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(400.0, self.fig.width / float(self.fig.height), .01, 10000)
        gl.glRotate(-90.,.0,0.0,1.0)
        gl.glTranslate(-0.5,-0.5,-2.0-xxx*0.25)#+np.cos(self.i/20.0)/10.0)
        gl.glRotate(55.+xxx*10,.0,-1.0,0.0)

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

        if self.ts.dat_s != None:
            self.img_s = glumpy.image.Image(spect, colormap=self.colormap)
            self.img_s.update()
            self.img_s.draw( x=0, y=0, z=0, width=1, height=1)
        self.fig.unlock()


class Scaleogram(BaseView):
    colormap = glumpy.colormap.IceAndFire

    def __init__(self, fig, ts, size=0.5, colormap=None):
        self.fig = fig
        self.ts = ts
        if not colormap is None: self.colormap = colormap
        self.fig.push(self)

    def on_draw(self):
        self.fig.lock()
        self.fig.clear(*THEME_BG)
        if self.ts.dat_s != None:
            self.img_s = glumpy.image.Image(self.ts.dat_w.astype(np.float32), 
                    interpolation='bilinear',
                    colormap=self.colormap)
            self.img_s.update()
            self.img_s.draw( x=-self.ts.samples_since_last_update()*self.fig.width*0.00002 , y=0, z=0, width=self.fig.width, height=self.fig.height )
        self.fig.unlock()


class Cube(BaseView):
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
        self.fig.clear(*THEME_BG)
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


