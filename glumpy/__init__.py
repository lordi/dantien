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
import numpy

import colormap
from image import Image
from window import Window, show
from figure import Figure
from trackball import Trackball
from graphics import VertexBuffer

from version import version as __version__




# ------------------------------------------------------------------ figure ---
def figure(size = (800,600), position = (0,0)):
    '''
    Helper function to create a figure.

    This function first creates a Window and creates a figure whose viewport
    covers the entire window.

    :Parameters:

    ``size``: (int, int)
        Figure size (pixels).

    ``position``: (int,int)
        Figure position.

    .. note::

       Depending on the window manager, the position request may or may not be
       not honored.
    '''
 
    return Figure(size=size, position=position, parent=None)



# ------------------------------------------------------------------ imshow ---
def imshow(data):
    '''
    Helper function to show an image.
    '''
    import PIL

    figure= active_figure()
    frame = active_frame()

    if type(data) is str:
        filename = data
        Z = numpy.asarray(PIL.Image.open(data))
        Z = (Z/256.0).astype(numpy.float32)

    image = Image( Z, colormap = colormap.Hot )
    frame.set_aspect( I.shape[1]/float(I.shape[0]) )
    
    subfigure = glumpy.Figure( size=(.5,.05), position=(.45,.90), parent=figure )
    subframe  = subfig.add_frame( size=(1,1), aspect = 10.0 )

    C = numpy.linspace(0,1,256).astype(numpy.float32).reshape(1,256)
    colorbar = glumpy.image.Image(C, colormap=colormap.Hot)

    @figure.event
    def on_draw( ):
        figure.clear(1,1,1,0)
        frame.draw( x=frame.X, y=frame.Y )
        image.draw( x=frame.X, y=frame.Y,  z = 0,
                    width=frame.width, height=frame.height )
        subframe.draw( x=frame.X+5, y=frame.Y+5 )
        colorbar.draw( x=frame.X+5, y=frame.Y+5, z = 1,
                       width=subframe.width, height=subframe.height )    
