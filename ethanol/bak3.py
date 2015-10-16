#!/usr/bin/python

from __future__ import division
import numpy as np
from pyx import *
from math import exp,log

text.set(mode="latex")
text.preamble(r"\usepackage{wasysym}")

kappa     = 0.46
rm        = 0.68
rf        = 0.55
m_koerper = 65
gamma     = 0.15

m0 = 0.7*0.789*0.4 * 1000

print m0
print log( (kappa*m0)/(gamma*rm*m_koerper) ) / kappa
print log( (kappa*m0)/(gamma*rf*m_koerper) ) / kappa

data = []
for t in np.linspace(0,6,250):
    cm = m0/(rm*m_koerper)*(1-exp(-kappa*t))-gamma*t
    cf = m0/(rf*m_koerper)*(1-exp(-kappa*t))-gamma*t
    data.append((t, cm, cf))

g = graph.graphxy(
    width = 6,
    key=graph.key.key(pos="br", dist=0.1),
    x = graph.axis.lin(title=r"$t$ in h"),
    y = graph.axis.lin(title=r"$c_\mathrm{BAK}$ in $\permil$")
)

g.plot([
    graph.data.points(data, x=1, y=2, title=r"\mars"),
    graph.data.points(data, x=1, y=3, title=r"\female")
  ], [graph.style.line([color.gradient.RedBlue])])

g.writePDFfile("bak3_2.pdf")
