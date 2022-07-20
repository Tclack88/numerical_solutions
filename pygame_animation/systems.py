import numpy as np
from numpy import pi, cos, sin
from scipy.integrate import solve_ivp
from methods import runga_kutta2, runga_kutta3, runga_kutta4, euler
# g = 9.807
# m = 1
# M = 3
# L = 1.5 # length of rope
# d = 1 # distance between pulleys
names = ('rk2','rk3','rk4','euler')
sol_functions = (runga_kutta2, runga_kutta3, runga_kutta4, euler)
sol_methods = dict(zip(names,sol_functions))


class Atwood:
    def __init__(self, g, L, m, M, d):
        self.g = g
        self.L = L
        self.m = m # mass1
        self.M = M # mass2
        self.d = d # distance between pulleys


    def derivatives(self,t,y):
        """Expected input:
        y = [r, r', o, o']
        t = np array, list of times
        Not used explicitly required for solve_ivp
        """
        g = self.g
        m = self.m
        M = self.M

        r = y[0:2]
        o = y[2:4]
        r_derivs = [r[1], (m*r[0]*o[1]**2 + g*(m*cos(o[0])-M))/(m+M)] # r', r''
        o_derivs = [o[1], (-g*sin(o[0]) - 2*r[1]*o[1])/r[0]] # o',  o''
        dydt =  np.array(r_derivs + o_derivs) # concat derivs and return array
        return dydt

    
    def solve(self, y0, method_name):
        """ y0 : list of floats/ints representing [r,r',o,o']"""
        g = self.g
        m = self.m
        M = self.M
        L = self.L
        d = self.d
        #y0 = np.array([1, 0, pi/6, 0]) # initial conditions (r, r', o, o')
        t_range = np.linspace(0,10,num=1001)
        

        if method_name == 'true':
            sol = solve_ivp(self.derivatives, [t_range[0],t_range[-1]], y0, method='Radau', t_eval=t_range)
            rs = sol.y[0]
            os = sol.y[2]
        else:
            sol_method = sol_methods[method_name]
            sol = sol_method(self.derivatives, t_range, y0)
            rs = sol.T[0]
            os = sol.T[2]

        os = os - pi/2 # rotate cw by 90 deg so it's facing "down"
        rs2 = L - rs
        os2 = -pi/2*np.ones(np.shape(rs2))
        
        # convert polar to x and y for ease of plotting
        x = rs*cos(os)
        y = rs*sin(os)*-1
        x2 = rs2*cos(os2) # subtract the distance between points
        y2 = rs2*sin(os2)*-1

        # approximate r, r', o, o' to be used for the next set of calculations
        dt = t_range[-1] - t_range[-2]
        dr = (rs[-1] - rs[-2])/dt
        do = (os[-1] - os[-2])/dt
        last_vals = [rs[-1], dr, os[-1]+pi/2, do] # need to rotate last o back
        return [x,y,x2,y2], last_vals


class DoublePendulum:
    def __init__(self, g, l1, l2, m1, m2):
        self.g = g
        self.l1 = l1
        self.l2 = l2
        self.m1 = m1 # mass1
        self.m2 = m2 # mass2

    def derivatives(self,t,y):
        # Expected input: y = [o1, o1', o2, o2']
        g = self.g
        l1 = self.l1
        l2 = self.l2
        m1 = self.m1 # mass1
        m2 = self.m2  # mass2

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

    def solve(self, y0, method_name):
        """ y0 : list of floats/ints representing [o1, o1', o2, o2']"""
        g = self.g
        l1 = self.l1
        l2 = self.l2
        m1 = self.m1 # mass1
        m2 = self.m2  # mass2
        t_range = np.linspace(0,10,num=1001)

        if method_name == 'true':
            sol = solve_ivp(self.derivatives, [t_range[0],t_range[-1]], y0, method='Radau', t_eval=t_range)
            o1s = sol.y[0] - pi/2 # rotate CW by 90 deg so it's facing "down"
            o2s = sol.y[2] - pi/2 # rotate CW by 90 deg so it's facing "down"
        else:
            sol_method = sol_methods[method_name]
            sol = sol_method(self.derivatives, t_range, y0)

            o1s = sol.T[0] - pi/2 # rotate CW by 90 deg so it's facing "down"
            o2s = sol.T[2] - pi/2 # rotate CW by 90 deg so it's facing "down"
        # convert polar to x and y for ease of plotting
        x = l1*cos(o1s)
        y = l1*sin(o1s)*-1
        x2 = l2*cos(o2s) # pendulum 2 starts from coordinates of pendulum 1
        y2 = (l2*sin(o2s))*-1 # pendulum 2 starts from coordinates of pendulum 1


        # approximate o1, o1', o2, o2' to be used for the next set of calculations
        dt = t_range[-1] - t_range[-2]
        do1 = (o1s[-1] - o1s[-2])/dt
        do2 = (o2s[-1] - o2s[-2])/dt
        last_vals = [o1s[-1]+pi/2, do1, o2s[-1]+pi/2, do2] # need to rotate last o's back
        return [x,y,x2,y2], last_vals
