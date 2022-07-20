import pygame

class Mass:
    def __init__(self, location, mass, color=(0,250,0)):
        """Ball/mass for the weights,
        location is last known or initial location, tuple (x,y) coordinates
        mass: float or in.
        """
        self.color = color
        self.location = location
        self.mass = mass

    def __repr__(self):
        return f"""Mass:{self.mass}kg located at {self.location}"""

    def render(self, screen):
        # Vol = 4/3 pi r^3, and vol proportional to mass
        self.radius = 5*(3/4*self.mass)**.33
        pygame.draw.circle(screen, self.color, self.location, self.radius)

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




class Checkbox:
    """stolen from:
        https://stackoverflow.com/questions/38551168/radio-button-in-pygame
    """
    def __init__(self, surface, x, y, id, color=(230, 230, 230),
        caption="", outline_color=(0, 0, 0), check_color=(0, 0, 0),
        font_size=18, font_color=(0, 0, 0),
    text_offset=(15, 1), font='Ariel Black', checked=False):
        self.surface = surface
        self.x = x
        self.y = y
        self.color = color
        self.caption = caption
        self.oc = outline_color
        self.cc = check_color
        self.fs = font_size
        self.fc = font_color
        self.to = text_offset
        self.ft = font
        self.checked = checked

        #identification for removal and reorginazation
        self.id = id
        # checkbox object
        self.checkbox_obj = pygame.Rect(self.x, self.y, 12, 12)
        self.checkbox_outline = self.checkbox_obj.copy()

    def _draw_button_text(self):
        self.font = pygame.font.SysFont(self.ft, self.fs)
        self.font_surf = self.font.render(self.caption, True, self.fc)
        w, h = self.font.size(self.caption)
        self.font_pos = (self.x + self.to[0], self.y + 12 / 2 - h / 2 +
        self.to[1])
        self.surface.blit(self.font_surf, self.font_pos)

    def render(self):
        if self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
            pygame.draw.circle(self.surface, self.cc, (self.x + 6, self.y + 6), 4)

        elif not self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
        self._draw_button_text()

    def _update(self, event_object):
        x, y = pygame.mouse.get_pos()
        px, py, w, h = self.checkbox_obj
        if px < x < px + w and py < y < py + w:
            if self.checked:
                self.checked = False
            else:
                self.checked = True

    def update_checkbox(self, event_object):
        if event_object.type == pygame.MOUSEBUTTONDOWN:
            self.click = True
            self._update(event_object)

class Slider:
    # Shamelessly stolen and modified from stack overflow:
    # https://stackoverflow.com/questions/65482148/creating-sliders-using-pygame
    def __init__(self, position:tuple, startingValue:int=1, w:int = 20, h:int = 80,  font_color=(0,255,0), text:str="")->None:
        self.position = position
        self.w = w
        # NOTE: can't figure out how to take the starting height change
        # It will default to 1, but it's not linear
        self.h = h
        self.outlineSize = (self.w,self.h) # original dim. vals change on slide
        self.upperValue = 10
        self.startingValue = startingValue
        self.text = text
        self.font_color = font_color
        self.starting = True # set to False after 1st time "changeValue" called
        self.test = 1

    #returns the current value of the slider
    def getValue(self)->float:
        if self.starting:
            return self.startingValue
        else:
            # add 1 to keep mass >= 1 (can't handle 0 mass)
            return abs(1+self.upperValue - (self.h / (self.outlineSize[1] / self.upperValue)))

    def render(self, display:pygame.display)->None:
        #draw outline and slider rectangles
        pygame.draw.rect(display, (50, 50, 50),
            (self.position[0], self.position[1], self.outlineSize[0], self.outlineSize[1]), 3)

        pygame.draw.rect(display, (0, 0, 0),
                (self.position[0], self.position[1] + self.h, self.w , self.outlineSize[1] - self.h))

        #determine size of font
        self.font = pygame.font.Font(pygame.font.get_default_font(), int(1.5*self.w))

        #create text surface with value
        valueSurf = self.font.render(f"{self.text}{round(self.getValue())}", True, self.font_color)

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
                self.starting = False


