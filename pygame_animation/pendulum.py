import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from numpy import pi, cos, sin
from random import random as rand
import scipy
from scipy.integrate import odeint, solve_ivp

g = 9.807
m1 = 1
m2 = 3
l1 = 1 # length of rope 1
l2 = 1 # length of rope 2

def derivatives(t,y):
    # Expected input: y = [o1, o1', o2, o2']
    o1 = y[0:2]
    o2 = y[2:4]
    # Equation I solved has o1'' and o2'' mixed. Easiest to solve with
    # linear algebra instead of isolating for each o''
    A = np.array([[(m1+m2)*l1, m2*l2*cos(o1[0]-o2[0])],
        [l1*cos(o1[0]+o2[0]), l2]])
    b = np.array([[-(m1+m2)*g*sin(o1[0]) - m2*l2*o2[1]**2*sin(o1[0]-o2[0])],
        [l1*o1[1]**2*sin(o1[0]-o2[0])-g*sin(o2[0])]])
    second_derivs = np.linalg.solve(A,b)
    o1_derivs = [o1[1],second_derivs[0][0]]
    o2_derivs = [o2[1],second_derivs[1][0]]
    dydt = np.array(o1_derivs + o2_derivs)
    return dydt

def animate(i):
    lim = 100 # set how amny prevous points will be included in the motion
    ax.clear()
    ax.set(xlim = (-2,2), ylim = (-2,2))
    # Plot the motion of m2 (outer mass)
    if i <= lim:
        ax.plot(x2[:i],y2[:i])
    else:
        ax.plot(x2[i-lim:i],y2[i-lim:i])
    ax.plot([x[i-1],x2[i-1]],[y[i-1],y2[i-1]],lw=1,c='blue')
    ax.plot(x2[i-1],y2[i-1],c='blue',marker='o',markersize=3*m2)
    # plot the motion of m1 (inner mass)
    ax.plot(x[i-1],y[i-1], marker='o', c='blue',markersize=3*m1)
    ax.plot([0,x[i-1]],[0,y[i-1]],lw=1,c='blue')
    # Plot the origin
    ax.plot(0,0, marker='o',c='black')

y0 = np.array([pi/2, 0, pi/6, 0]) # initial conditions (o1, o1', o2, o2')
t_range = np.linspace(0,10,num=1000)
plot_range = range(len(t_range))

sol = solve_ivp(derivatives, [t_range[0],t_range[-1]], y0, method='Radau', t_eval=t_range)
o1s = sol.y[0] - pi/2 # rotate CW by 90 deg so it's facing "down"
o2s = sol.y[2] - pi/2 # rotate CW by 90 deg so it's facing "down"
# convert polar to x and y for ease of plotting
x = l1*cos(o1s)
y = l1*sin(o1s)
x2 = l2*cos(o2s) + x # pendulum 2 starts from coordinates of pendulum 1
y2 = l2*sin(o2s) + y # pendulum 2 starts from coordinates of pendulum 1
