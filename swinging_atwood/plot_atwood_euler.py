import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from numpy import pi, cos, sin
from random import random as rand
import scipy
from scipy.integrate import odeint, solve_ivp

g = 9.807
m = 1
M = 7
L = 1 # length of rope


def euler_solve(f, t, y0):
    dt = t[1]-t[0]
    y = np.zeros([len(t),len(y0)])
    y[0] = y0

    for n in range(len(t)-1):
        y[n+1] = y[n] + f(t[n],y[n])*dt
    return y


def derivatives(t,y):
    # y = [r, r', o, o']
    r = y[0:2]
    o = y[2:4]
    r_derivs = [r[1], (m*r[0]*o[1]**2 + g*(m*cos(o[0])-M))/(m+M)] # r' and r''
    o_derivs = [o[1], (-g*sin(o[0]) - 2*r[1]*o[1])/r[0]] # o' and o''
    dydt =  np.array(r_derivs + o_derivs) # concat derivs and return array
    return dydt



# Get ready for Euler solves
y0 = np.array([1, 0, pi/6, 0]) # initial conditions
dt = .001
t_range = np.arange(0,10,dt)

y = newton_solve(derivatives, t_range, y0)


rs = y.T[0]
os = y.T[2]
rs2 = L - rs
os2 = -pi/2*np.ones(np.shape(rs2))
os = os - pi/2 # rotate cw by 90 degrees to face things "down"
plt.polar(os, rs,'g',os2,rs2,'r')
plt.show()
