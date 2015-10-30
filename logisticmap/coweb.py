from pyx import *

alpha = 2.8
x0 = 0.2

f = lambda x: alpha*x*(1-x)

g = graph.graphxy(
    width = 8,
    x     = graph.axis.lin(title=r"$x_n$", min=0, max=1),
    y     = graph.axis.lin(title=r"$x_{n+1}$", min=0, max=1)
)

g.plot(graph.data.function("y(x)=%g*x*(1-x)" % alpha, min=0, max=1, points=100))
g.plot(graph.data.function("y(x)=x", min=0, max=1), [graph.style.line([style.linestyle.dashed])])
g.text(0.3,4.4, r"$\alpha=%.2f$" % alpha)

attrs = [color.rgb.red, deco.earrow(size=0.1)]

x0,y0 = 0.2,0
for j in range(10):
    fx0 = f(x0)
    x1,y1 = g.pos(x0, y0)
    x2,y2 = g.pos(x0, fx0)
    x3,y3 = g.pos(fx0, fx0)

    g.stroke(path.line(x1, y1, x2, y2), attrs)
    g.stroke(path.line(x2, y2, x3, y3), attrs)

    x0,y0 = fx0, fx0


g.writePDFfile()
