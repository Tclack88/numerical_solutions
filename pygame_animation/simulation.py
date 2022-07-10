from atwood import Atwood
import numpy as np
from random import random as rand
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


class Controller(pygame.Rect):
    def __init__(self, screen):
        """contains sliders to change mass, gravity, string length, etc."""
        
        self.w = screen.get_width()
        self.h = screen.get_height()/5

    def render(self, screen):
        pygame.draw.rect(screen, (100,100,100), (0,0,self.w,self.h))

class Slider:
    # Shamelessly stolen from stack overflow
    # https://stackoverflow.com/questions/65482148/creating-sliders-using-pygame
    def __init__(self, position:tuple, upperValue:int=10, w:int = 20, h:int = 80, text:str="")->None:
        self.w = w
        self.h = h
        self.position = position
        self.outlineSize = (self.w,self.h) #outlineSize
        self.text = text
        self.upperValue = upperValue

    #returns the current value of the slider
    def getValue(self)->float:
        return self.h / (self.outlineSize[1] / self.upperValue)

    #renders slider and the text showing the value of the slider
    def render(self, display:pygame.display)->None:
        #draw outline and slider rectangles
        pygame.draw.rect(display, (50, 50, 50),
            (self.position[0], self.position[1], self.outlineSize[0], self.outlineSize[1]), 3)

        pygame.draw.rect(display, (0, 0, 0),
                (self.position[0], self.position[1], self.w , self.h))

        #determine size of font
        self.font = pygame.font.Font(pygame.font.get_default_font(), int(1.5*self.w))

        #create text surface with value
        valueSurf = self.font.render(f"{self.text}{round(self.getValue())}", True, (255, 0, 0))

        #centre text
        textx = self.position[0] + (self.outlineSize[0]/2) - (valueSurf.get_rect().width/2)
        texty = self.position[1] + (self.outlineSize[1]) + .5*(valueSurf.get_rect().height/2)

        display.blit(valueSurf, (textx, texty))

    #allows users to change value of the slider by dragging it.
    def changeValue(self)->None:
        #If mouse is pressed and mouse is inside the slider
        def pointInRectanlge(px, py, rw, rh, rx, ry):
            if px > rx and px < rx  + rw:
                if py > ry and py < ry + rh:
                    return True
            return False
        mousePos = pygame.mouse.get_pos()
        if pointInRectanlge(mousePos[0], mousePos[1], self.outlineSize[0], self.outlineSize[1], self.position[0], self.position[1]):
            if pygame.mouse.get_pressed()[0]:
                #the size of the slider
                self.h = mousePos[1] - self.position[1]

                #limit the size of the slider
                if self.h < 1:
                    self.h = 0
                if self.h > self.outlineSize[1]:
                    self.h = self.outlineSize[1]


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

        self.pulleys = [Pulley(self.center),
                Pulley(np.array([self.WIDTH/3,self.HEIGHT/2]))]
        # initiate masses (positions don't matter, they get handled
        # immediately in the "recalculate" method, but mass is needed
        self.masses = [Mass((400,400), 1),
                Mass((self.WIDTH/3,self.HEIGHT/2+100), 3)]
        self.controller = Controller(self.screen)
        # get controller dimenstions to place sliders
        c_width, c_height = self.controller.w, self.controller.h
        num_sliders = 3
        h_dist = c_width/(num_sliders+1)
        v_dist = c_height/4
        self.sliders = [Slider((h_dist,v_dist),w=h_dist/10,h=v_dist*2)]
        #self.sliders = [Slider((h_dist,v_dist))]
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
        [x,y,x2,y2],self.last_vals = atwood.solve(self.state)
        self.x, self.y, self.x2, self.y2 = x,y,x2,y2
        self.index = 0

    def on_loop(self):
        while self.running:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                #for slider in self.sliders:
                #    slider.handle_event(self.screen)
                if event.type == pygame.QUIT:
                    self.running = False
            # update
            i = self.index
            x = self.x[i]
            y = self.y[i]
            x2 = self.x2[i]
            y2 = self.y2[i]

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
            if self.index == len(self.x): # end of index reached
                self.state = self.last_vals
                self.recalculate(self.state)

            # add controller on top of everything
            self.controller.render(self.screen)
            for slider in self.sliders:
                slider.render(self.screen)
                slider.changeValue()

        pygame.quit()

    def execute(self):
        self.on_init()
        self.object_init()
        self.on_loop()

if __name__ == "__main__":
    simulation = Simulation()
    simulation.execute()
