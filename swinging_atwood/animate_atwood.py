import matplotlib.pyplot as plt
import matplotlib
from matplotlib import animation
from matplotlib.animation import FuncAnimation
import numpy as np
from numpy import pi, cos, sin
from random import random as rand
import scipy
from scipy.integrate import odeint, solve_ivp

g = 9.807
m = 1
M = 3
L = 1.5 # length of rope
d = 1 # distance between pulleys

def derivatives(t,y):
    # Expected input: y = [r, r', o, o']
    r = y[0:2]
    o = y[2:4]
    r_derivs = [r[1], (m*r[0]*o[1]**2 + g*(m*cos(o[0])-M))/(m+M)] # r' and r''
    o_derivs = [o[1], (-g*sin(o[0]) - 2*r[1]*o[1])/r[0]] # o' and o''
    dydt =  np.array(r_derivs + o_derivs) # concat derivs and return array
    return dydt

def animate(i):
    lim = 100 # set how amny prevous points will be included in the motion
    ax.clear()
    ax.set(xlim = (-2,2), ylim = (-2,2))
    # Plot the motion of the "main mass"
    if i <= lim:
        ax.plot(x[:i],y[:i])
    else:
        ax.plot(x[i-lim:i],y[i-lim:i])
    ax.plot([0,x[i-1]],[0,y[i-1]],lw=1,c='blue')
    ax.plot(x[i-1],y[i-1],c='blue',marker='o',markersize=3*m)
    # plot the motion of the other mass
    ax.plot(x2[i-1],y2[i-1], marker='o', c='blue',markersize=3*M)
    ax.plot([-1,x2[i-1]],[0,y2[i-1]],lw=1,c='blue')
    # Plot pulleys and connecting rope
    ax.plot(0,0, marker='o',c='black')
    ax.plot(-1,0, marker='o',c='black')
    ax.plot([-1,0],[0,0], c='blue',lw=1)

y0 = np.array([1, 0, pi/6, 0]) # initial conditions (r, r', o, o')
t_range = np.linspace(0,10,num=1001)
plot_range = range(len(t_range))

sol = solve_ivp(derivatives, [t_range[0],t_range[-1]], y0, method='Radau', t_eval=t_range)

rs = sol.y[0]
os = sol.y[2]
os = os - pi/2 # rotate cw by 90 deg so it's facing "down"
rs2 = L - rs
os2 = -pi/2*np.ones(np.shape(rs2))

# convert polar to x and y for ease of plotting
x = rs*cos(os)
y = rs*sin(os)
x2 = rs2*cos(os2) - 1 # subtract the distance between points
y2 = rs2*sin(os2)


fig, ax = plt.subplots(figsize =(6,6))
ax.set(xlim = (-2,2), ylim = (-2,2))




anim = FuncAnimation(fig, animate, interval=10, frames=len(t_range)-1)

plt.draw()
plt.show()

# Save output to gif (doesn't work well)
#f = r"atwood.gif"
#writergif = animation.PillowWriter(fps=60)
#anim.save(f, writer=writergif)
