from pyx import *
from numpy import linspace
from math import *

c = canvas.canvas()
c.stroke(path.line(1, 0, 5.2, 0), [style.linewidth.THICK])

for x in linspace(1.2, 4.6, 12):
    c.stroke(path.line(x, 0, x+0.5, 0.5))


l = 3
ldashed = 1.7
radius = 0.2
theta1 = 0.4
xoffset = 0.2
yoffset = +0.2

x0 = 3
y0 = 0
x1 = 3 + l*sin(theta1)
y1 = -l*cos(theta1)

c.stroke(path.line(x0, y0, x1, y1), [style.linewidth.thick])
c.text((x0+x1)/2+0.1, (y0+y1)/2, r"$l$")

c.stroke(path.line(x0, y0, x0, y0-ldashed), [style.linestyle.dashed])


c.fill(path.circle(x1, y1, radius), [color.cmyk.NavyBlue])
c.text(x1+xoffset, y1+yoffset, r"$m$")

ldashed2 = 1.5
c.stroke( path.path(path.arc(x0,y0,ldashed2,-90, -90+degrees(theta1))), [style.linewidth.thin, deco.earrow.small, deco.barrow.small] )

c.text((x0+x1)/2-0.4, y0-ldashed+0.4, r"$\varphi$")
#c.stroke(path.line((x0+x1)/2-0.5, y0-ldashed+0.55, (x0+x1)/2-0.1, y0-ldashed+0.3), [style.linewidth.thin])

c.writePDFfile()
