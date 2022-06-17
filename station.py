import pygame
from settings import Settings
import os

class Spacestation(pygame.sprite.Sprite):
    def __init__(self, filename, team, x, y):
        super().__init__()
        self.size = (500,500)
        self.original_image = pygame.image.load(os.path.join(Settings.path_spacestation, filename)).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, self.size)
        self.image = self.original_image
        self.rect = self.image.get_rect() 
        self.rect.center = (x,y)
        self.selected = False
        self.turrets = pygame.sprite.Group()
        self.team = team
        self.range = 500
        self.aiming = False
        self.hull = 10000
        self.shields = 10000
        self.regeneration_rate = 1
        self.destroyed = False
        self.stored_fighters = 0
        self.waypoint_x = self.rect.centerx
        self.waypoint_y = self.rect.centery
        self.path = Settings.path_spacestation
        self.name = filename

        #for animation
        self.images = []
        self.imageindex = 0
        self.clock_time = pygame.time.get_ticks()
        self.animation_time = 80
        self.images.append(self.original_image)

        for i in range(20):
            bitmap = pygame.image.load(os.path.join(
                Settings.path_spacestation, f"spacestation{i}.png"))
            scaled = pygame.transform.scale(bitmap,self.size)
            self.images.append(scaled)

        #check sprites
        self.appended_damaged = False


    def update_sprite(self):
        pass
        # if self.appended_damaged == False:
        #     if self.hull < 800:
        #         self.appended_damaged = True
        #         self.images.clear()
        #         for i in range(4):
        #             bitmap = pygame.image.load(os.path.join(
        #                 self.path, self.name+f"_damaged{i}.png"))
        #             scaled = pygame.transform.scale(bitmap,self.size)
        #             self.images.append(scaled)


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
            if not self.range_circle.collidepoint(self.target.rect.center) or self.target.destroyed:
                self.target = None
                self.target_group = None
                self.aiming = False

                

    def mark(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

    def draw_healthbar(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), (self.rect.centerx - 50, self.rect.centery - 61, self.shields *0.01, 3))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.centerx - 50, self.rect.centery - 58, self.hull* 0.01, 3))


    def update(self, offset):
        self.rect.centerx = self.rect.centerx + offset[0]
        self.rect.centery = self.rect.centery - offset[1]
        self.animate()

        for turret in self.turrets:
            turret.update(self.rect.center)

        self.regenerate()
        self.check_death()


    def shoot(self, target, target_group):
        for turret in self.turrets:
            turret.shoot(target, target_group)


    def check_death(self):
        if self.hull <= 0:
            self.destroyed = True

    def draw_turrets(self, screen):
        for turret in self.turrets:
            turret.draw(screen)

    def draw(self, screen):
        if self.selected:
            self.mark(screen)

        self.draw_turrets(screen)
        screen.blit(self.image, self.rect)
        self.draw_healthbar(screen)