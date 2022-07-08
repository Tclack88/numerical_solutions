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
        print(self.location)
        
    def render(self, screen):
        print('in render, location is:')
        print(self.location)
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
        print(self.location)
        
    def render(self, screen):
        print('in render, location is:')
        print(self.location)
        pygame.draw.circle(screen, (200,200,200), self.location, self.radius)



class Simulation:
    def __init__(self):
        self.running = True
        self.size = self.WIDTH, self.HEIGHT = 1000,1000
        self.screen = pygame.display.set_mode(self.size)

    def on_init(self):
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.FPS = 30

    def object_init(self):
        self.pulleys = [Pulley((self.WIDTH/3,self.HEIGHT/2)),
            Pulley((self.WIDTH*2/3, self.HEIGHT/2))]
        self.masses = [Mass((300,700), 1),
                Mass((600,800), 3)]

    def on_loop(self):
        while self.running:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            # update
            for mass in self.masses:
                mass.update()
            pygame.display.update()
            # draw / render
            self.screen.fill((0,0,0))
            for mass in self.masses:
                mass.render(self.screen)
            for pulley in self.pulleys:
                pulley.render(self.screen)

            # draw line connecting masses and pulleys
            points = [self.masses[0].location,
                    self.pulleys[0].location,
                    self.pulleys[1].location,
                    self.masses[1].location]
            pygame.draw.lines(self.screen, (200,200,200), False, points)

        pygame.quit()

    def execute(self):
        self.on_init()
        self.object_init()
        self.on_loop()

if __name__ == "__main__":
    simulation = Simulation()
    simulation.execute()
