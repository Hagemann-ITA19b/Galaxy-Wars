import pygame
import os
from settings import Settings

class Menu():
    def __init__(self, screen):
        self.start_button = pygame.image.load(os.path.join(Settings.path_ui, "start_button.png")).convert_alpha()
        self.start_rect = self.start_button.get_rect()
        self.start_rect.center = Settings.window_width / 2, Settings.window_height / 2

        self.mouse = pygame.mouse.get_pos()
        self.mb = False

        self.screen = screen
        self.running = True
        self.main_menu = True

        self.pixelfont = pygame.font.Font(os.path.join(Settings.path_font, "ChillPixels-Matrix.otf"), 72)

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

    def main(self):
        self.watch_for_events()
        self.screen.fill((0, 0, 0))
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
        pygame.display.flip()

    




