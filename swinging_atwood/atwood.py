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

global m
global M
global g
g = 9.807
m = 1
M = 7
L = 1 # length of rope
d = 1 # distance between pulleys

def derivatives(t,y):
    # y = [r, r', o, o']
    r = y[0:2]
    o = y[2:4]
    r_derivs = [r[1], (m*r[0]*o[1]**2 + g*(m*cos(o[0])-M))/(m+M)] # r' and r''
    o_derivs = [o[1], (-g*sin(o[0]) - 2*r[1]*o[1])/r[0]] # o' and o''
    dydt =  np.array(r_derivs + o_derivs) # concat derivs and return array
    return dydt

#x0 = [1, pi/3] # initial conditions. Radius, angle
y0 = np.array([1, 0, pi/6, 0]) # initial conditions
t_range = np.linspace(0,10,num=1001)

sol = solve_ivp(derivatives, [t_range[0],t_range[-1]], y0, method='Radau', t_eval=t_range)

#plt.plot(t_range,sol.y[1])
#plt.polar(o,0,'g.',o,r,'g.')
rs = sol.y[0]
os = sol.y[2]
rs2 = L - rs
os2 = -pi/2*np.ones(np.shape(rs2))

os = os - pi/2
plt.polar(os, rs,'g',os2,rs2,'r')
plt.show()

