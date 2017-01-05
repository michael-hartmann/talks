#!/usr/bin/python

from __future__ import division
import numpy as np
from pyx import *
from rk4 import rk4

text.set(mode="latex")
text.preamble(r"\usepackage{wasysym}")

rho_ethanol = 0.789 # density ethanol
V           = 2     # volume
Vprozent    = 5     # percent of ethanol
kappa       = 0.35  # 1.38 (leer), 0.69 (klein), 0.46 (normal), 0.35 (groß)
r           = 0.68  # male: 0.68, female: 0.55
m_koerper   = 65    # body mass
gamma       = 0.15  # male: 0.12, 0.15, 0.30; female: 0.10, 0.13, 0.26
alpha       = kappa/(r*m_koerper)

# mass current function
def I(t,te):
    if t >= 0 and t <= te:
        return rho_ethanol*V*Vprozent/100*1000/te
    else:
        return 0

# differential equation
def dgl(t,y,args):
    te = args
    m_magen, c_bak = y

    dm_magen = I(t,te)-kappa*m_magen
    dc_bak = alpha*m_magen
    if c_bak > 0:
        dc_bak -= gamma

    return np.array((dm_magen, dc_bak))


data  = []
plots = []

for te in (1,2,3,4,5):
    y = rk4(dgl, np.array((0,0)), 0, 14, 1500, args=te)

    data.append([])
    for i,elem in enumerate(y):
        t,cbak = y[i][0],y[i][1][1]
        if cbak < 0:
            cbak = 0
        data[-1].append((t,cbak))

    plots.append(graph.data.points(data[-1], x=1, y=2, title=r"$t_e=%d$" % te))

g = graph.graphxy(
    key=graph.key.key(pos="tr", dist=0.1),
    width = 10,
    x = graph.axis.lin(title=r"$t$", max=10),
    y = graph.axis.lin(title=r"$c_\mathrm{BAK}$ in $\permil$")
)

g.plot(plots, [graph.style.line([color.gradient.RedBlue])])
g.stroke(g.ygridpath(0.5), [style.linestyle.dashed])


g.writePDFfile()
