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
import string
import glumpy
from raw import *

def _make_glumpy_map():
    ret = {}
    for c in string.letters:
        ret[getattr(glumpy.window.key, c.upper())] = ord(c)
    for c in string.digits:
        ret[getattr(glumpy.window.key, "_"+c)] = ord(c)
    ret.update({
            glumpy.window.key.SPACE:     ord(' '),
            glumpy.window.key.BACKSPACE: ord('\b'),
            glumpy.window.key.RETURN:    ord('\r'),
            glumpy.window.key.PERIOD:    ord('.'),
            glumpy.window.key.MINUS:     ord('-'),
    })
    return ret

_glumpy_key_map = _make_glumpy_map()

_glumpy_button_map = {
    glumpy.window.mouse.LEFT:   TW_MOUSE_LEFT,
    glumpy.window.mouse.MIDDLE: TW_MOUSE_MIDDLE,
    glumpy.window.mouse.RIGHT:  TW_MOUSE_RIGHT,
}

def map_key(key):
    return _glumpy_key_map[key]

def map_button(button):
    return _glumpy_button_map[button]

def map_modifiers(modifiers):
    ret = TW_KMOD_NONE
    if modifiers & glumpy.window.key.MOD_SHIFT:
        ret |= TW_KMOD_SHIFT
    if modifiers & glumpy.window.key.MOD_CTRL:
        ret |= TW_KMOD_CTRL
    if modifiers & glumpy.window.key.MOD_ALT:
        ret |= TW_KMOD_ALT
    return ret


class Handlers(object):

    def __init__(self, window):
        self.window = window

    def on_resize(self, width, height):
        TwWindowSize(width, height)

    def on_key_press(self, symbol, modifiers):
        try:
            TwKeyPressed(map_key(symbol), map_modifiers(modifiers))
            self.window.redraw()
            return True
        except:
            pass 
        return False
    def on_mouse_press(self, x, y, button):
        if not button in _glumpy_button_map.keys():
            return False
        if TwMouseButton(TW_MOUSE_PRESSED, map_button(button)):
            self.window.redraw()
            return True

    def on_mouse_release(self, x, y, button):
        if not button in _glumpy_button_map.keys():
            return False
        if TwMouseButton(TW_MOUSE_RELEASED, map_button(button)):
            self.window.redraw()
            return True

    def on_mouse_drag(self, x, y, dx, dy, buttons):
        if TwMouseMotion(x, self.window.height-y):
            self.window.redraw()
            return True

    def on_mouse_motion(self, x, y, dx, dy):
        if TwMouseMotion(x, self.window.height-y):
            self.window.redraw()
            return True

    def on_draw(self):
        TwDraw()
