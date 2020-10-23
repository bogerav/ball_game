import random
from random import randint
import json

import pygame
from pygame.draw import *

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
"""набор цветов, из которых осуществляется случайный выбор"""
screen = pygame.display.set_mode((1200, 900)) #задаем размер экрана



class Target(): #создаем класс цели
    def __init__(self):
        
        self.x = randint(100, 1100) #задаем координаты
        self.y = randint(100, 800)
        self.color = random.choice(COLORS) #цвет цели
        self.degree_x = 10 #значение скорости и ее направление
        self.degree_x *= random.choice([-1, 1])
        self.degree_y = 10 #значение скорости и ее направление
        self.degree_y *= random.choice([-1, 1])

    def step(self): #обработка движения и столкновения со стенами
        k = random.randrange(-10, 10, 1) / 10 #коэф. для случ. отталкивания
        if k == 0: #обход случая когда объект стоит
            k = 0.1
        if (self.x > 1180 or self.x < 20):
            self.degree_y = 10
            self.degree_x = -self.degree_x
            self.degree_y *= k
        elif (self.y > 880 or self.y < 0):
            self.degree_x = 10
            self.degree_y = -self.degree_y
            self.degree_x *= k
        self.x += self.degree_x
        self.y += self.degree_y
        self.draw()

    def hit(self, targ_pos): #обработка попадания курсора по цели
        Mouse_x, Mouse_y = targ_pos
        if (((self.x - Mouse_x) ** 2 + (self.y - Mouse_y) ** 2)
            <= self.r ** 2):
            circle(screen, BLACK, (self.x, self.y), self.r)
            self.color = random.choice(COLORS)
            COLORS.remove(self.color)
            self.color2 = random.choice(COLORS)
            COLORS.append(self.color)
            self.r = randint(15, 25)
            self.x = randint(100, 1100)
            self.y = randint(100, 800)
            self.degree_x = 10
            self.degree_x *= random.choice([-1, 1])
            self.degree_y = 10
            self.degree_y *= random.choice([-1, 1])
            self.draw()
            pygame.display.update()
            return (1)
        else:
            return (0)


class Ball(Target): #класс мяча
    def __init__(self):
        super().__init__()
        self.r = randint(30, 50)

    def draw(self): #рисование мяча
        circle(screen, self.color, (self.x, self.y), self.r)


class Rect(Target): #класс квадрата с кругом, являющимся зоной поражения
    def __init__(self):
        super().__init__()
        self.r = randint(15, 25)
        COLORS.remove(self.color)
        self.color2 = random.choice(COLORS)
        COLORS.append(self.color)

    def draw(self): #рисование квадрата
        rect(screen, self.color, (self.x - 2 * self.r, self.y - 2 * self.r,
                                  4 * self.r, 4 * self.r))
        circle(screen, self.color2, (self.x, self.y), int(self.r))


