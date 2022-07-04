import pygame
from economy import *
from random import randint

class Enemy():
    def __init__(self) -> None:
        self.eco = Economy(2, 50, 1)
        self.spawn = False
        self.clock_time = pygame.time.get_ticks()
        self.rate = 100
        self.spawnlimit = 100
        self.ship = None

    def roll(self):
        print(self.eco.budget)
        d = randint(1, 20)
        if self.spawnlimit > 0:
            if d == 1:
                if self.eco.level == 0:
                    pass
                elif self.eco.level == 1:
                    self.ship = 0
                elif self.eco.level == 2:
                    self.ship = randint(0,1)
                elif self.eco.level == 3:
                    self.ship == randint(0,2)
                elif self.eco.level == 4:
                    self.ship = randint(0,3)
                elif self.eco.level == 5:
                    self.ship = randint(0,4)
                elif self.eco.level == 6:
                    self.ship = randint(4,5)
                self.spawn = True
                self.spawnlimit -= 1
        else:
                self.spawn = False

    def update(self):
        if pygame.time.get_ticks() > self.clock_time:
            self.clock_time = pygame.time.get_ticks() + self.rate
            self.roll()
        else:
            self.spawn = False
        self.eco.update()