from re import X
import pygame
import os
import math
from Settings import Settings
from random import randint

class Projectile(pygame.sprite.Sprite):
    def __init__(self, filename, dx, dy,x,y): #delta x and delta y
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_bullets, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.bullet_size)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        x = self.rect.left
        y = self.rect.top
        self.speed = randint(20,30)
        self.angle = math.atan2(dy-y , dx-x) #dx and dy are the coordinates for the cursor
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed
        self.x = x
        self.y = y
        self.travel_time = 0

    def move(self, bullet_range):
        self.x = self.x + self.dx 
        self.y = self.y + self.dy 
        self.rect.x = int(self.x) 
        self.rect.y = int(self.y)
        self.kill_after_time(bullet_range)

    def kill_after_time(self, bullet_range):
        self.travel_time = self.travel_time + 1
        if self.travel_time > bullet_range*0.039:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Turret(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.projectile = pygame.sprite.Group()
        self.range = 100
        self.x = x
        self.y = y
        self.clock_time = pygame.time.get_ticks()
        

    def update(self,xy):
        self.x = xy[0]
        self.y = xy[1]
        for projectile in self.projectile:
            projectile.move(self.range)


    def shoot(self, target, target_group):
        if pygame.time.get_ticks() > self.clock_time:
            self.clock_time = pygame.time.get_ticks() + self.rate
            for i in range(self.gunbarrel):
                self.projectile.add(Projectile(self.image, target[0], target[1],self.x + i*10 ,self.y + i*10))
        for projectile in self.projectile:
            for target in target_group:
                if projectile.rect.colliderect(target.rect):
                    projectile.kill()
                    if target.shields <= 0:
                        target.hull = target.hull - self.damage_hull
                    else:
                        target.shields = target.shields - self.damage_shield
                    break

    def draw(self, screen):
        for projectile in self.projectile:
            projectile.draw(screen)

        
class Dualies(Turret):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.gunbarrel = 2
        self.damage_shield = 20
        self.damage_hull = 5
        self.range = 500
        self.rate = 50
        self.image = "bullet.png"

class Breacher(Turret):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.speed = 1
        self.gunbarrel = 1
        self.damage_shield = 0
        self.damage_hull = 300
        self.range = 5000
        self.rate = 5000
        self.image = "breacher.png"




    