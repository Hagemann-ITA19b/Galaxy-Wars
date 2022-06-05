from posixpath import splitdrive
import pygame
import os
from Settings import Settings
import math
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

    def move(self):
        self.x = self.x + self.dx 
        self.y = self.y + self.dy 
        self.rect.x = int(self.x) 
        self.rect.y = int(self.y)
        self.kill_after_time()

    def kill_after_time(self):
        self.travel_time = self.travel_time + 1
        if self.travel_time > 20:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Turret(pygame.sprite.Sprite):
    def __init__(self, filename,x,y, slot):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_turrets, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.projectile = pygame.sprite.Group()
        self.slot = slot
        ##range of turret in circle
        self.range = 100
        #self.range_circle = pygame.draw.circle(screen, (255, 0, 0), self.rect.center, self.range)

    def update(self, slot):
        self.rect.center = slot
        for projectile in self.projectile:
            projectile.move()


    def shoot(self, target, target_group):
        self.projectile.add(Projectile("bullet.png", target[0], target[1], self.rect.centerx, self.rect.centery))

        for projectile in self.projectile:
            for target in target_group:
                if projectile.rect.colliderect(target.rect):
                    projectile.kill()
                    if target.shields <= 0:
                        target.hull = target.hull - 10
                    else:
                        target.shields = target.shields - 10
                    break

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for projectile in self.projectile:
            projectile.draw(screen)
        
class Dualies(Turret):
    def __init__(self, filename, x, y, slot):
        super().__init__(filename, x, y, slot)
        self.damage = 10
        self.range = 100
        self.rate = 1




    