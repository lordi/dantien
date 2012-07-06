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
import numpy as np
import OpenGL.GL as gl
from glumpy.image.filter import Filter
from glumpy.graphics import VertexBuffer
from glumpy.image.texture import Texture





class ImageException(Exception):
    '''The root exception for all image related errors.'''
    pass



class Image(object):
    '''
    '''

    def __init__(self, Z, format=None, vmin=None, vmax=None,
                 interpolation=None, origin='lower',
                 colormap = None, gamma=1.0, elevation=0.0,
                 grid_size = (0.0,0.0,0.0), grid_offset=(0.5,0.5,0.0), 
                 grid_color = (0.0,0.0,0.0,1.0), grid_thickness = (1.0,1.0,1.0) ):

        ''' Creates a texture from numpy array.

        :Parameters:
        ``Z`` : numpy array
            Z may be a float32 or uint8 array with following shapes:
                * M
                * MxN
                * MxNx[1,2,3,4]

        ``format``: [None | 'A' | 'LA' | 'RGB' | 'RGBA']
            Specify the texture format to use. Most of times it is possible to
            find it automatically but there are a few cases where it not
            possible to decide. For example an array with shape (M,3) can be
            considered as 2D alpha texture of size (M,3) or a 1D RGB texture of
            size (M,).

        ``interpolation``: str or None
             Spatial interpolation. Acceptable values are None,
            'nearest', 'bilinear', 'bicubic', 'spline16', 'spline36',
            'hanning', 'hamming', 'hermite', 'kaiser', 'quadric', 'catrom',
            'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos'

        ``colormap``: Colormap or None
            Color interpolation that takes the alpha value of an image to
            transform it to a r,g,b triplet.

        ``vmin``: scalar
            Minimal representable value.

        ``vmax``: scalar
            Maximal representable value.

        ``gamma``: float
            Gamma correction.

        ``elevation``: float
            Elevation of the z vertices of the current bound object.

        ``grid_size`: tuple of 3 floats
            Grid size. To get n isolines, uses (0,0,n).

        ``grid_offset`: tuple of 3 floats
            Grid offset.

        ``grid_color`: tuple of 3 floats
            Grid color.

        ``grid_thickness`: tuple of 3 floats
            Grid thickness.

        ``origin``: 'lower' or 'upper'
            Place the [0,0] index of the array in the upper left or lower left
            corner.
        '''

        self._texture = Texture(Z)
        if self._texture.dst_format in [gl.GL_RGB, gl.GL_RGBA]:
            colormap = None

        self._filter = Filter(interpolation, colormap, gamma, elevation,
                             grid_size, grid_offset, grid_color, grid_thickness)
        self._origin = origin
        self._vmin = vmin
        self._vmax = vmax
        self._data = Z
        self.update()

        n = 16
        xyz  = np.dtype( [('x','f4'), ('y','f4'), ('z','f4')] )
        uv   = np.dtype( [('u','f4'), ('v','f4')] )
        self._vertices = np.zeros( (n,n), dtype = [ ('position',  xyz),
                                                    ('tex_coord', uv) ] )
        u,v = np.mgrid[0:n,0:n]/float(n-1)
        self._vertices['tex_coord']['u'] = u
        self._vertices['tex_coord']['v'] = v
        x,y = np.ogrid[0:n-1,0:n-1]
        self._indices = np.zeros( (n-1,n-1,4), dtype = 'u4' )
        self._indices[x,y,0] = y*n+x
        self._indices[x,y,1] = y*n+x+1
        self._indices[x,y,2] = y*n+x+n+1
        self._indices[x,y,3] = y*n+x+n
        V = self._vertices.view( dtype = [ ('position',  'f4', 3),
                                           ('tex_coord', 'f4', 2) ] )
        self._mesh = VertexBuffer(V, self._indices.ravel())


    width = property(lambda self: self._data.shape[1],
         doc='''The width of the image.  Read-only.
         
         :type: int
         ''')

    height = property(lambda self: self._data.shape[0],
         doc='''The height of the image.  Read-only.
         
         :type: int
         ''')

    data = property(lambda self: self._data,
         doc='''The underlying image data.  Read-only.
         
         :type: numpy.ndarray
         ''')

    texture = property(lambda self: self._texture,
         doc='''A ``Texture`` view of this image.  
         
         :type: glumpy.image.Texture
         ''')

    @property
    def format(self):
        ''' Array representation format (string). '''
        format = self._texture.src_format
        if format == gl.GL_ALPHA:
            return 'A'
        elif format == gl.GL_LUMINANCE_ALPHA:
            return 'LA'
        elif format == gl.GL_RGB:
            return 'RGB'
        elif format == gl.GL_RGBA:
            return 'RGBA'


        
    def update(self):
        ''' Data update. '''
        if self._vmin is None:
            vmin = self._data.min()
        else:
            vmin = self._vmin
        if self._vmax is None:
            vmax = self._data.max()
        else:
            vmax = self._vmax
        if vmin == vmax:
            vmin, vmax = 0, 1

        colormap = self._filter.colormap
        if colormap:
            s = colormap.size
            self._texture.update(bias = 1.0/(s-1)-vmin*((s-3.1)/(s-1))/(vmax-vmin),
                                 scale = ((s-3.1)/(s-1))/(vmax-vmin))
        else:
            self._texture.update(bias=-vmin/(vmax-vmin),scale=1.0/(vmax-vmin))


    def draw(self, x, y, z, width, height):
        ''' Blit array onto active framebuffer. '''

        self._filter.activate( self._texture )
        #if self.origin == 'lower':
        #    t=0,1
        #else:
        #    t=1,0
        gl.glEnable( self._texture.target )
        gl.glEnable( gl.GL_BLEND )
        gl.glColor( 1, 1, 1, 1 )
        gl.glBindTexture( self._texture.target, self._texture.id )

        n = self._vertices.shape[0]
        mx, my = np.mgrid[0:n,0:n]/float(n-1)
        self._vertices['position']['x'] = x + width * mx
        self._vertices['position']['y'] = y + height*(1-my)
        self._vertices['position']['z'] = z
        self._mesh.upload()
        self._mesh.draw()

        self._filter.deactivate( )
