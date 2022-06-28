import pygame
import os
from settings import Settings

class Star():
    def __init__(self, name, x, y):
        self.image = pygame.image.load(os.path.join(Settings.path_bg, name +"1.png")).convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.centery = y

        #animation
        self.images = []
        self.imageindex = 0
        self.clock_time = pygame.time.get_ticks()
        self.animation_time = 100
        self.images.append(self.image)

        for i in range(49):
             bitmap = pygame.image.load(os.path.join(
                 Settings.path_bg, name + f"{i+1}.png"))
             self.images.append(bitmap)

    def animate(self,screen):
        if pygame.time.get_ticks() > self.clock_time:
            self.clock_time = pygame.time.get_ticks() + self.animation_time
            self.imageindex += 1
            if self.imageindex >= len(self.images):
                self.imageindex = 0
            self.image = self.images[self.imageindex]
        screen.blit(self.image, self.rect)


class Menu():
    def __init__(self, screen):
        self.start_button = pygame.image.load(os.path.join(Settings.path_ui, "start_button.png")).convert_alpha()
        self.start_rect = self.start_button.get_rect()
        self.start_rect.center = Settings.window_width / 2, Settings.window_height / 2

        self.dust = pygame.image.load(os.path.join(Settings.path_bg, "dust.png")).convert_alpha()
        self.dust_rect = self.dust.get_rect()

        self.nebula = pygame.image.load(os.path.join(Settings.path_bg, "nebula.png")).convert_alpha()
        self.nebula_rect = self.nebula.get_rect()

        self.mouse = pygame.mouse.get_pos()
        self.mb = False

        self.screen = screen
        self.running = True
        self.main_menu = True

        self.pixelfont = pygame.font.Font(os.path.join(Settings.path_font, "ChillPixels-Matrix.otf"), 72)

        #self.bg = pygame.image.load(os.path.join(Settings.path_ui, "main.png")).convert_alpha()
        #self.bg_rect = self.bg.get_rect()

        self.star1 = Star("galaxy", 1500, 200)



    def watch_for_events(self):
        self.mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:    
                    self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mb = True
            else:
                self.mb = False

    def updown(self):
         #self.dust_rect.centery <



            self.dust_rect.centery += 1
 

    def main(self):
        self.updown()
        self.watch_for_events()
        #self.screen.blit(self.bg,self.bg_rect)
        self.screen.fill((0,0,0))
        self.screen.blit(self.dust, self.dust_rect)
        self.screen.blit(self.nebula, self.nebula_rect)
        
        title = self.pixelfont.render("Galaxy Wars", True, (0, 0, 255))
        title_rect = title.get_rect()
        title_rect.center = (Settings.window_width / 2, (Settings.window_height / 2) - 100)
        self.screen.blit(title, title_rect)


        if self.start_rect.collidepoint(self.mouse):
            self.start_button = pygame.image.load(os.path.join(Settings.path_ui, "start_button_hover.png")).convert_alpha()
            if self.mb == True:
                self.main_menu = False
        else:
            self.start_button = pygame.image.load(os.path.join(Settings.path_ui, "start_button.png")).convert_alpha()

        self.screen.blit(self.start_button,self.start_rect)
        self.star1.animate(self.screen)
        pygame.display.flip()

    




