#!/usr/bin/python

from __future__ import division
import numpy as np
from math import *

def rk4(f, y0, t0, t, steps, args=None):
    h = (t-t0)/steps
    solution = [(t0,y0)]
    for i in range(1,steps):
        ti, yi = solution[-1]
        dyi = f(ti,yi,args)
        ya  = yi+h/2*dyi
        dya = f(ti+h/2,ya,args)
        yb  = yi+h/2*dya
        dyb = f(ti+h/2,yb,args)
        yc  = yi+h*dyb
        dyc = f(ti+h,yc,args)

        y1 = yi + h/6*(dyi + 2*(dya+dyb) + dyc)
        solution.append((t0+(i+1)*h,y1))

    return solution
