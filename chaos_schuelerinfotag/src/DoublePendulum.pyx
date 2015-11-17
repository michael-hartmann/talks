#!python
#cython: language_level=3, cdivision=True
# -*- coding: utf-8 -*-

from math import sin,cos,acos,sqrt
cimport libc.math
from libc.math cimport sin as csin
from libc.math cimport cos as ccos
from libc.math cimport sqrt as csqrt

cdef void rk4(double y[4], double omega, double h, int steps):
    cdef int i,j
    cdef double k1[4]
    cdef double k2[4]
    cdef double k3[4]
    cdef double k4[4]
    cdef double temp[4]

    for j in range(steps):
        # k1
        f(k1,y,omega)

        for i in range(4):
            temp[i] = y[i]+h/2*k1[i]

        # k2
        f(k2,temp,omega)

        for i in range(4):
            temp[i] = y[i]+h/2*k2[i]

        # k3
        f(k3,temp,omega)

        for i in range(4):
            temp[i] = y[i]+h*k3[i]

        f(k4,temp,omega)

        for i in range(4):
            y[i] += h/6*( k1[i] + 2*k2[i] + 2*k3[i] + k4[i] )


cdef void f(double dy[4], double y[4], double omega):
    """
    calculates derivative vector d/dt (Θ1, Θ2, p1, p2)
    """
    cdef double num1, num2, denom, delta

    cdef double theta1  = y[0]
    cdef double theta2  = y[1]
    cdef double dtheta1 = y[2]
    cdef double dtheta2 = y[3]

    dy[0] = dtheta1
    dy[1] = dtheta2

    Delta = theta1-theta2
    denom = 3-ccos(2*Delta)
    num1  = -omega*(3*csin(theta1)+csin(theta1-2*theta2)) - 2*csin(Delta)*(dtheta2**2+dtheta1**2*ccos(Delta))
    num2  = 2*csin(Delta)*(2*dtheta1**2+2*omega*ccos(theta1)+dtheta2**2*ccos(Delta))

    dy[2] = num1/denom
    dy[3] = num2/denom


def arcsimp(double x):
    """
    Gibt fuer x einen äquivalenten Winkel im Bereich [-π,π]
    """
    cdef double pi  = 3.141592653589793
    cdef double tau = 2*pi
    x = x % tau
    if x > pi:
        x = x-tau

    return x


def interpolate(double x1, double y1, double x2, double y2):
    """
    Steigung und y-Achsenabschnitt fuer Gerade zwischen zwei Punkten berechnen 
    """
    cdef double m, t

    m = (y2-y1)/(x2-x1)
    t = y1-m*x1

    return m,t



cdef class DoublePendulum:
    cdef readonly double l,m,g,omega
    def __init__(self, double l=1, double m=1, double g=9.81):
        """
        create new DoublePendulum object.
        m: mass of bobs
        l: length of pendulums
        g: earth acceleration
        """
        self.l     = l
        self.m     = m
        self.g     = g
        self.omega = g/l


    def E(self, double theta1, double theta2, double dtheta1, double dtheta2):
        """
        returns energy E(Θ1, Θ2, p1, p2)
        """
        cdef double m, l, g, T, V

        m = self.m
        l = self.l
        g = self.g

        # kinetische energie
        T = m*l**2*(dtheta1**2 + 0.5*dtheta2**2 + dtheta1*dtheta2*ccos(theta1-theta2))
        # potentielle energie
        V = m*g*l*(3-2*ccos(theta1)-ccos(theta2))

        return T+V


    def dtheta2(self, double E, double theta1, double dtheta1):
        cdef double ml2   = self.m*self.l**2
        cdef double omega = self.omega
        cdef double a,b,c

        a = 0.5
        b = dtheta1*ccos(theta1)
        c = dtheta1**2+2*omega*(1-ccos(theta1))-E/(ml2)

        return (-b+csqrt(b**2-4*a*c))/(2*a)


    def theta1_max(self, E):
        max = acos(1-E/(2*self.m*self.g*self.l))
        return -max,max


    def dtheta1_max(self, E):
        ml2 = self.m*self.l**2
        return -sqrt(2*E/ml2), sqrt(E/ml2)


    def integrate(self, y0, int N, int skip=10, double h=1e-3):
        cdef int i
        cdef double omega = self.omega
        cdef double y[4]
        y[0] = y0[0]
        y[1] = y0[1]
        y[2] = y0[2]
        y[3] = y0[3]

        out = [(0,y[0],y[1],y[2],y[3])]
        for i in range(N):
            rk4(y, omega, h, skip)
            out.append((h*skip*(i+1),y[0], y[1], y[2], y[3]))
 
        return out

 
    def poincare(self, double E, double theta1_0, double dtheta1_0, int N, double h=2e-3):
        """
        Punkte auf dem Poincare-Plot fuer Θ1,p1 berechnen.
        Energie=E, integriert wird bis zur Zeit T
        """
        cdef int i,n
        cdef double omega = self.omega
        cdef double m,t
        cdef double y[4]
        cdef double ylast[4]
        y[0] = theta1_0
        y[1] = 0
        y[2] = dtheta1_0
        y[3] = self.dtheta2(E,theta1_0,dtheta1_0)

        points = []
        while True:
            for i in range(4):
                ylast[i] = y[i]

            rk4(y, omega, h, 1)
            y[1] = arcsimp(y[1])

            if ylast[1] < 0 and y[1] > 0:
                m,t = interpolate(0, ylast[1], h, y[1])

                rk4(ylast, omega, -t/m, 1)
                points.append((arcsimp(ylast[0]),ylast[2]))

                if len(points) >= N:
                    break

                y[0] = ylast[0]
                y[1] = 0
                y[2] = ylast[2]
                y[3] = ylast[3]

        return points
