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
This is a template file to implement glumpy backends.


Event management::

    Keyboard:

    def on_key_press(symbol, modifiers):
        'A key on the keyboard was pressed.'
        pass

    def on_key_release(symbol, modifiers):
        'A key on the keyboard was released.'
        pass


    Mouse:

    def on_mouse_press(self, x, y, button):
        'A mouse button was pressed.'
        pass

    def on_mouse_release(self, x, y, button):
        'A mouse button was released.'
        pass
                
    def on_mouse_motion(x, y, dx, dy):
        'The mouse was moved with no buttons held down.'
        pass

    def on_mouse_drag(x, y, dx, dy, buttons):
        'The mouse was moved with some buttons pressed.'
        pass

    def on_mouse_scroll(self, dx, dy):
        'The mouse wheel was scrolled by (dx,dy).'
        pass


    Window:

    def on_init(self):
        'The window has just initialized iself.'
        pass

    def on_show(self):
        'The window was shown.'
        pass
    
    def on_hide(self):
        'The window was hidden.'
        pass

    def on_close(self,):
        'The user closed the window.'
        pass

    def on_resize(self, width, height):
        'The window was resized to (width,height)'
        pass

    def on_draw(self):
        'The window contents must be redrawn.'
        pass

    def on_idle(self):
        'The window is inactive.'
        pass
'''
import event



def show():
    '''Show all windows.'''
    raise NotImplemented



class Window(event.EventDispatcher):
    ''' '''

    def __init__( self, x=None, y=None, width=None, height=None,
                  title=None, visible=True, fullscreen=False ):
        '''
        Creates a new Window.

        :Parameters:

            ``x``: int
                Initial window x position
                
            ``yt``: int
                Initial window y position

            ``width``: int
                Initial window width
                
            ``height``: int
                Initial window height

            ``title``: str
                Window title

            ``visible``: bool
                Whether window is visible or not

            ``fullscreen``: bool
                Whether window is visible or not
        '''
        raise NotImplemented


    def show(self):
        ''' Show window. '''
        raise NotImplemented

    def hide(self):
        ''' Hide window. '''
        raise NotImplemented

    def start(self):
        ''' Starts the event loop. '''
        raise NotImplemented

    def stop(self):
        ''' Stops the event loop. '''
        raise NotImplemented

    def draw(self):
        ''' Force a redraw of the window. '''
        pass



    def _get_fullscreen( self ):
        ''' Get fullscreen mode '''
        raise NotImplemented
    def _set_fullscreen( self, state ):
        ''' Set fullscreen mode '''
        raise NotImplemented
    fullscreen = property( _get_fullscreen, _set_fullscreen,
                           doc = 'Window fullscreen mode' )

    def _get_x( self ):
        ''' Get window x position. '''
        raise NotImplemented
    def _set_x( self, state ):
        ''' Set window x position. '''
        raise NotImplemented
    x = property( _get_x, _set_x,
                  doc = 'Window x coordinate' )

    def _get_y( self ):
        ''' Get window x position. '''
        raise NotImplemented
    def _set_y( self, state ):
        ''' Set window x position. '''
        raise NotImplemented
    y = property(_get_y, _set_y,
                 doc = 'Window y coordinate' )

    def _get_position( self ):
        ''' Get window position. '''
        raise NotImplemented
    def _set_position( self, state ):
        ''' Set window position. '''
        raise NotImplemented
    position = property( _get_position, _set_position,
                         doc = 'Window position' )

    def _get_width(self):
        ''' Get window width. '''
        raise NotImplemented
    def _set_width(self, state):
        ''' Set window width. '''
        raise NotImplemented
    width = property(_get_width, _set_width)

    def _get_height(self):
        ''' Get window height. '''
        raise NotImplemented
    def _set_height(self, state):
        ''' Set window height. '''
        raise NotImplemented
    height = property(_get_height, _set_height)

    def _get_size( self ):
        ''' Get window size. '''
        raise NotImplemented
    def _set_size( self, state ):
        ''' Set window size. '''
        raise NotImplemented
    size = property( _get_size, _set_size,
                     doc = 'Window size' )




# -----------------------------------------------------------------------------
if __name__ == '__main__':
    

    window = Window(640, 480, 0, 0, "Window title")

    @window.event
    def on_init():
        print 'Inititalization'

    @window.event
    def on_show():
        print 'Window has been shown'

    @window.event
    def on_hidden():
        print 'Window has been hidden'

    @window.event
    def on_draw():
        print 'Drawing requested'

    @window.event
    def on_resize(width,height):
        print 'Figure resized (width=%.1f, height=%.1f)'% (width,height)

    @window.timer(fps=1.0)
    def timer(elapsed):
        print 'Timed event (%.2f second(s) elapsed)' % elapsed

    # @window.event
    # def on_idle(dt):
    #     print 'Idle event'

    @window.event
    def on_key_press(symbol, modifiers):
        print 'Key pressed (symbol=%s, modifiers=%s)'% (symbol,modifiers)

    @window.event
    def on_key_release(symbol, modifiers):
        print 'Key released (symbol=%s, modifiers=%s)'% (symbol,modifiers)

    @window.event
    def on_mouse_press(x, y, button):
        print 'Mouse button pressed (x=%.1f, y=%.1f, button=%d)' % (x,y,button)

    @window.event
    def on_mouse_release(x, y, button):
        print 'Mouse button released (x=%.1f, y=%.1f, button=%d)' % (x,y,button)

    @window.event
    def on_mouse_motion(x, y, dx, dy):
        print 'Mouse motion (x=%.1f, y=%.1f, dx=%.1f, dy=%.1f)' % (x,y,dx,dy)

    @window.event
    def on_mouse_drag(x, y, dx, dy, button):
        print 'Mouse drag (x=%.1f, y=%.1f, dx=%.1f, dy=%.1f, button=%d)' % (x,y,dx,dy,button)

    window.start()
