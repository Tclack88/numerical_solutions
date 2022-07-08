from atwood import Atwood
import numpy as np
from numpy import pi, sin, cos
import pygame
from pygame.locals import *

class Mass:
    def __init__(self, location, mass):
        """Ball/mass for the weights,
        location is last known or initial location, tuple (x,y) coordinates
        mass: float or in.
        """
        self.location = location
        self.mass = mass
        self.radius = 4*mass**.5 # Radius proportional to mass for effect

    def __repr__(self):
        return f"""Mass:{self.mass}kg located at {self.location}"""
        
    def render(self, screen):
        pygame.draw.circle(screen, (0,250,0), self.location, self.radius)

    def update(self, location=None, mass=None):
        if location != None:
            self.location = location
        if mass != None:
            self.mass = mass

class Pulley:
    def __init__(self, location):
        """Pulley drawn for visual appeal, no purpose
        location (tuple) fixed
        """
        self.location = location
        self.radius = 2
        
    def render(self, screen):
        pygame.draw.circle(screen, (200,200,200), self.location, self.radius)



class Simulation:
    def __init__(self):
        self.running = True
        self.size = self.WIDTH, self.HEIGHT = 500,500
        self.screen = pygame.display.set_mode(self.size)
        self.center = np.array([self.WIDTH/2, self.HEIGHT/2])

    def on_init(self):
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.FPS = 500
        #self.RECALCULATE = pygame.USEREVENT + 1
        #pygame.time.set_timer(self.RECALCULATE,3000)
        self.state = np.array([50,0,pi/6,0]) # initial conditions

    def object_init(self):

        self.pulleys = [Pulley(self.center),
                Pulley(np.array([self.WIDTH/3,self.HEIGHT/2]))]
        # initiate masses (positions don't matter, they get handled
        # immediately in the "recalculate" method, but mass is needed
        self.masses = [Mass((400,400), 1),
                Mass((self.WIDTH/3,self.HEIGHT/2+100), 3)]
        # Initialize parameters (make editable later)
        self.L = 150
        self.g = 9.807
        self.d = np.linalg.norm(np.array(self.pulleys[0].location) - np.array(self.pulleys[1].location))
        self.recalculate(self.state) # intantiate atwood state

    def recalculate(self, y0):
        """
        y0: [r, r', o, o']
        """
        m, M = self.masses[0].mass, self.masses[1].mass
        L = self.L
        g = self.g
        d = self.d
        atwood = Atwood(g, L, m, M, d)
        [x,y,x2,y2] = atwood.solve(self.state)
        self.x, self.y, self.x2, self.y2 = x,y,x2,y2
        self.index = 0

    def on_loop(self):
        while self.running:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                #if event.type == self.RECALCULATE:
                #    print("recalculating")
                #    self.recalculate(self.state) # intantiate atwood state
                    
                if event.type == pygame.QUIT:
                    self.running = False
            # update
            i = self.index
            x = self.x[i]
            y = self.y[i]
            x2 = self.x2[i]
            y2 = self.y2[i]
            self.state = [x,y,x2,y2]

            # TODO implement mass update
            (newx,newy) = np.array(self.pulleys[0].location) + np.array((x,y))
            (newx2,newy2) = np.array(self.pulleys[1].location) + np.array((x2,y2))
            self.masses[0].update((newx,newy))
            self.masses[1].update((newx2,newy2))
            pygame.display.update()
            # draw / render
            self.screen.fill((0,0,0))
            for mass in self.masses:
                mass.render(self.screen)
            for pulley in self.pulleys:
                pulley.render(self.screen)

            # draw line connecting masses and pulleys
            points = [self.masses[1].location,
                    self.pulleys[1].location,
                    self.pulleys[0].location,
                    self.masses[0].location]
            pygame.draw.lines(self.screen, (200,200,200), False, points)

            self.index += 1
            if self.index == 1000:
                state = [self.x[-1], self.y[-1], self.x2[-1],self.y2[-1]]
                self.recalculate(state)

        pygame.quit()

    def execute(self):
        self.on_init()
        self.object_init()
        self.on_loop()

if __name__ == "__main__":
    simulation = Simulation()
    simulation.execute()
