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

def main_game(screen, running):
    clock = pg.time.Clock()
    ground_group = pg.sprite.Group()

    # Set up the fonts

    font = pg.font.Font(None, 36)

    # Set up the buttons

    start_button_rect = pg.Rect(50, 100, 150, 50)
    start_button_text = font.render("Start", True, (255, 255, 255))
    quit_button_rect = pg.Rect(200, 100, 150, 50)
    quit_button_text = font.render("Quit", True, (255, 255, 255))
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
                        print("Start")
                    elif active_button == quit_button_rect:
                        running = False
                        pg.quit()
                        quit()

        screen.fill((0, 0, 0))
        ground_group.draw(screen)
        pg.display.update()

        # Draw the buttons

        if active_button == start_button_rect:
            pg.draw.rect(screen, (255, 0, 0), start_button_rect)
            screen.blit(start_button_text, (start_button_rect.x + 10, start_button_rect.y + 10))
        else:
            pg.draw.rect(screen, (128, 0, 0), start_button_rect)
            screen.blit(start_button_text, (start_button_rect.x + 10, start_button_rect.y + 10))
        if active_button == quit_button_rect:
            pg.draw.rect(screen, (0, 255, 0), quit_button_rect)
            screen.blit(quit_button_text, (quit_button_rect.x + 10, quit_button_rect.y + 10))
        else:
            pg.draw.rect(screen, (0, 128, 0), quit_button_rect)
            screen.blit(quit_button_text, (quit_button_rect.x + 10, quit_button_rect.y + 10))

pg.init()

screen = pg.display.set_mode([WIDTH, HEIGHT])
running = True
pg.display.set_caption('Parraski')
main_game(screen, running)