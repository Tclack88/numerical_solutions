import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation
from methods import runga_kutta2, runga_kutta3 ,runga_kutta4, euler
import numpy as np
from numpy import pi, cos, sin
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
        ax.plot(x[i-1],y[i-1],c=colors[j],marker='o',markersize=3*m)
        # plot the motion of the other mass
        ax.plot(x2[i-1],y2[i-1], marker='o', c=colors[j],markersize=3*M)
        ax.plot([-1,x2[i-1]],[0,y2[i-1]],lw=1,c=colors[j],)
        # Plot pulleys and connecting rope
        ax.plot(0,0, marker='o',c='black')
        ax.plot(-1,0, marker='o',c='black')
        ax.plot([-1,0],[0,0], c=colors[j],lw=1)
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
    y = solver(derivatives, t_range, y0)

    rs = y.T[0]
    os = y.T[2]
    os = os - pi/2 # rotate cw by 90 deg so it's facing "down"
    rs2 = L - rs
    os2 = -pi/2*np.ones(np.shape(rs2))
    # convert polar to x and y for ease of plotting
    x = rs*cos(os)
    y = rs*sin(os)
    x2 = rs2*cos(os2) - 1 # subtract the distance between points
    y2 = rs2*sin(os2)
    solutions.append(np.array([x,y,x2,y2]))


#sol_array = np.array(solutions)
#print(np.shape(sol_array[1]))



#sol = solve_ivp(derivatives, [t_range[0],t_range[-1]], y0, method='Radau', t_eval=t_range)



fig, ax = plt.subplots(figsize =(6,6))
ax.set(xlim = (-2,2), ylim = (-2,2))




anim = FuncAnimation(fig, animate, interval=10, frames=len(t_range)-1)

plt.draw()
plt.show()

# Save output to gif (doesn't work well)
#f = r"atwood.gif"
#writergif = animation.PillowWriter(fps=60)
#anim.save(f, writer=writergif)
