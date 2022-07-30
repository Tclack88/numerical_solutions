import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation
from methods import runga_kutta2, runga_kutta3 ,runga_kutta4, euler
import numpy as np
from numpy import pi, cos, sin
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
    for j,solver in enumerate(solvers):
        solution = solutions[j]
        x = solution[0]
        y = solution[1]
        x2 = solution[2]
        y2 = solution[3]
        # Plot the motion of the "main mass"
        if i <= lim:
            ax.plot(x[:i],y[:i])
        else:
            ax.plot(x[i-lim:i],y[i-lim:i])
        ax.plot([0,x[i-1]],[0,y[i-1]],lw=1,c=colors[j])
        ax.plot(x[i-1],y[i-1],c=colors[j],marker='o',markersize=3*m1)
        # plot the motion of the other mass
        ax.plot(x2[i-1],y2[i-1], marker='o', c=colors[j],markersize=3*m2)
        # Plot pulley and connecting rope
        ax.plot(0,0, marker='o',c='black')
        ax.plot([x[i-1],x2[i-1]],[y[i-1],y2[i-1]],lw=1,c=colors[j],)
    ax.legend(legend)

y0 = np.array([1, 0, pi/6, 0]) # initial conditions (r, r', o, o')
t_range = np.linspace(0,10,num=1000)
plot_range = range(len(t_range))

solvers = [euler, runga_kutta2, runga_kutta3 ,runga_kutta4]
legend = [' '.join(str(s).split()[1:-2]) for s in solvers]
#colors = ['blue', 'red', 'yellow', 'green']
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

solutions = []
for solver in solvers:
    sol = solver(derivatives, t_range, y0)

    o1s = sol.T[0] - pi/2 # rotate CW by 90 deg so it's facing "down"
    o2s = sol.T[2] - pi/2 # rotate CW by 90 deg so it's facing "down"
    # convert polar to x and y for ease of plotting
    x = l1*cos(o1s)
    y = l1*sin(o1s)
    x2 = l2*cos(o2s) + x # pendulum 2 starts from coordinates of pendulum 1
    y2 = l2*sin(o2s) + y # pendulum 2 starts from coordinates of pendulum 1
    solutions.append(np.array([x,y,x2,y2]))

fig, ax = plt.subplots(figsize =(6,6))
ax.set(xlim = (-2,2), ylim = (-2,2))

anim = FuncAnimation(fig, animate, interval=10, frames=len(t_range)-1)
plt.draw()
plt.show()
