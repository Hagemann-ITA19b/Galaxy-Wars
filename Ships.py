import pygame
import os
from Settings import Settings
from Turrets import *
from random import randint

class Ship(pygame.sprite.Sprite):
    def __init__(self, filename, team):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_ships, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.mouse = pygame.mouse.get_pos()
        self.rect.center = self.mouse
        self.move = False
        self.selected = False
        self.speed = 0
        self.turrets = pygame.sprite.Group()
        self.slot0 = (0,0)
        self.team = team
        self.range = 500
        self.target_list = []
        self.aiming = False
        self.hull = 1000
        self.shields = 1000
        self.destroyed = False

    def range_check(self, screen):
        self.range_circle = pygame.draw.circle(screen, (255, 0, 0), self.rect.center, self.range)

    def update_target(self, target, group):
        self.shoot(target.rect.center, group)
        print(self.target.rect.center)

    def get_range(self, target, group):
        if self.aiming == False:
            if self.range_circle.collidepoint(target.rect.center):
                self.aiming = True
                self.target = target
                self.target_group = group
            else:
                self.aiming = False
                self.target = None
                self.target_group = None

        if self.aiming == True:
            if not self.range_circle.collidepoint(self.target.rect.center) or self.target.destroyed:
                print("Not in range")
                
                self.target = None
                self.target_group = None
                self.aiming = False

        if self.aiming == True:
            self.update_target(self.target, self.target_group)
                

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
        
        self.check_death()

    def create_waypoint(self):
        rightclick = pygame.mouse.get_pressed() == (0, 0, 1)
        leftclick = pygame.mouse.get_pressed() == (0, 1, 0)
        if rightclick:
            self.move = True
            self.mouse = pygame.mouse.get_pos()

        if leftclick:
            self.mouse = pygame.mouse.get_pos()
            for turret in self.turrets:
                turret.shoot(self.mouse[0], self.mouse[1])

    def shoot(self, target, target_group):
        for turret in self.turrets:
            turret.shoot(target, target_group)

    def check_death(self):
        if self.hull <= 0:
            self.destroyed = True
            self.kill()

class Carrier(Ship):
    def __init__(self, filename, team):
        super().__init__(filename, team)
        self.speed = 2
        self.slot0 = (self.rect.centerx, self.rect.centery - 30)
        self.slot1 = (self.rect.centerx, self.rect.centery - 10)
        self.turrets.add(Dualies("dualies.png", self.slot0[0], self.slot0[1], 0))
        self.turrets.add(Dualies("dualies.png", self.slot1[0], self.slot1[1],1))


    def get_slots(self):
        self.slot0 = (self.rect.centerx, self.rect.centery - 30)
        self.slot1 = (self.rect.centerx, self.rect.centery - 10)
        self.slots = [self.slot0, self.slot1]

class Assault(Ship):
    def __init__(self, filename):
        super().__init__(filename)
        self.speed = 2
        self.slot0 = (self.rect.centerx +10, self.rect.centery - 30)
        self.slot1 = (self.rect.centerx - 10, self.rect.centery - 10)
        self.turrets.add(Dualies("dualies.png", self.slot0[0], self.slot0[1], 0))
        self.turrets.add(Dualies("dualies.png", self.slot1[0], self.slot1[1],1))


    def get_slots(self):
        self.slot0 = (self.rect.centerx, self.rect.centery - 30)
        self.slot1 = (self.rect.centerx, self.rect.centery - 10)
        self.slots = [self.slot0, self.slot1]

    def speed_up(self):
        self.speed += 1

