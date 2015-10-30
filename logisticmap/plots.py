from pyx import *

def f(alpha,x):
    return alpha*x*(1-x)

x0 = 0.3
N = 30
d1 = [x0] # 0.5
d2 = [x0] # 1.5
d3 = [x0] # 2.5
d4 = [x0] # 3.1 
d5 = [x0] # 4

for i in range(N):
    d1.append(f(0.5, d1[-1]))
    d2.append(f(1.5, d2[-1]))
    d3.append(f(2.5, d3[-1]))
    d4.append(f(3.1, d4[-1]))

for i in range(3*N):
    d5.append(f(4, d5[-1]))


i = 1
for alpha,d in ((0.5,d1),(1.5,d2),(2.5,d3),(3.1,d4),(4,d5)):
    g = graph.graphxy(
        key   = graph.key.key(pos="br", dist=0.1),
        width = 8,
        x     = graph.axis.lin(title=r"$n$"),
        y     = graph.axis.lin(title=r"$x_n$")
    )

    if alpha != 4:
        xaxis = range(N+1)
    else:
        xaxis = range(3*N+1)
    g.plot([
        graph.data.values(x=xaxis, y=d, title=r"$\alpha=%g$" % alpha),
        ],
        [graph.style.symbol(graph.style.symbol.changecircle, size=0.1, symbolattrs=[color.gradient.RedBlue]), graph.style.line()]
    )

    g.writePDFfile("plot%d" % i)
    i+=1
