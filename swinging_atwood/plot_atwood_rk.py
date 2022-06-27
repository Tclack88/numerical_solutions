import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from numpy import pi, cos, sin
from random import random as rand
import scipy
from scipy.integrate import odeint, solve_ivp

#
# plt.gca().axes.get_xaxis().set_visible(False)
# plt.axis('off')
# #plt.axes(projection = 'polar')
# r = 3
# o = pi/2
# plt.polar(o,0,'g.',o,r,'g.')
# plt.show()

g = 9.807
m = 1
M = 7
L = 1 # length of rope

def runga_kutta2_solve(f, t, y0):
    dt = t[1]-t[0]
    y = np.zeros([len(t),len(y0)])
    y[0] = y0

    for n in range(len(t)-1):
        k1 = f(t[n], y[n])
        k2 = f(t[n] + dt, y[n] + dt*k1)
        y[n+1] = y[n] + (k1/2 + k2/2)*dt

    return y


def runga_kutta3_solve(f, t, y0):
    dt = t[1]-t[0]
    y = np.zeros([len(t),len(y0)])
    y[0] = y0

    for n in range(len(t)-1):
        k1 = f(t[n], y[n])
        k2 = f(t[n] + dt/2, y[n] + dt*k1/2)
        k3 = f(t[n] + dt, y[n] + dt*k2)
        y[n+1] = y[n] + (k1 + 4*k2 + k3)*dt/6

    return y


def runga_kutta4_solve(f, t, y0):
    dt = t[1]-t[0]
    y = np.zeros([len(t),len(y0)])
    y[0] = y0

    for n in range(len(t)-1):
        k1 = f(t[n], y[n])
        k2 = f(t[n] + dt/2, y[n] + dt*k1/2)
        k3 = f(t[n] + dt/2, y[n] + dt*k2/2)
        k4 = f(t[n] + dt, y[n] + k3*dt)
        y[n+1] = y[n] + (k1 + 2*k2 + 2*k3 + k4)*dt/6

    return y

def derivatives(t,y):
    # y = [r, r', o, o']
    r = y[0:2]
    o = y[2:4]
    r_derivs = [r[1], (m*r[0]*o[1]**2 + g*(m*cos(o[0])-M))/(m+M)] # r' and r''
    o_derivs = [o[1], (-g*sin(o[0]) - 2*r[1]*o[1])/r[0]] # o' and o''
    dydt =  np.array(r_derivs + o_derivs) # concat derivs and return array
    return dydt



# Get ready for Runga Kutta 2 solve
y0 = np.array([1, 0, pi/6, 0]) # initial conditions
dt = .01
t_range = np.arange(0,10,dt)

y = runga_kutta4_solve(derivatives, t_range, y0)


rs = y.T[0]
os = y.T[2]
rs2 = L - rs
os2 = -pi/2*np.ones(np.shape(rs2))
os = os - pi/2 # rotate cw by 90 degrees to face things "down"
plt.polar(os, rs,'g',os2,rs2,'r')
plt.show()
