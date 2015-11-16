#!/usr/bin/python3

from math import sin,pi
from pyx import *
from scipy.integrate import odeint
import numpy as np

def plot(g,phi0,alpha0, arrow=True):
    y0 = np.array([phi0,alpha0])
    d = []
    for i,(alpha,phi) in enumerate(odeint(f, y0, times)):
        d.append((alpha,phi))

    if arrow:
        g.plot(graph.data.points(d, x=1, y=2), [graph.style.line([deco.arrow(pos=0.05)])])
    else:
        g.plot(graph.data.points(d, x=1, y=2), [graph.style.line()])


def f(y,t, omega=1):
    phi,alpha = y
    return np.array([alpha, -omega**2*sin(phi)])

g = graph.graphxy(
    width = 8,
    x     = graph.axis.lin(title=r"$\varphi$", divisor=pi, texter=graph.axis.texter.rational(suffix=r"\pi"), min=-3.2*pi, max=3.2*pi),
    y     = graph.axis.lin(title=r"$\dot\varphi$", min=-3, max=3)
)

times = np.linspace(0,50,1500)

for phi0 in np.linspace(-pi-1e-1, pi+1e-1, 8):
    plot(g,phi0,0)
    plot(g,phi0+2*pi,0)
    plot(g,phi0-2*pi,0)

plot(g,0,0.01, arrow=False)
plot(g,2*pi,0.01, arrow=False)
plot(g,-2*pi,0.01, arrow=False)

for alpha0 in (2.5,2.9):
    plot(g,-6*pi,alpha0)
    plot(g,6*pi,-alpha0)

plot(g,-5*pi,0.7)
plot(g,5*pi,-0.7)

g.writePDFfile()
