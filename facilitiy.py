import pygame
from settings import Settings
import os
from turrets import *
from gui import *

class Mine(pygame.sprite.Sprite):
    def __init__(self, filename, team, x, y, income):
        super().__init__()
        self.size = (300,300)
        self.original_image = pygame.image.load(os.path.join(Settings.path_mine, filename)).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, self.size)
        self.image = self.original_image
        self.rect = self.image.get_rect() 
        self.rect.center = (x,y)
        self.selected = False
        self.team = team
        self.range = 500
        self.hull = 10000
        self.shields = 10000
        self.regeneration_rate = 1
        self.destroyed = False
        self.stored_fighters = 0
        self.waypoint_x = self.rect.centerx
        self.waypoint_y = self.rect.centery
        self.path = Settings.path_spacestation
        self.name = filename

        self.team1_progress = 0
        self.team2_progress = 0

        self.team_changed = False

        self.income = income

        #for animation
        self.images = []
        self.imageindex = 0
        self.clock_time = pygame.time.get_ticks()
        self.animation_time = 150

        for i in range(6):
            bitmap = pygame.image.load(os.path.join(
                Settings.path_mine, f"mine{i+1}.png"))
            scaled = pygame.transform.scale(bitmap,self.size)
            self.images.append(scaled)


        #check sprites
        self.appended_damaged = False

        #for spawning
        self.spawn_rect = pygame.Surface((500,500))  # the size of your rect
        self.spawn_rect.set_alpha(128)                # alpha level
        self.spawn_rect.fill((0,255,0))           # this fills the entire surface
        


    def update_sprite(self):
        pass


    def animate(self):
            if pygame.time.get_ticks() > self.clock_time:
                self.clock_time = pygame.time.get_ticks() + self.animation_time
                self.imageindex += 1
                self.image = self.original_image
                if self.imageindex >= len(self.images):
                    self.imageindex = 0
                self.original_image = self.images[self.imageindex]


    def range_check(self, screen):
        self.range_circle = pygame.draw.circle(screen, (255, 0, 0), self.rect.center, self.range)

    def warp_area(self, screen):
        screen.blit(self.spawn_rect, (self.rect.centerx - 250,self.rect.centery - 250))
        self.spawn_area = self.spawn_rect.get_rect(center = self.rect.center)

    def update_team(self):
        if self.team1_progress == 100:
            self.team = 1
        elif self.team2_progress == 100:
            self.team = 2

    def regenerate(self):
        if self.shields < 1000:
            self.shields += self.regeneration_rate

    def get_range(self, target, group):
        if self.range_circle.collidepoint(target.rect.center):
            if target.team != self.team and target.name == "conqueror":
                if target.team == 1:
                    self.team1_progress += 1
                    self.team2_progress -= 1
                if target.team == 2:
                    self.team2_progress += 1
                    self.team1_progress -= 1

                self.team_changed = True
            self.update_team()
        
        


    def mark(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

    def draw_healthbar(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), (self.rect.centerx - 50, self.rect.centery - 150, self.team1_progress, 20))
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.centerx - 50, self.rect.centery - 150, self.team2_progress, 20))

        pygame.draw.rect(screen, (0, 0, 255), (self.rect.centerx - 50, self.rect.centery - 61, self.shields *0.01, 3))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.centerx - 50, self.rect.centery - 58, self.hull* 0.01, 3))
       

    def update(self, offset):
        self.rect.centerx = self.rect.centerx + offset[0]
        self.rect.centery = self.rect.centery - offset[1]
        self.animate()

        self.regenerate()
        self.check_death()


    def shoot(self, target, target_group):
        pass


    def check_death(self):
        if self.hull <= 0:
            self.destroyed = True



    def draw(self, screen):
        if self.selected:
            self.mark(screen)

        screen.blit(self.image, self.rect)
        self.draw_healthbar(screen)