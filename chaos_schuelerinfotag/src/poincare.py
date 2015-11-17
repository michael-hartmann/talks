#!/usr/bin/python
# -*- coding: utf-8 -*-

from optparse import OptionParser
from DoublePendulum import DoublePendulum
from math import *
import sys, string
from random import random,seed
from PIL import Image, ImageFont, ImageDraw


def theta1_to_X(theta1):
    x = round((theta1+theta1_max)/(2*theta1_max)*res, 0)
    return min(res, max(0,x))

def dtheta1_to_Y(dtheta1):
    y = res-round((dtheta1-dtheta1_min)/(dtheta1_max-dtheta1_min)*res, 0)
    return min(res, max(0,y))


seed(0)

# kommandozeilen parameter parsen
parser = OptionParser()
parser.add_option("--m", action="store", type="float", dest="m", help="set value of m (default: 1)",   default=1) 
parser.add_option("--l", action="store", type="float", dest="l", help="set value of l (default: 1)",   default=1) 
parser.add_option("-g",  action="store", type="float", dest="g", help="set value of g (default 9.81)", default=9.81) 

parser.add_option("-n", "--grid",   action="store", type="int",    dest="n",      help="set grid of initial points (default: 10)", default=10) 
parser.add_option("-N", "--amount", action="store", type="int",    dest="N",      help="set amount of points per initial condition (default: 1000)", default=1000)
parser.add_option("-E", "--energy", action="store", type="float",  dest="E",      help="set energy", default=10)
parser.add_option("-o", "--output", action="store", type="string", dest="output", help="set output; omit file suffix (default: poincare)", default="poincare")
parser.add_option("-s", "--stdin",  action="store_true",           dest="stdin",  help="read from stdin (format: x,px,N); (default: False)", default=False)

parser.add_option("-d", "--dump",       action="store_true", dest="dump",                 help="read from stdin (format: x,px,N); (default: False)", default=False)
parser.add_option("-p", "--pyx",        action="store_true", dest="pyx",                  help="read from stdin (format: x,px,N); (default: False)", default=False)
parser.add_option("-r", "--resolution", action="store", type="string", dest="resolution", help="read from stdin (format: x,px,N); (default: False)", default=600)
parser.add_option("-f", "--fps",        action="store", type="int", dest="fps",           help="read from stdin (format: x,px,N); (default: False)", default=250)


(options, args) = parser.parse_args()

n      = options.n
N      = options.N
output = options.output
E0     = options.E
stdin  = options.stdin
dump   = options.dump
pyx    = options.pyx
res    = options.resolution
fps    = options.fps


# Liste der Anfangspunkte auf dem Poincare-Plot
iv = []
points = {}
pendulum = DoublePendulum(options.l, options.m, options.g)

# groesst moeglichsten Winkel für Θ1 berechnen
# das ist der Fall, wenn die kinetische Energie T=0 und Θ2=0:
# E = g*m*l1*(1-cos(Θ1)) => nach Θ1 aufloesen
theta1_min, theta1_max   = pendulum.theta1_max(E0)
dtheta1_min, dtheta1_max = pendulum.dtheta1_max(E0)

if stdin:
    # punkte von stdin lesen
    lines = sys.stdin.read().split("\n")
    for line in lines[:-1]:
        if line.find("#") == 0:
            continue

        theta1,dtheta1,N = line.split(",")
        iv.append( (float(theta1), float(dtheta1), int(N)) )
else:
    for theta1 in (2*theta1_max/3, theta1_max/3, 0, -2*theta1_max/3, -theta1_max/3):
        delta   = (2*dtheta1_max)/n
        dtheta1 = dtheta1_min+delta/2
        while dtheta1 < dtheta1_max:
            if pendulum.E(theta1,0,dtheta1,0) < E0:
                iv.append( (theta1, dtheta1, N) )
            dtheta1 += delta


progress = 0

for theta1,dtheta1,N in iv:
    # poincare punkte
    points[ (theta1,dtheta1) ] = pendulum.poincare(E0, theta1, dtheta1, N)
    progress += 1
    print("%.2f%%" % (progress/len(iv)*100))

if dump:
    import yaml
    stream = file(output + ".yaml", "w")
    yaml.dump(points, stream)


