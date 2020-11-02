import pygame as pg
from threading import Thread
from time import sleep
from pygame.draw import *
from solar_vis import *

class Drawer:
    def __init__(self, screen):
        self.screen = screen
        self.alive = True
        self.figures = []


    def update(self, figures, ui):
        self.screen.fill((0, 0, 0))
        for figure in figures:
            figure.drawOn(self.screen)
        
        ui.blit()
        ui.update()
        pg.display.update()


class DrawableObject:
    def __init__(self, obj):
        self.obj = obj

    def drawOn(self, surface):
        object_ = self.obj
        circle(surface, object_.color, (scale_x(object_.x), scale_y(object_.y)), object_.R)
        
