#!/usr/bin/python3
# -*- coding: utf-8 -*-

from optparse import OptionParser
from scipy import integrate
import numpy as np
from math import *
from DoublePendulum import DoublePendulum, arcsimp
from sys import stderr

# start
parser = OptionParser()
parser.add_option("--theta1",    action="store", type="float",  dest="Θ1",  help="initial value for Θ1 (in rad); default: 2",  default=2)
parser.add_option("--theta2",    action="store", type="float",  dest="Θ2",  help="initial value for Θ2 (in rad); default: 3",  default=3)
parser.add_option("--dtheta1",   action="store", type="float",  dest="dΘ1", help="initial value for dΘ1 (in rad/s); default: 0", default=0)
parser.add_option("--dtheta2",   action="store", type="float",  dest="dΘ2", help="initial value for dΘ2 (in rad/s); default: 0", default=0)
parser.add_option("--l",         action="store", type="float",  dest="l",   help="value for l; default: 1",             default=1)
parser.add_option("--m",         action="store", type="float",  dest="m",   help="value for m; default: 1",             default=1)
parser.add_option("-g",          action="store", type="float",  dest="g",   help="value for g; default: 9.81",          default=9.81)
parser.add_option("-f", "--fps", action="store", type="float",  dest="fps", help="frames per second; default: 30",      default=30)
parser.add_option("-t",          action="store", type="float",  dest="te",  help="duration of simulation; default: 30", default=30)

(options, args) = parser.parse_args()

l   = options.l
g   = options.g
m   = options.m
te  = options.te
fps = options.fps

#anfangsbedingungen
Θ1  = options.Θ1
Θ2  = options.Θ2
dΘ1 = options.dΘ1
dΘ2 = options.dΘ2

print("%e, %e, %e, %e" % (l,m,g,options.fps))


pendulum = DoublePendulum(l, m, g)
solution = pendulum.integrate((Θ1, Θ2, dΘ1, dΘ2), int(te*fps), skip=200, h=1/fps/200)
print("E=%.4f" % pendulum.E(Θ1, Θ2, dΘ1, dΘ2), file=stderr)

for n in range(len(solution)):
    t,Θ1,Θ2,dΘ1,dΘ2 = solution[n]
    En = pendulum.E(Θ1, Θ2, dΘ1, dΘ2)
    print(En, file=stderr)
    print("%.6f, %e, %e, %e, %e, %e" % (t, Θ1, Θ2, dΘ1, dΘ2, En))
