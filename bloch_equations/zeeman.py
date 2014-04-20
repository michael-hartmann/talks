#!/usr/bin/python

from __future__ import division
from pyx import *

texter = graph.axis.texter.decimal(labelattrs=[color.grey(1)])
g = graph.graphxy(width=8,
                  x=graph.axis.lin(title=r"$H$", density=0.0001, texter=texter),
                  y=graph.axis.lin(title=r"$E$", density=0.0001, texter=texter, max=2.5, min=-2.5))

l = [ -5, -3, -1, 1, 3, 5]
d = [0.1, 0.1, 0.15, 0.2, 0.3, 0.2]
for i in range(6):
  f = "y(x)=%f*x" % ((i-2.5)*0.1)
  g.plot(graph.data.function(f, min=0, max=10), [graph.style.line()])

  xpos,  ypos = g.pos(8, d[i]+0.4+(i-3)*0.8)
  latex = "$m=%d/2$" % l[i]
  g.text(xpos,ypos, latex, [text.size.tiny])

g.writePDFfile("zeeman")
