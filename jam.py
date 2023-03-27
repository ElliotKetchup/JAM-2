#!/usr/bin/env python3
import pygame as pg
from math import *
from random import *

WIDTH = 1920
HEIGHT = 1080
SCROLL_SPEED = -8

class Foreground(pg.sprite.Sprite):
    def __init__(self, image, vitesse_scroll):
        super(Foreground, self).__init__()
        self.image = image.image
        self.rect = image.rect
        self.xrect = image.rect.x
        self.yrect = image.rect.y
        self.count = 0
        self.vitesse_scroll = vitesse_scroll
        self.image = pg.transform.scale(self.image, (WIDTH * 2, HEIGHT))
    def update(self):
        if int(self.count) <= -WIDTH:
            self.count = 0
        self.rect.topleft = (self.count, self.rect.y)
        self.count -= self.vitesse_scroll

    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def draw (self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

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
    def __init__(self, x, y, surf, spawn_location):
        super(Obstacle, self).__init__()
        self.surf = surf
        self.rect = self.surf.get_rect(topleft = (spawn_location))
        self.rect.topleft = (x,y)

    def draw(self):
        screen.blit(self.surf, (self.rect.x, self.rect.y))

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y

    def delete(self):
        self.kill()

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

class Player(pg.sprite.Sprite):
    def __init__(self, x, y, dico_anim,):
        super(Player, self).__init__()
        self.x = x
        self.y = y
        self.dico_anim = dico_anim
        self.surf = self.dico_anim[0]
        self.rect = self.surf.get_rect(topleft = (x,y))
        self.count = 0
        self.animation_speed = 0.1
        self.is_jumping = False
        self.jump_speed = 10  # adjust as needed
        self.air_time = 0

    def update(self): # update the animation
        if not self.is_jumping:
            if int(self.count) > len(self.dico_anim)-1:
                self.count = 0

            self.surf = self.dico_anim[int(self.count)]
            self.count+= self.animation_speed

        if self.is_jumping:
            self.rect.y += self.jump_speed - (self.air_time * 2)
            self.air_time -= 1

            if self.air_time <= 0:
                self.is_jumping = False
                self.rect.topleft = (self.rect.x, self.y)


    def draw(self):
        screen.blit(self.surf, (self.rect.x, self.rect.y))

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.air_time = 20  # adjust as needed

def end_game(screen, running, elapsed_time):
    font_button = pg.font.Font("font/Paralis.ttf", 64)
    font_text = pg.font.Font(None, 50)
    clock = pg.time.Clock()

    # set up the buttons

    restart_button_rect = pg.Rect((WIDTH / 2) - 500 / 2, 600, 500, 150)
    restart_button_text = font_button.render("Restart", True, (255, 255, 255))
    restart_button_text_rect = restart_button_text.get_rect(center=restart_button_rect.center)
    quit_button_rect = pg.Rect((WIDTH / 2) - 500 / 2, 800, 500, 150)
    quit_button_text = font_button.render("Quit", True, (255, 255, 255))
    quit_button_text_rect = quit_button_text.get_rect(center=quit_button_rect.center)
    active_button = restart_button_rect

    # set up the text

    text = font_text.render("You have skied for : {:02d}:{:02d}:{:03d}".format(elapsed_time // 60000, (elapsed_time // 1000) % 60, elapsed_time % 1000), True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH/2, 300))

    while running:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                running = False
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    active_button = restart_button_rect
                elif event.key == pg.K_DOWN:
                    active_button = quit_button_rect
                elif event.key == pg.K_RETURN:
                    if active_button == restart_button_rect:
                        running = False
                        main_game(screen, True)
                    elif active_button == quit_button_rect:
                        running = False
                        pg.quit()
                        quit()

        # Draw the title

        pg.draw.rect(screen, (0, 0, 0), text_rect)
        screen.blit(text, text_rect)

        # Draw the buttons

        if active_button == restart_button_rect:
            pg.draw.rect(screen, (128, 128, 128), restart_button_rect)
            screen.blit(restart_button_text, restart_button_text_rect)
        else:
            pg.draw.rect(screen, (0, 0, 0), restart_button_rect)
            screen.blit(restart_button_text, restart_button_text_rect)
        if active_button == quit_button_rect:
            pg.draw.rect(screen, (128, 128, 128), quit_button_rect)
            screen.blit(quit_button_text, quit_button_text_rect)
        else:
            pg.draw.rect(screen, (0, 0, 0), quit_button_rect)
            screen.blit(quit_button_text, quit_button_text_rect)
        pg.display.update()

def main_menu(screen, running):
    clock = pg.time.Clock()
    font = pg.font.Font("font/Paralis.ttf", 64)
    font_title = pg.font.Font("font/Paralis.ttf", 90)

    # Set up the buttons

    timea = 0
    timeb = 0
    timec = 2000
    clock = pg.time.Clock()
    back = Image(0, 0, pg.image.load('./ressources/background.png'))
    back.image = pg.transform.scale(back.image, (WIDTH, HEIGHT))
    forest1 = Image(0, -500, pg.image.load('./ressources/huge_foreste.png'))
    moutain = Image(0, -500, pg.image.load('./ressources/moutain_pink.png'))
    moutain2 = Image(1980, -500, pg.image.load('./ressources/moutain_pink.png'))
    foreground_group = pg.sprite.Group()
    forest_sprite = Foreground(forest1, 50)
    moutain_sprite = Foreground(moutain, 50)
    moutain_sprite2 = Foreground(moutain2, 50)
    foreground_group.add(moutain_sprite)
    foreground_group.add(moutain_sprite2)
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

        #draw background
        timea = timea - (clock.get_time() * 1.5)
        timeb = timeb - (clock.get_time() / 2)
        timec = timec - (clock.get_time() / 3)
        back.draw()
        foreground_group.draw(screen)
        forest_sprite.draw(screen)
        forest_sprite.move(timea, -500)
        moutain_sprite2.move((timec) , -500)
        moutain_sprite.move((timeb), -500)

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

        if timea  <= -1500:
            timea = 0
        if timeb  <= -3700:
            timeb = 700
        if timec  <= -3700:
            timec = 1500
        pg.display.update()

def main_game(screen, running):
    timea = 0
    timeb = 0
    timec = 2000

    clock = pg.time.Clock()
    back = Image(0, 0, pg.image.load('./ressources/background.png'))
    back.image = pg.transform.scale(back.image, (WIDTH, HEIGHT))
    forest1 = Image(0, -500, pg.image.load('./ressources/huge_foreste.png'))
    moutain = Image(0, -500, pg.image.load('./ressources/moutain_pink.png'))
    moutain2 = Image(1980, -500, pg.image.load('./ressources/moutain_pink.png'))
    foreground_group = pg.sprite.Group()
    forest_sprite = Foreground(forest1, 50)
    moutain_sprite = Foreground(moutain, 50)
    moutain_sprite2 = Foreground(moutain2, 50)
    foreground_group.add(moutain_sprite)
    foreground_group.add(moutain_sprite2)

    ramp_group = pg.sprite.Group()
    ramp_image = SpriteSheet('ressources/Untitled.png').image_at((0, 0, 2698, 587))
    new_ramp0 = Ramp(-200, -200, ramp_image)
    new_ramp0.rotate(-45)
    ramp_group.add(new_ramp0)
    obstacle_group = pg.sprite.Group()
    arbre_image = SpriteSheet('ressources/arbre.png').image_at((0, 0, 17, 29))
    arbre_image = pg.transform.scale(arbre_image, (17*3, 29*3))
    arbre_enfer_image = SpriteSheet('ressources/arbre_enfer.png').image_at((0, 0, 17, 29))
    arbre_enfer_image = pg.transform.scale(arbre_enfer_image, (17*5, 29*5))

    skier_image = SpriteSheet("ressources/reimusheet.png")
    skier0 = pg.transform.scale(skier_image.image_at((3, 0, 22, 23)), (22*5, 23*5))
    skier1 = pg.transform.scale(skier_image.image_at((30, 0, 22, 23)), (22*5, 23*5))
    skier2 = pg.transform.scale(skier_image.image_at((56, 0, 22, 23)), (22*5, 23*5))
    skier3 = pg.transform.scale(skier_image.image_at((84, 0, 22, 23)), (22*5, 23*5))
    skier4 = pg.transform.scale(skier_image.image_at((110, 0, 22, 23)), (22*5, 23*5))
    skier5 = pg.transform.scale(skier_image.image_at((136, 0, 22, 23)), (22*5, 23*5))
    dico_skier = {0: skier0, 1: skier1, 2: skier2, 3: skier3, 4: skier4, 5: skier5}
    skier_top = Player(590, 220, dico_skier)
    skier_bottom = Player(150, 460, dico_skier)
    skier_group = pg.sprite.Group()
    skier_group.add(skier_top)


    ticks = pg.time.get_ticks()
    font = pg.font.Font(None, 54)

    while running:
        clock.tick(60)
        keys = pg.key.get_pressed()

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                running = False
                pg.quit()
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                print(pg.mouse.get_pos())
            elif (event.type == pg.KEYDOWN and event.key == pg.K_TAB):
                end_game(screen, running, elapsed_time)

        if keys[pg.K_SPACE]:
            skier_top.jump()
        # move and draw the background
        time = clock.get_time()
        timea = timea - (time * 1)
        timeb = timeb - (time / 2)
        timec = timec - (time / 3)
        back.draw()
        foreground_group.draw(screen)
        forest_sprite.draw(screen)
        forest_sprite.move(timea, -500)
        moutain_sprite2.move((timec) , -500)
        moutain_sprite.move((timeb), -500)

        # Create, draw, move and delete the ramps
        for sprite in ramp_group:
            if sprite.rect.x < - 541 and sprite.rect.y < - 587:
                sprite.delete()
                new_ramp0 = Ramp(-215, -215, ramp_image)
                new_ramp0.rotate(-45)
                ramp_group.add(new_ramp0)
            sprite.draw()
            sprite.move(SCROLL_SPEED, SCROLL_SPEED)

        # Create the obstacles
        if randrange(0, 100) == 0:
            new_obstacle = Obstacle(1400, 1050, arbre_image, (16, 28))
            obstacle_group.add(new_obstacle)
        if randrange(0, 100) == 0:
            new_obstacle = Obstacle(800, 1050, arbre_enfer_image, (12, 19))
            obstacle_group.add(new_obstacle)
        # Draw and move the obstacles
        for sprite in obstacle_group:
            if sprite.rect.x < - 541 and sprite.rect.y < - 587:
                sprite.delete()
            sprite.draw()
            sprite.move(SCROLL_SPEED, SCROLL_SPEED)

        # Draw and move the player
        for sprite in skier_group:
            sprite.draw()
            sprite.update()

        # calculate elapsed time
        milliseconds = pg.time.get_ticks() - ticks
        elapsed_time = milliseconds
        seconds = milliseconds // 1000
        minutes = seconds // 60
        milliseconds = elapsed_time % 1000
        seconds = seconds % 60

        # draw chronometer
        chronometer = font.render(f"{minutes:02}:{seconds:02}:{milliseconds:03}", True, (0, 0, 0))
        screen.blit(chronometer, (WIDTH - 190, 15))


        if timea  <= -1500:
            timea = 0
        if timeb  <= -3700:
            timeb = 700
        if timec  <= -3700:
            timec = 1500

        # update screen
        pg.display.update()

pg.init()

screen = pg.display.set_mode([WIDTH, HEIGHT], pg.RESIZABLE)
running = True
pg.display.set_caption('Parraski')
main_menu(screen, running)