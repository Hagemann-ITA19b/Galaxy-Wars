import pygame
import os
from settings import Settings
from turrets import *
from random import randint

class Ship(pygame.sprite.Sprite):
    def __init__(self, filename, team):
        super().__init__()
        self.size = (150,150)
        self.original_image = pygame.image.load(os.path.join(Settings.path_ships, filename)).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, self.size)
        self.image = self.original_image
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
        self.stored_fighters = 0
        #for animation
        self.images = []
        self.imageindex = 0
        self.clock_time = pygame.time.get_ticks()
        self.animation_time = 50
        self.images.append(self.original_image) 

        self.waypoint_x = self.mouse[0] 
        self.waypoint_y = self.mouse[1]

        #check sprites
        self.appended_damaged = False


    def update_sprite(self):
        if self.appended_damaged == False:
            if self.hull < 800:
                self.appended_damaged = True
                self.images.clear()
                for i in range(4):
                    bitmap = pygame.image.load(os.path.join(
                        self.path, self.name+f"_damaged{i}.png"))
                    scaled = pygame.transform.scale(bitmap,self.size)
                    self.images.append(scaled)

    def animate(self):
            if pygame.time.get_ticks() > self.clock_time:
                self.clock_time = pygame.time.get_ticks() + self.animation_time
                self.image = pygame.transform.rotate(self.original_image, int(self.current_angle))
                self.imageindex += 1
                if self.imageindex >= len(self.images):
                    self.imageindex = 0
                self.original_image = self.images[self.imageindex]

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
            self.update_target(self.target, self.target_group)
            if not self.range_circle.collidepoint(self.target.rect.center) or self.target.destroyed or self.target_group == self.team:
                self.target = None
                self.target_group = None
                self.aiming = False

                

    def mark(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

    def draw_healthbar(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), (self.rect.centerx - 50, self.rect.centery - 61, self.shields *0.1, 3))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.centerx - 50, self.rect.centery - 58, self.hull* 0.1, 3))

    def draw(self, screen):
        if self.selected:
            self.create_waypoint(screen)
            self.mark(screen)

        self.draw_turrets(screen)
        screen.blit(self.image, self.rect)
        self.draw_healthbar(screen)
        

    def draw_turrets(self, screen):
        for turret in self.turrets:
            turret.draw(screen)

    def advance(self):
        dx = self.mouse[0]- self.rect.centerx
        dy = self.mouse[0]- self.rect.centery
        distance = math.sqrt(dx*dy + dy*dy)
        if distance > 15:
            vx = dx * 5 / distance 
            vy = dy * 5 / distance 
            self.rect.centerx += vx
            self.rect.centerx += vy


    def update(self, offset):
        self.rect.centerx = self.rect.centerx + offset[0]
        self.rect.centery = self.rect.centery - offset[1]
        self.waypoint_x = self.waypoint_x + offset[0]
        self.waypoint_y = self.waypoint_y - offset[1]
        self.animate()
        if self.selected:
            self.mouse_actions()
            
        for turret in self.turrets:
            turret.update(self.rect.center)
      
        if self.rotated:
            self.rotate(self.waypoint_x, self.waypoint_y)

        if self.move:            
            if self.rect.centerx < self.waypoint_x:
                self.rect.centerx += self.speed
            if self.rect.centerx > self.waypoint_x:
                self.rect.centerx -= self.speed
            if self.rect.centery < self.waypoint_y:
                self.rect.centery += self.speed
            if self.rect.centery > self.waypoint_y:
                self.rect.centery -= self.speed


            if self.waypoint_circle.collidepoint(self.rect.center):
                self.move = False
                self.rotated = False

            
        
        self.regenerate()
        self.check_death()

    def mouse_actions(self):
        rightclick = pygame.mouse.get_pressed() == (0, 0, 1)
        leftclick = pygame.mouse.get_pressed() == (0, 1, 0)
        if rightclick:
            self.move = False
            self.rotated = True
            self.waypoint_x = pygame.mouse.get_pos()[0]
            self.waypoint_y = pygame.mouse.get_pos()[1]
            
        if leftclick:
            self.mouse = pygame.mouse.get_pos()
            for turret in self.turrets:
                turret.shoot(self.mouse[0], self.mouse[1])

    def create_waypoint(self, screen):
        self.waypoint_circle = pygame.draw.circle(screen, (255, 255, 0), (self.waypoint_x,self.waypoint_y), 5)
        
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

#ship types  

class Carrier(Ship):
    def __init__(self, filename, team):
        super().__init__(filename, team)
        self.size = (150,150)
        self.turrets.add(Dualies(randint(self.rect.left,self.rect.right), randint(self.rect.top, self.rect.bottom)))
        self.speed = 2
        self.stored_fighters = 3
        self.name = "carrier"
        self.path = Settings.path_carrier
        for i in range(4):
            bitmap = pygame.image.load(os.path.join(
                Settings.path_carrier, f"carrier{i}.png"))
            scaled = pygame.transform.scale(bitmap,self.size)
            self.images.append(scaled)

class Assault(Ship):
    def __init__(self, filename, team):
        super().__init__(filename, team)
        self.size = (150,150)
        self.speed = 2
        self.turrets.add(Dualies(randint(self.rect.left,self.rect.right), randint(self.rect.top, self.rect.bottom)))
        self.turrets.add(Breacher(randint(self.rect.left,self.rect.right), randint(self.rect.top, self.rect.bottom)))
        self.range = 500
        self.name = "assault"
        self.path = Settings.path_assault
        for i in range(4):
            bitmap = pygame.image.load(os.path.join(
                Settings.path_assault, f"assault{i}.png"))
            scaled = pygame.transform.scale(bitmap,self.size)
            self.images.append(scaled)

    def speed_up(self):
        self.speed += 1

class Dreadnought(Ship):
    def __init__(self, filename, team):
        super().__init__(filename, team)
        self.size = (500, 1000)
        self.speed = 1
        self.turrets.add(Dualies(randint(self.rect.left,self.rect.right), randint(self.rect.top, self.rect.bottom)))
        self.turrets.add(Breacher(randint(self.rect.left,self.rect.right), randint(self.rect.top, self.rect.bottom)))
        self.range = 500
        self.hull = 10000
        self.shields = 10000
        self.name = "dreadnought"
        self.path = Settings.path_dreadnought
        self.images.clear()
        for i in range(3):
            bitmap = pygame.image.load(os.path.join(
                Settings.path_dreadnought, f"dreadnought{i}.png"))
            scaled = pygame.transform.scale(bitmap,self.size)
            self.images.append(scaled)