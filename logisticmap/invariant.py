#!/usr/bin/python

from pyx import *
from math import *

def f(x,alpha=4):
    return alpha*x*(1-x)

x = 0.4
N = int(1e5)
Nbins = 200
bins = [0]*Nbins

for i in range(N):
    x = f(x)
    bins[int(x*Nbins)] += 1

for i in range(Nbins):
    bins[i] *= Nbins/N

xaxis = [ i/Nbins+0.5/Nbins for i in range(Nbins)]


g = graph.graphxy(
    key   = graph.key.key(pos="tr", dist=0.1),
    width = 6,
    x     = graph.axis.lin(title=r"$x$"),
    y     = graph.axis.lin(title=r"$\varrho(x)$", max=10)
)

g.plot(graph.data.values(x=xaxis, y=bins, title=r"$10^5$ points"), [graph.style.symbol(graph.style.symbol.changecircle, size=0.04, symbolattrs=[color.gradient.RedBlue])])

f = "y(x) = %.10g/sqrt(x*(1-x))" % (1./pi)
g.plot(graph.data.function(f, points=1000, min=1e-5, max=1-1e-5, title=r"$\varrho(x) = {1\over{\pi\sqrt{x(1-x)}}}$"))

g.writePDFfile("invariantmeassure")
