#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# glumpy is an OpenGL framework for the fast visualization of numpy arrays.
# Copyright (C) 2009-2011  Nicolas P. Rougier. All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY NICOLAS P. ROUGIER ''AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL NICOLAS P. ROUGIER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# The views and conclusions contained in the software and documentation are
# those of the authors and should not be interpreted as representing official
# policies, either expressed or implied, of Nicolas P. Rougier.
# -----------------------------------------------------------------------------
'''
A Figure represents a rectangular area on a window that can be used to
display graphics and received events.
'''
import sys
import numpy as np
import OpenGL.GL as gl
from glumpy.window import Window, event, key, mouse, show




class FigureException(Exception):
    '''The root exception for all figure-related errors.'''
    pass




class Figure(event.EventDispatcher):
    '''
    A Figure represents a rectangular area on a window that can be used to
    display graphics and received events.

    :Example:

    .. code-block:: python

       fig = Figure()

       @fig.event
       def on_draw():
           draw_something()

       fig.show()
    '''



    def __init__(self, size = (800,600), position = (0,0), fullscreen = False, parent = None):
        '''
        :param int,int or float,float size:
            Absolute size in pixels if parent is None or relative size to
            parent's viewport.
        :param int,int or float,float position:
            Absolute position in pixels if parent is None or relative
            position in parent's viewport.
         :param Figure or Window parent:
             Parent Figure or Window
        '''
        event.EventDispatcher.__init__(self)
        self._parent = parent
        self._figures  = []
        self._size = size
        self._position = position

        if parent is None:
            w,h = size[0], size[1]
            self._window = Window( size=(w,h), position=position, title='Figure')
            self._window.push_handlers(self)
            self._window.push_handlers({})
            self._depth = -999
        else:
            self._depth = parent._depth + 10
            parent._figures.append( self )



    def _get_window(self):
        ''' Get window. '''
        parent = self
        while parent is not None:
            if parent.parent is None:
                return parent._window
            parent = parent.parent
    window = property(_get_window,
         doc='''
         Root window. Read-only.
         ''')

    parent = property(lambda self: self._parent,
         doc='''
         Parent figure. Read-only.
         ''')

    width = property(lambda self: self._width,
        doc='''Figure width in pixels. Read-only.
        ''')

    height = property(lambda self: self._height,
        doc='''Figure height in pixels. Read-only.
        ''')

    x = property(lambda self: self._x,
        doc='''Figure absolute x coordinate. Read-only.
        ''')

    y = property(lambda self: self._y,
        doc='''Figure absolute y coordinate. Read-only.
        ''')

    viewport = property(lambda self: (int(round(self.x)),
                                      int(round(self.y)),
                                      int(round(self.width)),
                                      int(round(self.height))),
         doc='''
         Figure absolute viewport as (x,y,width,height). Read-only.
         ''')



    def add_figure(self, cols = 1, rows = 1, position = (0,0), size = (1,1)):
        '''
        Add a figure to the current figure.

        :param integer cols:
            Virtual number of columns to be considered

        :param integer row:
            Virtual number of rows to be considered

        :param int,int position:
            Position relative to (cols,rows)

        :param int,int size:
            Size relative to (cols,rows)
        '''

        hborder, vborder = 0, 0
        if type(cols) is int:
            cols = [1,]*cols
        elif type(cols) is float:
            cols = [1,]*int(cols) + [cols-int(cols),]
        p = np.array(cols).astype(float)
        hborder = np.resize(np.array(hborder),len(cols)*2)
        hsize = (p / p.sum()) * (1-hborder.sum())

        if type(rows) is int:
            rows = [1,]*int(rows)
        elif type(rows) is float:
            rows = [1,]*rows + [rows-int(rows),]
        p = np.array(rows).astype(float)
        vborder = np.resize(np.array(vborder),len(rows)*2)
        vsize = (p / p.sum()) * (1-vborder.sum())

        col, row = position
        width, height = size
        x0 = hsize[0:col       ].sum() + hborder[0:1+2*col           ].sum()
        x1 = hsize[0:col+width ].sum() + hborder[0:1+2*(col+width)-2 ].sum()
        y0 = vsize[0:row       ].sum() + vborder[0:1+2*row           ].sum()
        y1 = vsize[0:row+height].sum() + vborder[0:1+2*(row+height)-2].sum()

        fig = Figure(size=(x1-x0,y1-y0), position=(x0,y0), parent=self)
        self._figures.append(fig)
        return fig




    def split(self, position = 'right', size = 0.5, spacing=0):
        '''
        Split the figure into two figures.

        :param string position:
           Split orientation, one of ("vertical", "horizontal")

        :param float size:
            Relative size of the two newly created figures.

        :param float spacing:
            Relative spacing betwen the two newly created figures.
        '''

        w,h = self._size
        x,y = self._position
        if position == 'horizontal':
            w1, w2 = (1-size-spacing/2.0),  (size-spacing/2.0)
            h1, h2 = 1, 1
            x1, x2 = 0, w1+spacing
            y1, y2 = 0, 0
        elif position == 'vertical':
            w1, w2 = 1, 1
            h1, h2 = (1-size-spacing/2.0),  (size-spacing/2.0)
            x1, x2 = 0, 0
            y1, y2 = 0, h2+spacing

        fig1 = Figure( size=(w1,h1), position=(x1,y1), parent=self )
        fig2 = Figure( size=(w2,h2), position=(x2,y2), parent=self )
        self._figures.extend([fig1,fig2])
        return fig1, fig2




    def add_frame(self, size = (0.9,0.9), spacing = 0.025, aspect=None):
        ''' '''
        return Frame(self, size=size, spacing=spacing, aspect=aspect)



    def clear(self, red=1, green=1, blue=1, alpha=1):
        '''
        Clear the current figure with given color.

        :param float red:
            Red component (default 1).

        :param float green:
            Green component (default 1).

        :param float blue:
            Blue component (default 1).

        :param float alpha:
            Alpha component (transparency, default 1).
        '''
        gl.glClearColor(red,green,blue,alpha)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)



    def show(self):
        '''
        Show all figures and enter the mainloop.
        '''

        self.window.start()



    def redraw(self):
        '''
        Draw the figure and all subfigures
        '''

        self.window.redraw()



    def save(self, filename):
        '''
        '''

        try:
            import OpenGL.GL.EXT.framebuffer_object as fbo
        except ImportError:
            print 'You do not have the framebuffer extension on your video card'
            print 'Cannot save figure'
            return

        w,h = self.window.width, self.window.height
        # Setup framebuffer
        framebuffer = fbo.glGenFramebuffersEXT(1)
        fbo.glBindFramebufferEXT( fbo.GL_FRAMEBUFFER_EXT, framebuffer)

        # Setup depthbuffer
        depthbuffer = fbo.glGenRenderbuffersEXT( 1 )
        fbo.glBindRenderbufferEXT( fbo.GL_RENDERBUFFER_EXT, depthbuffer )
        fbo.glRenderbufferStorageEXT( fbo.GL_RENDERBUFFER_EXT, gl.GL_DEPTH_COMPONENT, w, h)
    
        # Create texture to render to
        data = np.zeros((w,h,4), dtype=np.ubyte)
        texture = gl.glGenTextures(1)
        gl.glBindTexture( gl.GL_TEXTURE_2D, texture)
        gl.glTexParameteri( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexImage2D( gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, w, h, 0,
                         gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, data)
        fbo.glFramebufferTexture2DEXT( gl.GL_FRAMEBUFFER_EXT, gl.GL_COLOR_ATTACHMENT0_EXT,
                                       gl.GL_TEXTURE_2D, texture, 0)
        fbo.glFramebufferRenderbufferEXT( gl.GL_FRAMEBUFFER_EXT, gl.GL_DEPTH_ATTACHMENT_EXT, 
                                          gl.GL_RENDERBUFFER_EXT, depthbuffer)
        status = fbo.glCheckFramebufferStatusEXT( fbo.GL_FRAMEBUFFER_EXT )

        if status != fbo.GL_FRAMEBUFFER_COMPLETE_EXT:
            raise(RuntimeError, 'Error in framebuffer activation')

        self.redraw()
        self.window.refresh()
        
        x,y,w,h = self.viewport
        data = gl.glReadPixels (x,y,w, h, gl.GL_RGBA,  gl.GL_UNSIGNED_BYTE)
        from PIL import Image
        image = Image.fromstring('RGBA', (w,h), data)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image.save (filename)

        # Cleanup
        fbo.glBindRenderbufferEXT( fbo.GL_RENDERBUFFER_EXT, 0 )
        fbo.glBindFramebufferEXT( fbo.GL_FRAMEBUFFER_EXT, 0 )
        gl.glDeleteTextures( texture )
        fbo.glDeleteFramebuffersEXT( [framebuffer,] )



    def push(self, obj):
        '''
        Push object handlers onto the event stack

        :param object obj:
            Object to be pushed onto the event stack
        '''

        if self.parent is None:
            self.window.push_handlers(obj)
        else:
            self.push_handlers(obj)


    def pop(self, obj=None):
        '''
        Pop given object from the event stack. If obj is None, the last objects
        is removed.

        :param object obj:
            Object to be pushed onto the event stack or ``None`` to remove last
            pushed object
        '''
        if self.parent is None:
            if obj is None:
                self.window.pop_handlers(obj)
            else:
                self.window.remove_handlers(obj)
        else:
            if obj is None:
                self.pop_handlers(obj)
            else:
                self.remove_handlers(obj)





    def __contains__(self, point):
        '''
        Return true if point is contained in figure viewport
        '''

        x,y,w,h = self.viewport
        #x,y,w,h = self.x, self.y, self.width, self.height
        return x <= point[0] <= x+w and y <= point[1] <= y+h




    def on_init(self):
        '''
        OpenGL setup.
        
        The event loop will dispatch this event to all subfigures before
        entering mainloop and the figure will already have a valid GL context.
        '''

        gl.glEnable (gl.GL_DEPTH_TEST)
        gl.glEnable (gl.GL_LIGHT0)
        gl.glLightfv (gl.GL_LIGHT0, gl.GL_DIFFUSE,  (1.0, 1.0, 1.0, 1.0))
        gl.glLightfv (gl.GL_LIGHT0, gl.GL_AMBIENT,  (0.1, 0.1, 0.1, 1.0))
        gl.glLightfv (gl.GL_LIGHT0, gl.GL_SPECULAR, (0.0, 0.0, 0.0, 1.0))
        gl.glLightfv (gl.GL_LIGHT0, gl.GL_POSITION, (0.0, 1.0, 2.0, 1.0))
        gl.glEnable (gl.GL_BLEND)
        gl.glEnable (gl.GL_COLOR_MATERIAL)
        gl.glColorMaterial(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT_AND_DIFFUSE)
        gl.glBlendFunc (gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        
        for fig in self._figures:
            invoked = fig.dispatch_event('on_init')
            if invoked == event.EVENT_HANDLED: return invoked

        return event.EVENT_UNHANDLED




    def timer(self, fps):
        '''
        Function decorator for a timed handler.

        :param int fps:
           Frames per second
        '''

        return self.window.timer(fps)




    def on_draw(self):
        '''
        The window contents must be redrawn.

        The event loop will dispatch this event to all subfigures. This will
        happen during idle time after any figure events and after any scheduled
        functions were called.
        '''

        for fig in self._figures:
            # fig.lock()
            fig.dispatch_event('on_draw')
            # fig.unlock()




    def on_resize(self, width, height, x=0, y=0):
        '''
        The figure was resized.

        :param integer width:
            New parent absolute width, in pixels.
        :param integer height:
            New parent absolute height, in pixels.
        :param float x:
            New parent absolute x coordinate
        :param float x:
            New parent absolute y coordinate
        '''

        if self._parent is None:
            gl.glViewport( 0, 0, width, height )
            gl.glMatrixMode( gl.GL_PROJECTION )
            gl.glLoadIdentity( )
            gl.glOrtho( 0, width, 0, height, -1000, 1000 )
            gl.glMatrixMode( gl.GL_MODELVIEW )
            gl.glLoadIdentity( )
            self._width, self._height = width,height
            self._x, self._y = 0, 0
        else:
            self._width  = self._size[0]*width
            self._height = self._size[1]*height
            self._x = self._position[0]*width + x
            self._y = self._position[1]*height + y

        for fig in self._figures:
            fig.dispatch_event('on_resize', self.width, self.height, self.x, self.y)


        

    def on_key_press(self, symbol, modifiers):
        '''
        A key on the keyboard was pressed.

        :param integer symbol:
            The key symbol pressed.
        :param integer modifiers:
            Bitwise combination of the key modifiers active.
        '''

        for fig in self._figures:
            invoked = fig.dispatch_event('on_key_press', symbol, modifiers)
            if invoked == event.EVENT_HANDLED: return invoked
        return event.EVENT_UNHANDLED




    def on_key_release(self, symbol, modifiers):
        '''
        A key on the keyboard was released.

        :param integer symbol:
            The key symbol pressed.
        :param integer modifiers:
            Bitwise combination of the key modifiers active.
        '''

        for fig in self._figures:
            invoked = fig.dispatch_event('on_key_release', symbol, modifiers)
            if invoked == event.EVENT_HANDLED: return invoked
        return event.EVENT_UNHANDLED




    def on_mouse_press(self, x, y, button):
        '''
        A mouse button was pressed.

        :param integer x:
            Distance in pixels from the left edge of the window.
        :param integer y:
            Distance in pixels from the bottom edge of the window.
        :param integer button:
            The mouse button that was pressed.
        '''

        for fig in self._figures:
            if (x,y) in fig:
                invoked = fig.dispatch_event('on_mouse_press',
                                            x-fig.x, y-fig.y, button)
                if invoked == event.EVENT_HANDLED: return invoked
        return event.EVENT_UNHANDLED




    def on_mouse_release(self, x, y, button):
        '''
        A mouse button was released.

        :param integer x:
            Distance in pixels from the left edge of the figure.
        :param integer y:
            Distance in pixels from the bottom edge of the figure.
        :param integer button:
            The mouse button that was released.
        '''

        for fig in self._figures:
            if (x,y) in fig:
                invoked = fig.dispatch_event('on_mouse_release',
                                            x-fig.x, y-fig.y, button)
                if invoked == event.EVENT_HANDLED: return invoked
        return event.EVENT_UNHANDLED



    def on_mouse_motion(self, x, y, dx, dy):
        '''
        The mouse was moved with no buttons held down.
   
        :param integer x:
            Distance in pixels from the left edge of the figure.
        :param integer y:
            Distance in pixels from the bottom edge of the figure.
        :param integer dx:
            Relative X position from the previous mouse position.
        :param integer dy:
            Relative Y position from the previous mouse position.
        '''


        for fig in self._figures:
            if (x,y) in fig:
                invoked = fig.dispatch_event('on_mouse_motion',
                                            x-fig.x, y-fig.y, dx,dy)
                if invoked == event.EVENT_HANDLED: return invoked
        return event.EVENT_UNHANDLED



    def on_mouse_drag(self, x, y, dx, dy, button):
        '''
        The mouse was moved with some buttons pressed.

        :param integer x:
            Distance in pixels from the left edge of the figure.
        :param integer y:
            Distance in pixels from the bottom edge of the figure.
        :param integer dx:
            Relative X position from the previous mouse position.
        :param integer dy:
            Relative Y position from the previous mouse position.
        :param integer buttons:
            Bitwise combination of the mouse buttons currently pressed.
        '''

        for fig in self._figures:
            if (x,y) in fig:
                invoked = fig.dispatch_event('on_mouse_drag',
                                             x, y, dx, dy, button)
                if invoked == event.EVENT_HANDLED: return invoked
        return event.EVENT_UNHANDLED



    def on_mouse_scroll(self, dx, dy):
        '''
        The mouse wheel was scrolled by (dx,dy).

        :param integer dx:
            Number of "clicks" towards the right (left if negative).
        :param integer dy:
            Number of "clicks" upwards (downwards if negative).
        '''

        for fig in self._figures:
            if (x,y) in fig:
                invoked = fig.dispatch_event('on_mouse_scroll',
                                            x-fig.x, y-fig.y, scroll_x, scroll_y)
                if invoked == event.EVENT_HANDLED: return invoked
        return event.EVENT_UNHANDLED



    def event(self, *args):
        '''Function decorator for an event handler.'''

        if self.parent is None:
            return event.EventDispatcher.event(self.window,*args)
        else:
            # If the event is 'on_idle', we attach it directly to the window
            if args[0] == 'on_idle' or args[0].__name__ == 'on_idle':
                self.window.push_handlers(*args)
            else:
                return event.EventDispatcher.event(self,*args)



    def lock(self):
        '''
        Lock the figure by setting GL viewport to figure viewport and
        prohibiting drawing outside the viewport.
        '''

        x, y, w, h = self.viewport
        gl.glPushAttrib( gl.GL_VIEWPORT_BIT | gl.GL_SCISSOR_BIT )
        gl.glMatrixMode( gl.GL_PROJECTION )
        gl.glPushMatrix( )
        gl.glLoadIdentity( )
        gl.glViewport( x, y, w, h )
        gl.glEnable( gl.GL_SCISSOR_TEST )
        gl.glScissor( x, y, w, h )
        gl.glOrtho( 0, w, 0, h, -1000, 1000 )
        gl.glMatrixMode( gl.GL_MODELVIEW )
        gl.glPushMatrix( )
        gl.glLoadIdentity( )




    def unlock(self):
        '''
        Unlock the figure by restoring viewport.
        '''

        gl.glMatrixMode( gl.GL_PROJECTION )
        gl.glPopMatrix( )
        gl.glMatrixMode( gl.GL_MODELVIEW )
        gl.glPopMatrix( )
        gl.glPopAttrib( )





class Frame(Figure):
    ''' 
    A Frame is a special king of figure that can draw itself and preserve a
    given aspect ratio.
    '''

    def __init__(self, figure, size = (1.0,1.0), aspect = None, spacing=0,
                 fg_color=(0,0,0,1), bg_color=(1,1,1,1)):
        '''
        Create a new frame within given figures.

        :Parameters:
        
            ``figure``: Figure
                 Figure to put frame into

            ``size``: (float,float)
                 Frame relative size

             ``aspect``: float
                 Frame aspect

             ``fg_color``: 4-floats tuple
                 Foreground color (border)

             ``bg_color``: 4-floats tuple
                 Background color
        '''
        self._aspect = aspect
        Figure.__init__(self, size=size, parent=figure)
        self._fg_color = fg_color
        self._bg_color = bg_color




    def on_resize(self, width, height, x=0, y=0):
        '''
        A resize event occured.

        :Parameters:

            ``width`` : float
                New parent absolute width

            ``height`` : float
                New parent absolute height

            ``x`` : float
                New parent absolute x coordinate

            ``y`` : float
                New parent absolute y coordinate
        '''

        if self._parent is None:
            gl.glViewport( 0, 0, width, height )
            gl.glMatrixMode( gl.GL_PROJECTION )
            gl.glLoadIdentity( )
            gl.glOrtho( 0, width, 0, height, -1000, 1000 )
            gl.glMatrixMode( gl.GL_MODELVIEW )
            gl.glLoadIdentity( )
            self._width, self._height = width,height
            self._x, self._y = 0, 0
        else:
            w,h = self._size[0]*width, self._size[1]*height
            if self._aspect is not None:
                if w/float(h) > self._aspect:
                    w = self._aspect*h
                else:
                    h = w/self._aspect
            self._width, self._height = w,h
            self._x, self._y = (width-w)/2 + x, (height-h)/2 + y

        for fig in self._figures:
            fig.dispatch_event('on_resize', self.width, self.height, self.x, self.y)




    def draw(self, x=0, y=0, z=None, width=None, height=None):
        '''
        Draw the frame at specified coordinates.

        :Parameters:

            ``x`` : float
                X coordinate

            ``y`` : float
                Y coordinate

            ``z`` : float
                Z coordinate

        :Note:

            Background is drawn at depth z while foreground border is drawn at
            depth -z.
        '''

        if z is None:
            z = self._depth

        x,y,z = x + .315, y + .315, -abs(z)
        
        if width is None:
            w = int(round(self.width)) -.315
        else:
            w = int(round(width)) -.315

        if height is None:
            h = int(round(self.height)) -.315
        else:
            h = int(round(height)) -.315

        gl.glDisable(gl.GL_BLEND)
        gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glDisable(gl.GL_LINE_SMOOTH)
        gl.glPolygonMode( gl.GL_FRONT_AND_BACK, gl.GL_FILL )

        gl.glColor(*self._bg_color)
        gl.glBegin(gl.GL_QUADS)
        gl.glVertex3f(x,   y,   z)
        gl.glVertex3f(x+w, y,   z)
        gl.glVertex3f(x+w, y+h, z)
        gl.glVertex3f(x,   y+h, z)
        gl.glEnd()

        gl.glColor(*self._fg_color)
        gl.glBegin(gl.GL_LINE_LOOP)
        gl.glVertex3f(x,   y,   -z)
        gl.glVertex3f(x+w, y,   -z)
        gl.glVertex3f(x+w, y+h, -z)
        gl.glVertex3f(x,   y+h, -z)
        gl.glEnd()



Figure.register_event_type('on_init')
Figure.register_event_type('on_resize')
Figure.register_event_type('on_draw')
Figure.register_event_type('on_idle')
Figure.register_event_type('on_key_press')
Figure.register_event_type('on_key_release')
Figure.register_event_type('on_mouse_motion')
Figure.register_event_type('on_mouse_drag')
Figure.register_event_type('on_mouse_press')
Figure.register_event_type('on_mouse_release')
Figure.register_event_type('on_mouse_scroll')

