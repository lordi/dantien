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
import sys
import key
import event
import mouse



def show():
    ''' Show all windows and enters the main event loop. '''

    raise NotImplemented



class WindowException(Exception):
    '''The root exception for all window-related errors.'''
    pass




class Window(event.EventDispatcher):
    '''Platform independent window.

    The content area of a window is filled entirely with an OpenGL viewport.
    Applications have no access to operating system widgets or controls; all
    rendering must be done via OpenGL.

    Windows may appear as floating regions or can be set to fill an entire
    screen (fullscreen).  When floating, windows may appear borderless or
    decorated with a platform-specific frame (including, for example, the
    title bar, minimize and close buttons, resize handles, and so on).

    While it is possible to set the location of a window, it is recommended
    that applications allow the platform to place it according to local
    conventions.  This will ensure it is not obscured by other windows,
    and appears on an appropriate screen for the user.

    It is the responsability of the window backend to dispatch the following
    events when necessary:

    Keyboard::

      def on_key_press(symbol, modifiers):
          'A key on the keyboard was pressed.'
          pass

      def on_key_release(symbol, modifiers):
          'A key on the keyboard was released.'
          pass


    Mouse::

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


    Window::

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


    def __init__( self, size=(640,480), position=(0,0), title=None ):
        '''
        Create a window with given size, position and title.

        :Parameters:

        ``size``: (int,int)
            Initial window size as (width,height) in pixels.

        ``position``: (int,int)
            Initial window position. Depending on the window-manager, the
            position request may or may not be honored.

        ``title``: str
            Window title
        '''
        if size is not None:
            self._width, self._height = size
        if position is not None:
            self._x, self._y = position
        

    def show(self):
        '''
        The show() method causes a window to be displayed as soon as possible.
        '''

        raise NotImplemented


    def hide(self):
        '''
        The hide() method reverses the effects of the show() method, causing
        the window to be hidden (removed from the display).
        '''

        raise NotImplemented


    def redraw(self):
        '''
        The redrawa() method invalidates the window area. Once the main loop
        becomes idle (after the current batch of events has been processed,
        roughly), the window will dispatch a ``draw`` event and swaps the
        buffers if double buffered.
        '''

        raise NotImplemented


    def refresh(self):
        ''' Refresh the window content by swapping back and fron buffer.. '''

        raise NotImplemented


    def set_fullscreen(self, state):
        '''
        If `state` is True, the set_fullscreen() method requests the window
        manager to place the window in the fullscreen state. If `state` is
        False the set_fullscreen() method requests the window manager to toggle
        off the fullscreen state for the window. Note that in any case, you
        shouldn't not assume the window state is definitely set afterward,
        because other entities (e.g. the user or window manager) could
        fullscreen/unfullscreen it again, and not all window managers honor
        requests to fullscreen windows.

        :param bool state:
            Fullscreen state to be set.

        '''

        raise NotImplemented


    def get_fullscreen(self):
        '''
        Return whether window is currently in fullscreen state or not.
        '''

        raise NotImplemented


    def set_title(self, title):
        '''
        The set_title() method sets the "title" property of the Window to the
        value specified by title. The title of a window will be displayed in
        its title bar. On the X Window System, the title bar is rendered by the
        window manager, so exactly how the title appears to users may vary
        according to a user's exact configuration. The title should help a user
        distinguish this window from other windows they may have open. A good
        title might include the application name and current document filename.

        :Parameters:

            ``title`` : str
                the title of the window
        '''

        raise NotImplemented


    def get_title(self):
        '''

        The get_title() method returns the value of the "title" property of the
        window. See the set_title() method.

        :rtype: str
        :return: the title of the window
        '''

        raise NotImplemented


    def set_size(self, width, height):
        '''
        The set_size() method requests the window manager to resize the window
        to the specified width and height as if the user had done so, obeying
        geometry constraints. Note you shouldn't assume the new window size is
        definitely the requested one afterward, because other entities (e.g. the user
        or window manager) could change it ssize again, and not all window
        managers honor requests to resize windows. 

        :Parameters:

            ``width`` : int
                The width in pixels to resize the window to

            ``height`` : int
                The height in pixels to resize the window to
        '''

        raise NotImplemented


    def get_size(self):
        '''
        The get_size() methods returns the current size of the window and does
        not include the size of the window manager decorations (aka the window
        frame or border). 

        :rtype: (int, int)

        :return: The width and height of the window, in pixels.
        '''

        raise NotImplemented


    def set_position(self, x, y):
        '''
        The set_position() method requests the window manager to move the
        window to the specified coordinates as if the user had done so, obeying
        geometry constraints. Note you shouldn't assume the new window position
        is definitely the requested one afterward, because other entities
        (e.g. the user or window manager) could change it position again, and
        not all window managers honor requests to move windows.

        :param integer x:
            The x coordinate in pixels to move the window to

        :param integer y:
            The y coordinate in pixels to move the window to
        '''

        raise NotImplemented


    def get_position(self):
        '''
        The get_position() method returns the current posiiton of the window. 

        :rtype: (int, int)
        :return: The current window coordinates, in pixels.
        '''

        raise NotImplemented



    def timer( self, fps ):
        '''Function decorator for timed handlers.
        

        :Parameters:

            ``fps``: int
                Frames per second

        Usage::

            win = window.Window()
            @win.timer(60)
            def timer(dt):
                do_something ...
        '''

        def decorator(func):
            self._timer_stack.append((func, fps))
            self._timer_date.append(0)
            return func
        return decorator



    title = property(lambda self: self._title,
         doc='''
         Window title. Read-only.
         ''')

    width = property(lambda self: self._width,
         doc='''
         Window width in pixels. Read-only.
         ''')

    height = property(lambda self: self._height,
         doc='''
         Window height in pixels. Read-only.
         ''')

    x = property(lambda self: self._x,
         doc='''
         Window x coordinate. Read-only.
         ''')

    y = property(lambda self: self._y,
         doc='''
         Window x coordinate. Read-only.
         ''')



Window.register_event_type('on_key_press')
Window.register_event_type('on_key_release')
Window.register_event_type('on_mouse_motion')
Window.register_event_type('on_mouse_drag')
Window.register_event_type('on_mouse_press')
Window.register_event_type('on_mouse_release')
Window.register_event_type('on_mouse_scroll')
Window.register_event_type('on_mouse_enter')
Window.register_event_type('on_mouse_leave')
Window.register_event_type('on_init')
Window.register_event_type('on_show')
Window.register_event_type('on_hide')
Window.register_event_type('on_resize')
Window.register_event_type('on_draw')
Window.register_event_type('on_idle')

