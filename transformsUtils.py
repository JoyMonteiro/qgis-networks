import rasterio
import numpy as np
from affine import Affine

def pixelToCoordFn(raster):
    """ Converts from pixel indices to actual coordinates.
    
    :param raster: file for which the coordinates have to be calculated
    :param x: x coordinate
    :param y: y coordinate
    :returns transFunc: function which does the transformation
    
    """
    
    with rasterio.open(raster, 'r') as rasterFile:
        T0 = rasterFile.affine
        
    #By default, transformation is for pixel edge. convert to centre
    T1 = T0#*Affine.translation(0.5,0.5)
    
    transFunc = lambda (r, c): (c, r) * T1
    
    return transFunc
            

def coordToPixelFn(raster):
    """ Converts from actual coordinates to pixel indices.
    
    :param raster: file for which the coordinates have to be calculated
    :param x: x coordinate
    :param y: y coordinate
    :returns transFunc: function which does the transformation
    
    """
    
    with rasterio.open(raster, 'r') as rasterFile:
        T0 = rasterFile.affine
        
    a1 = 1./T0.a
    b1 = T0.b
    c1 = -T0.c/T0.a
    
    d1 = T0.d
    e1 = 1/T0.e
    f1 = -T0.f/T0.e
    
    #print T0.a, T0.b, T0.c, T0.d, T0.e, T0.f
    T0 = Affine(a1,b1,c1,d1,e1,f1)
    #print T0.a, T0.b, T0.c, T0.d, T0.e, T0.f
    #print T0*(69.99958357546711, 20.000417005657994)
    
    #By default, transformation is for pixel edge. convert to centre
    T1 = T0#*Affine.translation(0.5,0.5)    
    
    transFunc = lambda (r, c): tuple(np.array((r, c)*T1)[::-1])
    
    return transFunc    



