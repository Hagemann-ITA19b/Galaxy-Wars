import pygame
import os
from Settings import Settings
class GUI():
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_ui, filename)).convert_alpha()
        self.buy_panel = pygame.image.load(os.path.join(Settings.path_ui, "buy_panel.png")).convert_alpha()
        self.buy_panel_rect = self.buy_panel.get_rect()
        self.buy_panel_rect.center = (2100, 500)
        self.slider1 = pygame.image.load(os.path.join(Settings.path_ui, "slider.png")).convert_alpha()
        self.slider1_rect = self.slider1.get_rect()
        self.slider1_rect.center = (2100, 500)
        self.rect = self.image.get_rect()



    def update_pos(self):
        self.slider1_rect.centerx = self.buy_panel_rect.centerx - 200
        self.slider1_rect.centery = self.buy_panel_rect.centery


    def interaction(self):
        self.mouse = pygame.mouse.get_pos()
        if self.slider1_rect.collidepoint(self.mouse):
            self.buy_panel_rect.centerx -= 11
        






    def draw(self, screen):
        self.update_pos()
        self.interaction()
        screen.blit(self.image, self.rect)
        screen.blit(self.buy_panel, self.buy_panel_rect)
        screen.blit(self.slider1, self.slider1_rect)
 