import numpy as np

def runga_kutta2(f, t, y0):
    dt = t[1]-t[0]
    y = np.zeros([len(t),len(y0)])
    y[0] = y0

    for n in range(len(t)-1):
        k1 = f(t[n], y[n])
        k2 = f(t[n] + dt, y[n] + dt*k1)
        y[n+1] = y[n] + (k1/2 + k2/2)*dt

    return y


def runga_kutta3(f, t, y0):
    dt = t[1]-t[0]
    y = np.zeros([len(t),len(y0)])
    y[0] = y0

    for n in range(len(t)-1):
        k1 = f(t[n], y[n])
        k2 = f(t[n] + dt/2, y[n] + dt*k1/2)
        k3 = f(t[n] + dt, y[n] + dt*k2)
        y[n+1] = y[n] + (k1 + 4*k2 + k3)*dt/6

    return y


def runga_kutta4(f, t, y0):
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


def euler(f, t, y0):
    dt = t[1]-t[0]
    y = np.zeros([len(t),len(y0)])
    y[0] = y0

    for n in range(len(t)-1):
        y[n+1] = y[n] + f(t[n],y[n])*dt
    return y
