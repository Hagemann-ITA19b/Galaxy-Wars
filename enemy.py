import pygame
from economy import *
from random import randint

class Enemy():
    def __init__(self) -> None:
        self.eco = Economy(2, 50, 1)
        self.spawn = False
        self.clock_time = pygame.time.get_ticks()
        self.rate = 100

    def roll(self):
        d = randint(1, 500)
        if d == 1:
            self.spawn = True
        else:
            self.spawn = False

    def update(self):
        if pygame.time.get_ticks() > self.clock_time:
            self.clock_time = pygame.time.get_ticks() + self.rate
            self.roll()

        self.eco.update()