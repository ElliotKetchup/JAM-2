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

class Obstacle(pg.sprite.Sprite):
    def __init__(self, x, y, image, angle):
        super(Obstacle, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.image = pg.transform.rotate(self.image, angle)


    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y

class Ramp(pg.sprite.Sprite):
    def __init__(self, x, y, image):
        super(Ramp, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def rotate(self, angle):
        self.image = pg.transform.rotate(self.image, angle)

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y

    def delete(self):
        self.kill()

def main_menu(screen, running):
    clock = pg.time.Clock()
    font = pg.font.Font("font/Paralis.ttf", 64)
    font_title = pg.font.Font("font/Paralis.ttf", 90)

    # Set up the buttons

    start_button_rect = pg.Rect((WIDTH / 2) - 500 / 2, 600, 500, 150)
    start_button_text = font.render("Start", True, (255, 255, 255))
    start_button_text_rect = start_button_text.get_rect(center=start_button_rect.center)
    quit_button_rect = pg.Rect((WIDTH / 2) - 500 / 2, 800, 500, 150)
    quit_button_text = font.render("Quit", True, (255, 255, 255))
    quit_button_text_rect = quit_button_text.get_rect(center=quit_button_rect.center)
    active_button = start_button_rect

    # Set Title

    title_text = font_title.render("Parraski", True, (255, 255, 255))
    title_text_rect = title_text.get_rect(center=(WIDTH/2, 300))

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

        # Draw the title

        pg.draw.rect(screen, (0, 0, 0), title_text_rect)
        screen.blit(title_text, title_text_rect)

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
    ramp_group = pg.sprite.Group()
    ramp_image = SpriteSheet('ressources/Untitled.png').image_at((0, 0, 2698, 587))
    new_ramp0 = Ramp(-200, -200, ramp_image)
    new_ramp0.rotate(-45)
    ramp_group.add(new_ramp0)
    ticks = pg.time.get_ticks()
    font = pg.font.Font(None, 54)

    while running:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                running = False
                pg.quit()
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                print(pg.mouse.get_pos())

        screen.fill((255, 255, 255))
        for sprite in ramp_group:
            if sprite.rect.x < - 541 and sprite.rect.y < - 587:
                sprite.delete()
                new_ramp0 = Ramp(-200, -200, ramp_image)
                new_ramp0.rotate(-45)
                ramp_group.add(new_ramp0)
            sprite.draw()
            sprite.move(-1, -1)

        # calculate elapsed time
        milliseconds = pg.time.get_ticks() - ticks
        seconds = int(milliseconds / 1000) % 60
        minutes = int(seconds / 60)
        milliseconds = milliseconds % 1000

        # draw chronometer
        chronometer = font.render(f"{minutes:02}:{seconds:02}:{milliseconds:03}", True, (0, 0, 0))
        screen.blit(chronometer, (WIDTH - 190, 15))

        # update screen
        pg.display.update()

pg.init()

screen = pg.display.set_mode([WIDTH, HEIGHT], pg.RESIZABLE)
running = True
pg.display.set_caption('Parraski')
main_menu(screen, running)