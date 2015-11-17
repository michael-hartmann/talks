#!/usr/bin/python

from __future__ import division
from tempfile import mkdtemp
from optparse import OptionParser
from math import *
from copy import deepcopy
import os, csv, cairo

# start
parser = OptionParser()
parser.add_option("-i", "--input",      action="store", type="string",  dest="infile",      help="input csv-file; default: pendulum.csv",  default="pendulum.csv")
parser.add_option("-r", "--resolution", action="store", type="int",     dest="resolution",  help="set resolution; default: 600",  default=600)
parser.add_option("-o", "--output",     action="store", type="string",  dest="outfile",     help="output file; default pendulum.mp4",   default="pendulum.mp4")
parser.add_option("-q", "--silent",     action="store_true",            dest="silent",      help="don't output to stdout", default=False)
parser.add_option("-t", "--trace",      action="store_true",            dest="trace",       help="show trace; default: False", default=False)

(options, args) = parser.parse_args()

resolution = options.resolution
infile     = options.infile
output     = options.outfile
trace      = options.trace

states = []
with open(infile, "r") as f:
    (l, m, g, fps) = map(float, f.readline().split(","))

    csvReader = csv.reader(f, delimiter=',', quotechar='|')
    for row in csvReader:
        states.append(list(map(float, row)))

deltal = 0.47/(2*l)

i = 0
modulo = int(log10(len(states)))+1
outdir = mkdtemp()

points = []
for state in states:
    theta1 = state[1]
    theta2 = state[2]

    point1 = l*sin(theta1)*deltal+0.5, l*cos(theta1)*deltal+0.5
    point2 = l*sin(theta2)*deltal+point1[0], l*cos(theta2)*deltal+point1[1]

    surface = cairo.SVGSurface(None, resolution, resolution)
    cr = cairo.Context(surface)

    cr.scale(resolution, resolution)

    # hintergrund weiss
    cr.rectangle(0, 0, 1, 1)
    cr.set_source_rgb(1, 1, 1)
    cr.fill()

    # spur
    if trace:
        points.append(point2)
        cr.set_line_width(0.002)
        cr.set_source_rgb(120/256, 5/256, 250/256)
        cr.move_to(points[0][0], points[0][1])
        for (x,y) in points:
            cr.line_to(x,y)
        cr.stroke()

    # stangen
    cr.set_source_rgb(0, 0, 0)
    cr.move_to(0.5, 0.5) # aufhaengepunkt
    cr.line_to(point1[0], point1[1])
    cr.line_to(point2[0], point2[1])
    cr.set_line_width(0.007)
    cr.stroke()

    # massenpunkt m1
    cr.set_source_rgb(1, 0, 0)
    cr.arc(point1[0], point1[1], 0.02, 0, 2*pi)
    cr.fill()
    cr.stroke()

    # massenpunkt m2
    cr.set_source_rgb(0, 1, 0)
    cr.arc(point2[0], point2[1], 0.02, 0, 2*pi)
    cr.fill()
    cr.stroke()
        
    outfile = outdir + "/%04d" % i
    surface.write_to_png(outfile + '.png')

    i += 1
    if not options.silent and i % modulo == 0:
        print("%.2f%%" % (i/len(states)*100))


ffmpeg_cmd = "avconv -y -r %.2f -i " % fps + outdir + r"/%04d.png " + output
print(ffmpeg_cmd)
os.system(ffmpeg_cmd)
os.system("rm -rf %s" % outdir)
