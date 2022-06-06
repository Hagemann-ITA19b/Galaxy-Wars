import pygame
import os
from Settings import Settings
from Turrets import *
from random import randint

class Ship(pygame.sprite.Sprite):
    def __init__(self, filename, team):
        super().__init__()
        self.size = (300,300)
        self.original_image = pygame.image.load(os.path.join(Settings.path_ships, filename)).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, self.size)
        self.image = pygame.image.load(os.path.join(Settings.path_ships, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.mouse = pygame.mouse.get_pos()
        self.rect.center = self.mouse
        self.move = False
        self.rotated = False
        self.selected = False
        self.speed = 0
        self.rotation_speed = 1
        self.turrets = pygame.sprite.Group()
        self.team = team
        self.range = 500
        self.aiming = False
        self.hull = 1000
        self.shields = 1000
        self.regeneration_rate = 1
        self.destroyed = False
        self.current_angle = 0
        self.slots = 2
        self.stored_fighters = 0
  
        

    def range_check(self, screen):
        self.range_circle = pygame.draw.circle(screen, (255, 0, 0), self.rect.center, self.range)

    def update_target(self, target, group):
            self.shoot(target.rect.center, group)

    def regenerate(self):
        if self.shields < 1000:
            self.shields += self.regeneration_rate

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
                
                self.target = None
                self.target_group = None
                self.aiming = False

        if self.aiming == True:
            self.update_target(self.target, self.target_group)
                

    def mark(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), (self.rect.centerx - 50, self.rect.centery - 61, self.shields *0.1, 3))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.centerx - 50, self.rect.centery - 58, self.hull* 0.1, 3))
        if self.selected:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

    def draw(self, screen):
        if self.selected:
            self.create_waypoint(screen)
        
        self.mark(screen)
        self.draw_turrets(screen)
        screen.blit(self.image, self.rect)
        

    def draw_turrets(self, screen):
        for turret in self.turrets:
            turret.draw(screen)


    def update(self):
        if self.selected:
            self.mouse_actions()
            
        for turret in self.turrets:
            turret.update(self.rect.center)
      
        if self.rotated:
            self.rotate(self.mouse[0], self.mouse[1])

        if self.move:
            if self.rect.centerx < self.mouse[0]:
                self.rect.centerx += self.speed
            if self.rect.centerx > self.mouse[0]:
                self.rect.centerx -= self.speed
            if self.rect.centery < self.mouse[1]:
                self.rect.centery += self.speed
            if self.rect.centery > self.mouse[1]:
                self.rect.centery -= self.speed

            if self.waypoint.collidepoint(self.rect.center):
                self.move = False
                self.rotated = False

            
        
        self.regenerate()
        self.check_death()

    def mouse_actions(self):
        rightclick = pygame.mouse.get_pressed() == (0, 0, 1)
        leftclick = pygame.mouse.get_pressed() == (0, 1, 0)
        if rightclick:
            self.rotated = True
            self.mouse = pygame.mouse.get_pos()
            
        if leftclick:
            self.mouse = pygame.mouse.get_pos()
            for turret in self.turrets:
                turret.shoot(self.mouse[0], self.mouse[1])

    def create_waypoint(self, screen):
        self.waypoint = pygame.draw.circle(screen, (255, 255, 0), self.mouse, 5)
        
    def shoot(self, target, target_group):
        for turret in self.turrets:
            turret.shoot(target, target_group)

    def check_death(self):
        if self.hull <= 0:
            self.destroyed = True
            self.kill()

    def rotate(self, dx,dy):
        rel_x, rel_y = dx - self.rect.centerx, dy - self.rect.centery
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) -90
        if self.current_angle < angle:
            self.current_angle = self.current_angle + self.rotation_speed
        elif self.current_angle > angle:
            self.current_angle = self.current_angle - self.rotation_speed

        self.image = pygame.transform.rotate(self.original_image, int(self.current_angle))
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.current_angle < angle + self.rotation_speed and self.current_angle > angle - self.rotation_speed:
            self.move = True
            self.rotated = False

  

class Carrier(Ship):
    def __init__(self, filename, team):
        super().__init__(filename, team)
        self.turrets.add(Dualies(randint(self.rect.left,self.rect.right), randint(self.rect.top, self.rect.bottom)))
        self.speed = 2
        self.stored_fighters = 3

class Assault(Ship):
    def __init__(self, filename, team):
        super().__init__(filename, team)
        self.speed = 2
        self.turrets.add(Dualies(randint(self.rect.left,self.rect.right), randint(self.rect.top, self.rect.bottom)))
        self.turrets.add(Breacher(randint(self.rect.left,self.rect.right), randint(self.rect.top, self.rect.bottom)))
        self.range = 500

    def speed_up(self):
        self.speed += 1

