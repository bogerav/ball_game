import random
from random import randint

import pygame
from pygame.draw import *

pygame.init()

FPS = 30

screen = pygame.display.set_mode((1200, 900))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
"""набор цветов, из которых осуществляется случайный выбор"""



class Ball:
    def __init__(self):
        self.x = randint(100, 1100)
        self.y = randint(100, 800)
        self.r = randint(30, 50)
        self.color = random.choice(COLORS)
        self.degree_x = randint(8, 10)
        self.degree_x *= random.choice([-1, 1])
        self.degree_y = randint(8, 10)
        self.degree_y *= random.choice([-1, 1])

    def draw_ball(self):
        circle(screen, self.color, (self.x, self.y), self.r)

    def hit_ball(self, targ_pos):
        Mouse_x, Mouse_y = targ_pos
        if (((self.x - Mouse_x) ** 2 + (self.y - Mouse_y) ** 2) <= self.r ** 2):
            circle(screen, BLACK, (self.x, self.y), self.r)
            self.color = random.choice(COLORS)
            self.r = randint(30, 50)
            self.x = randint(100, 1100)
            self.y = randint(100, 800)
            self.degree_x = randint(8, 10)
            self.degree_x *= random.choice([-1, 1])
            self.degree_y = randint(8, 10)
            self.degree_y *= random.choice([-1, 1])
            self.draw_ball()
            pygame.display.update()
            return (1)
        else:
            return (0)

    def step(self):
        if (self.x > 1180 or self.x < 20):
            self.degree_x = -self.degree_x
        elif (self.y > 880 or self.y < 0):
            self.degree_y = -self.degree_y
        self.x += self.degree_x
        self.y += self.degree_y
        self.draw_ball()

balls = [Ball() for i in range(5)]
for ball in balls:
    ball.draw_ball()

pygame.display.update()
clock = pygame.time.Clock()
finished = False

fontObj = pygame.font.Font('freesansbold.ttf', 50)

t = 0 #счетчик очков

while not finished:

    textSurfaceObj = fontObj.render(str(t), True, GREEN, BLACK)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (600, 50)
    screen.blit(textSurfaceObj, textRectObj)

    pygame.display.update()
    clock.tick(FPS)
    screen.fill(BLACK)
    for ball in balls:
        ball.step()
        ball.draw_ball()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for ball in balls:
                t += ball.hit_ball(event.pos)

pygame.quit()

