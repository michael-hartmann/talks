#!/usr/bin/python

from __future__ import division
import numpy as np
from scipy.integrate import odeint
from pyx import *

text.set(mode="latex")
text.preamble(r"\usepackage{wasysym}")

def dgl(c,t):
    if c > 0:
        return -gamma
    else:
        return 0

cbak0 = 1.0
data  = []
plots = []
for gamma in [0.12, 0.15, 0.3]:
    print gamma
    times = np.linspace(0,10,200)
    y = odeint(dgl, [cbak0], times)

    data.append([])
    for i,elem in enumerate(y):
        t    = times[i]
        cbak = y[i][0]
        if cbak < 0:
            cbak = 0
        data[-1].append((t,cbak))

    title = r"$\gamma=%.2f$" % gamma
    plots.append(graph.data.points(data[-1], x=1, y=2, title=title))

g = graph.graphxy(
    width=8,
    key = graph.key.key(pos="tr"),
    x = graph.axis.lin(title="$t$ in h", min=0, max=10),
    y = graph.axis.lin(title="$c_\mathrm{BAK}$ in $\permil$", min=0, max=1)
)

g.plot(plots, [graph.style.line([color.gradient.RedBlue])])

g.writePDFfile()