class GameHelp(): #класс "игрового помощника"
    def __init__(self):

        self.score = 0 #количество очков
        self.mist = 0 #количество ошибок
        self.name = "Unknown" #имя игрока
        self.highscores = None #словарь рекордов
        self.load() #загрузка рекордов

    def load(self): #загрузка рекордов
        """Loads highscores from a file called 'highscores.txt'"""
        try:
            with open('highscores.txt', 'r') as handle:
                text = handle.read()
                if text:
                    self.highscores = json.loads(text)
                    return
        except FileNotFoundError:
            pass
        self.highscores = {}

    def update(self, name, score): #обновление рекорда игрока
        """Update current highscore for user and keep only top 5 users"""
        self.highscores[name] = max(score, self.highscores.get(name, 0))
        self.highscores = {n: s for n, s in self.highscores.items()
                           if s in sorted(self.highscores.values(),
                                          reverse=True)[:5]}

    def save(self): #сохранение нового словаря рекордов
        """Saves highscores to a file called 'highscores.txt'"""
        with open('highscores.txt', 'w') as handle:
            json.dump(self.highscores, handle)

    def clear(self): #очистка словаря рекордов
        """Remves highscores (in memory, save is needed to clear record)"""
        self.highscores = {}

    def lose(self): #обработка проигрыша

        def mist1(): #случай когда 1 ошибка
            fontObj = pygame.font.Font('freesansbold.ttf', 50)
            textSurfaceObj = fontObj.render(str("X"), True, RED, BLACK)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (1080, 70)
            screen.blit(textSurfaceObj, textRectObj)

        def mist2(): #случай когда 1 ошибка
            fontObj = pygame.font.Font('freesansbold.ttf', 50)
            textSurfaceObj = fontObj.render(str("X"), True, RED, BLACK)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (1120, 70)
            screen.blit(textSurfaceObj, textRectObj)

        def mist3(): #случай когда 1 ошибка
            screen.fill(BLACK)
            fontObj = pygame.font.Font('freesansbold.ttf', 50)
            textSurfaceObj = fontObj.render(str("X"), True, RED, BLACK)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (1160, 70)
            screen.blit(textSurfaceObj, textRectObj)
            fontObj = pygame.font.Font('freesansbold.ttf', 100)
            textSurfaceObj = fontObj.render(str("GAME OVER"), True, RED, BLACK)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (600, 400)
            screen.blit(textSurfaceObj, textRectObj)

        if self.mist == 1:
            mist1()
        if self.mist == 2:
            mist1()
            mist2()
        if self.mist == 3:
            mist3()
            mist1()
            mist2()
            self.load()
            self.update(self.name, self.score)
            self.save()
            fontObj = pygame.font.Font('freesansbold.ttf', 50)
            y = 500 #координата "y" начала таблицы рекордов
            gap = 50 #расстоягние между строк таблицы
            list1 = list(self.highscores.items())
            list1.sort(key=lambda i: i[1], reverse=True) #сортировака рекордов

            for member in list1: #вывод таблицы на экран
                textSurfaceObj1 = fontObj.render(member[0], True, RED, BLACK)
                textSurfaceObj2 = fontObj.render(str(member[1]), True,
                                                 RED, BLACK)
                textRectObj1 = textSurfaceObj1.get_rect()
                textRectObj2 = textSurfaceObj2.get_rect()
                textRectObj1.center = (550, y)
                textRectObj2.center = (650, y)
                screen.blit(textSurfaceObj1, textRectObj1)
                screen.blit(textSurfaceObj2, textRectObj2)
                y += gap

            print(self.highscores)
            self.mist += 1

    def start(self): #обработка начала игры

        self.name = input("What's your name? (Max 3 symbols)") #запрос имени
        pygame.init()
        FPS = 30
        fontObj = pygame.font.Font('freesansbold.ttf', 50)

        balls = [Ball() for i in range(5)] #создание целей первого типа
        for ball in balls:
            ball.draw() #появление целей на экране

        rectang = Rect()#создание цели второго типа
        rectang.draw() #появление цели на экране

        pygame.display.update()
        clock = pygame.time.Clock()
        finished = False

        while self.mist != 4: #пока количество ошибок не превысит 3

            self.lose() #проверка на проигрыш
            textSurfaceObj = fontObj.render(str(self.score), True, GREEN, BLACK)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (600, 50)
            screen.blit(textSurfaceObj, textRectObj)
            """ отображение счетчика очков"""

            pygame.display.update()
            clock.tick(FPS)
            screen.fill(BLACK)
            for ball in balls: #движение мячей
                ball.step()
                ball.draw()
            rectang.step() #движение мквадрата
            rectang.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    counter1 = 0 #счетчик попадания в мячи
                    counter2 = 0 #счетчик попадания в квадрат
                    for ball in balls:
                        ev1 = ball.hit(event.pos) #событие попадания в мяч
                        counter1 += ev1
                        self.score += ev1 #одно очко за мяч
                    ev2 = rectang.hit(event.pos) #событие попадания в квадрат
                    self.score += 5 * ev2 #пять очков за квадрат
                    counter2 += ev2
                    if counter1 + counter2 == 0: #проверка попадания в обе цели
                        self.mist += 1 #прибавляем ошибку


game = GameHelp() #создаем игру
game.start() #начинаем игру

