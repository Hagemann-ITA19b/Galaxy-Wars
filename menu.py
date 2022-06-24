import pygame
import os
from settings import Settings

class Menu():
    def __init__(self, screen):
        self.start_button = pygame.image.load(os.path.join(Settings.path_ui, "start_button.png")).convert_alpha()
        self.start_rect = self.start_button.get_rect()

        self.mouse = pygame.mouse.get_pos()
        self.mb = False

        self.screen = screen

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
        if self.start_rect.collidepoint(self.mouse):
            if self.mb == True:
                self.main_menu = False

        self.screen.blit(self.start_button,self.start_rect)
        pygame.display.flip()

    




