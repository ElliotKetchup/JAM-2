#!/usr/bin/env python3
import pygame as pg
from math import *

WIDTH = 1920
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

def main_menu(screen, running):
    clock = pg.time.Clock()
    font = pg.font.Font("font/Cube.ttf", 68)

    # Set up the buttons

    start_button_rect = pg.Rect(100, 600, 815, 200)
    start_button_text = font.render("Start", True, (255, 255, 255))
    start_button_text_rect = start_button_text.get_rect(center=start_button_rect.center)
    quit_button_rect = pg.Rect(100, 840, 665, 200)
    quit_button_text = font.render("Quit", True, (255, 255, 255))
    quit_button_text_rect = quit_button_text.get_rect(center=quit_button_rect.center)
    active_button = start_button_rect

    while running:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                running = False
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    active_button = start_button_rect
                elif event.key == pg.K_DOWN:
                    active_button = quit_button_rect
                elif event.key == pg.K_RETURN:
                    if active_button == start_button_rect:
                        running = False
                        main_game(screen, True)
                    elif active_button == quit_button_rect:
                        running = False
                        pg.quit()
                        quit()

        screen.fill((0, 0, 0))

        # Draw the buttons

        if active_button == start_button_rect:
            pg.draw.rect(screen, (128, 128, 128), start_button_rect)
            screen.blit(start_button_text, start_button_text_rect)
        else:
            pg.draw.rect(screen, (0, 0, 0), start_button_rect)
            screen.blit(start_button_text, start_button_text_rect)
        if active_button == quit_button_rect:
            pg.draw.rect(screen, (128, 128, 128), quit_button_rect)
            screen.blit(quit_button_text, quit_button_text_rect)
        else:
            pg.draw.rect(screen, (0, 0, 0), quit_button_rect)
            screen.blit(quit_button_text, quit_button_text_rect)
        pg.display.update()

def main_game(screen, running):
    clock = pg.time.Clock()
    ground_group = pg.sprite.Group()
    ground_image = SpriteSheet('ressources/ramp.png').image_at((0, 0, 541, 895))
    ground = Image(0, 0, ground_image)

    while running:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                running = False
                pg.quit()
                quit()

        screen.fill((255, 255, 255))
        pg.display.update()

        ground.draw()

pg.init()

screen = pg.display.set_mode([WIDTH, HEIGHT])
running = True
pg.display.set_caption('Parraski')
main_menu(screen, running)