if pyx:
    from pyx import *
    # pyx farben
    colors = [
      color.cmyk.Apricot, color.cmyk.Aquamarine, color.cmyk.Bittersweet,
      color.cmyk.Black, color.cmyk.Blue, color.cmyk.BlueGreen, color.cmyk.BlueViolet,
      color.cmyk.BrickRed, color.cmyk.Brown, color.cmyk.BurntOrange,
      color.cmyk.CadetBlue, color.cmyk.CarnationPink, color.cmyk.Cerulean,
      color.cmyk.CornflowerBlue, color.cmyk.Cyan, color.cmyk.Dandelion,
      color.cmyk.DarkOrchid, color.cmyk.Emerald, color.cmyk.ForestGreen,
      color.cmyk.Fuchsia, color.cmyk.Goldenrod, color.cmyk.Gray, color.cmyk.Green,
      color.cmyk.GreenYellow, color.cmyk.Grey, color.cmyk.JungleGreen,
      color.cmyk.Lavender, color.cmyk.LimeGreen, color.cmyk.Magenta,
      color.cmyk.Mahogany, color.cmyk.Maroon, color.cmyk.Melon,
      color.cmyk.MidnightBlue, color.cmyk.Mulberry, color.cmyk.NavyBlue,
      color.cmyk.OliveGreen, color.cmyk.Orange, color.cmyk.OrangeRed,
      color.cmyk.Orchid, color.cmyk.Peach, color.cmyk.Periwinkle,
      color.cmyk.PineGreen, color.cmyk.Plum, color.cmyk.ProcessBlue,
      color.cmyk.Purple, color.cmyk.RawSienna, color.cmyk.Red, color.cmyk.RedOrange,
      color.cmyk.RedViolet, color.cmyk.Rhodamine, color.cmyk.RoyalBlue,
      color.cmyk.RoyalPurple, color.cmyk.RubineRed, color.cmyk.Salmon,
      color.cmyk.SeaGreen, color.cmyk.Sepia, color.cmyk.SkyBlue,
      color.cmyk.SpringGreen, color.cmyk.Tan, color.cmyk.TealBlue,
      color.cmyk.Thistle, color.cmyk.Turquoise, color.cmyk.Violet,
      color.cmyk.VioletRed, color.cmyk.White, color.cmyk.WildStrawberry,
      color.cmyk.Yellow, color.cmyk.YellowGreen, color.cmyk.YellowOrange
    ]

    xaxis = graph.axis.axis.lin(min=1.05*theta1_min, max=1.05*theta1_max, title = r"$\theta_1$", divisor=pi, texter=graph.axis.texter.rational(suffix=r"\pi"))
    yaxis = graph.axis.axis.lin(min=1.04*dtheta1_min, max=1.05*dtheta1_max, title = r"$\dot\theta_1$")
    g = graph.graphxy(
        width = 12,
        x     = xaxis,
        y     = yaxis
    )

    # t, theta1, theta2, dtheta1, p2
    for iv in points.keys():
        color = colors[int(random()*len(colors))]
        pyx_circle = [graph.style.symbol(graph.style.symbol.circle, symbolattrs=[deco.filled, color], size=0.007)]
        pyx_cross  = [graph.style.symbol(graph.style.symbol.cross, symbolattrs=[deco.filled, color])]
        g.plot(graph.data.values(x=[iv[0]], y=[iv[1]]), styles=pyx_cross)
        g.plot(graph.data.points(points[iv], x=1, y=2), styles=pyx_circle)

    g.writePDFfile("%s.pdf" % output)
else:
    im = Image.new("RGB", (res+1,res+1), "White")
    pix = im.load()

    for iv in points:
        colour = (int(random()*200), int(random()*200), int(random()*200))

        #print iv
        # kreuz fuer startpunkt zeichnen
        X = theta1_to_X(iv[0])
        Y = dtheta1_to_Y(iv[1])
        pix[X,Y] = colour
        for i in range(10):
            try:
              pix[X+i,Y] = colour
            except:
              pass
            try:
              pix[X-i,Y] = colour
            except:
              pass
            try:
              pix[X,Y+i] = colour
            except:
              pass
            try:
              pix[X,Y-i] = colour
            except:
              pass

        for (theta1, dtheta1) in points[iv]:
            X = theta1_to_X(theta1)
            Y = dtheta1_to_Y(dtheta1)
            pix[X,Y] = colour


    draw = ImageDraw.Draw(im)
    font = ImageFont.load_default()
    text = "E=%.6f" % (E0)
    #text = "m2=%.6f" % (m2)
    draw.text((5, 5), text, font=font, fill=(0,0,0))
    im.save("%s.png" % output)
