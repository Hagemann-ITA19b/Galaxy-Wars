import pygame
import os
from Settings import Settings
from Turrets import *

class Ship(pygame.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_ships, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.move = False
        self.selected = False
        self.speed = 0
        self.turrets = pygame.sprite.Group()
        self.slot0 = (0,0)


    def mark(self, screen):
        if self.selected:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

    def draw_turrets(self, screen):
        for turret in self.turrets:
            turret.draw(screen)
            turret.update(self.slots[turret.slot])

    def update(self):
        if self.selected:
            self.create_waypoint()
            
        if self.move:
            if self.rect.centerx < self.mouse[0]:
                self.rect.centerx += self.speed
            elif self.rect.centerx > self.mouse[0]:
                self.rect.centerx -= self.speed
            if self.rect.centery < self.mouse[1]:
                self.rect.centery += self.speed
            elif self.rect.centery > self.mouse[1]:
                self.rect.centery -= self.speed
            self.get_slots()

    def create_waypoint(self):
        rightclick = pygame.mouse.get_pressed() == (0, 0, 1)
        if rightclick:
            self.move = True
            self.mouse = pygame.mouse.get_pos()
            for turret in self.turrets:
                turret.shoot(self.mouse[0], self.mouse[1])



class Carrier(Ship):
    def __init__(self, filename):
        super().__init__(filename)
        self.speed = 2
        self.slot0 = (self.rect.centerx, self.rect.centery - 30)
        self.slot1 = (self.rect.centerx, self.rect.centery - 10)
        self.turrets.add(Dualies("dualies.png", self.slot0[0], self.slot0[1], 0))
        self.turrets.add(Dualies("dualies.png", self.slot1[0], self.slot1[1],1))


    def get_slots(self):
        self.slot0 = (self.rect.centerx, self.rect.centery - 30)
        self.slot1 = (self.rect.centerx, self.rect.centery - 10)
        self.slots = [self.slot0, self.slot1]