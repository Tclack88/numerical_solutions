from systems import Atwood
import numpy as np
from random import random as rand
from numpy import pi, sin, cos
import pygame
from pygame.locals import *
from utils import Mass, Pulley, Controller, Slider, Checkbox

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
        self.state = np.array([50,0,rand()*pi/2,0]) # initial conditions

    def object_init(self):
        c1 = (255,100,100)
        c2 = (0,255,0)

        self.pulleys = [Pulley(self.center),
                Pulley(np.array([self.WIDTH/3,self.HEIGHT/2]))]
        # initiate masses (positions don't matter, they get handled
        # immediately in the "recalculate" method, but mass is needed
        self.masses = [Mass((400,400), 1, c1),
                Mass((self.WIDTH/3,self.HEIGHT/2+100), 3, c2)]
        self.controller = Controller(self.screen)
        # get controller dimenstions to place sliders
        c_width, c_height = self.controller.w, self.controller.h
        num_sliders = 3
        h_dist = c_width/(num_sliders+1)
        v_dist = c_height/4
        self.sliders = [Slider((h_dist,v_dist), 1, h_dist/10, v_dist*2, c1),
                Slider((2*h_dist,v_dist), 3, h_dist/10, v_dist*2, c2)]
        # set checkboxes
        self.checkboxes=[Checkbox(self.screen,h_dist*3,v_dist,'true',caption='"True" solution',checked=True),
                Checkbox(self.screen,h_dist*3,1.5*v_dist,'euler',caption='euler'),
                Checkbox(self.screen,h_dist*3,2*v_dist,'rk2',caption='rk2'),
                Checkbox(self.screen,h_dist*3,2.5*v_dist,'rk3',caption='rk3'),
                Checkbox(self.screen,h_dist*3,3*v_dist,'rk4',caption='rk4')]
        self.solution = 'true'

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
        state = self.state
        name = self.solution # set by checkboxes (euler, rk2, etc)
        [x,y,x2,y2],self.last_vals = atwood.solve(state,name)
        self.x, self.y, self.x2, self.y2 = x,y,x2,y2
        self.index = 0

    def on_loop(self):
        while self.running:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                #for slider in self.sliders:
                #    slider.handle_event(self.screen)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for box in self.checkboxes:
                        box.update_checkbox(event)
                        if box.checked is True:
                            self.solution = box.id
                            for b in self.checkboxes:
                                if b != box:
                                    b.checked = False

                if event.type == pygame.QUIT:
                    self.running = False
            # update
            i = self.index
            x = self.x[i]
            y = self.y[i]
            x2 = self.x2[i]
            y2 = self.y2[i]

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
            if self.index == len(self.x): # end of index reached
                self.state = self.last_vals
                self.recalculate(self.state)

            # add controller on top of everything
            self.controller.render(self.screen)
            for i,slider in enumerate(self.sliders):
                slider.render(self.screen)
                slider.changeValue()
                self.masses[i].update(mass=slider.getValue())

            for checkbox in self.checkboxes:
                checkbox.render()


        pygame.quit()

    def execute(self):
        self.on_init()
        self.object_init()
        self.on_loop()

if __name__ == "__main__":
    simulation = Simulation()
    simulation.execute()
