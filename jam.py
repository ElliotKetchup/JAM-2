#!/usr/bin/env python3
import random
import pygame as pg
from math import *
import sys
import os

WIDTH = 1980
HEIGHT = 1080

class SpriteSheet(object):
    def __init__(self, fileName):
        self.sheet = pg.image.load(fileName).convert_alpha() 

    def image_at(self, rectangle):
        rect = pg.Rect(rectangle)
        image = pg.Surface(rect.size, pg.SRCALPHA, 32).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        return image

class Image():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

def main_game(screen, running):
    clock = pg.time.Clock()
    ground_group = pg.sprite.Group()

pg.init()


screen = pg.display.set_mode([WIDTH, HEIGHT])
running = True
pg.display.set_caption('Parraski')
main_game(screen, running)