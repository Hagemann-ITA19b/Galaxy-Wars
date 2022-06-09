import pygame
import os
from Settings import Settings
from Turrets import *
from random import randint
from Ships import *
from math import cos, sin
class Starfighter(pygame.sprite.Sprite):
    def __init__(self, filename, team):
        super().__init__()
        self.size = (20,20)
        self.original_image = pygame.image.load(os.path.join(Settings.path_starfighters, filename)).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, self.size)
        self.image = pygame.image.load(os.path.join(Settings.path_starfighters, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.mouse = pygame.mouse.get_pos()
        self.mouse = (self.mouse[0] - randint(-100, 100), self.mouse[1] - randint(-100, 100))
        self.rect.center = self.mouse
        self.move = False
        self.rotated = False
        self.selected = False
        self.speed = 10
        self.rotation_speed = 5
        self.turrets = pygame.sprite.Group()
        self.team = team
        self.range = 500
        self.aiming = False
        self.hull = 100
        self.shields = 50
        self.regeneration_rate = 1
        self.destroyed = False
        self.current_angle = 0
        self.slots = 2
        self.stored_fighters = 0
        self.angle = 0
        self.idle = False
        

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

        if self.stored_fighters > 0:
            self.spawn_fighter()
            self.stored_fighters -= 1        

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

            collision_rect = (self.rect.center[0] + self.rotation_speed, self.rect.center[1] + self.rotation_speed)
            if self.waypoint.collidepoint(collision_rect):
                self.move = False
                self.rotated = False

        elif self.move == False and self.rotated == False:
            self.idle = True
            self.move_sprite_in_circle()
            

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


    def move_sprite_in_circle(self):
        if self.idle:
            rel_x, rel_y = self.mouse[0] - self.rect.centerx, self.mouse[1] - self.rect.centery
            angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
            if self.current_angle < angle:
                self.current_angle = self.current_angle + self.rotation_speed
            elif self.current_angle > angle:
                self.current_angle = self.current_angle - self.rotation_speed

            self.image = pygame.transform.rotate(self.original_image, int(self.current_angle))
            self.rect = self.image.get_rect(center=self.rect.center)

            center = self.mouse
            self.rect.center = [center[0] + 100 * cos(self.angle), center[1] + 100 * sin(self.angle)]
            self.angle += 0.01
      
          
