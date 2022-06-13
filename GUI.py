import pygame
import os
from Settings import Settings
class GUI():
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_ui, filename)).convert_alpha()
        self.rect = self.image.get_rect()


        self.buy_panel = pygame.image.load(os.path.join(Settings.path_ui, "buypanel.png")).convert_alpha()
        self.buy_panel_rect = self.buy_panel.get_rect()
        self.buy_panel_rect.center = (2100, 500)

        self.slider1 = pygame.image.load(os.path.join(Settings.path_ui, "slider.png")).convert_alpha()
        self.slider1_rect = self.slider1.get_rect()
        self.slider1_rect.center = (2100, 500)

        self.call_panel = pygame.image.load(os.path.join(Settings.path_ui, "callpanel.png")).convert_alpha()
        self.call_panel_rect = self.call_panel.get_rect()
        self.call_panel_rect.center = (0, 300)

        self.slider2 = pygame.image.load(os.path.join(Settings.path_ui, "slider.png")).convert_alpha()
        self.slider2_rect = self.slider2.get_rect()
        self.slider2_rect.center = (0, 300)

        self.slide_1 = False
        self.slide_2 = False

        self.click = False



    def update_pos(self):
        self.slider1_rect.centerx = self.buy_panel_rect.centerx - 200
        self.slider2_rect.centerx = self.call_panel_rect.centerx + 200

    def interaction(self):
        self.mouse = pygame.mouse.get_pos()
        # self.click = pygame.mouse.get_pressed()
        if self.click == True:
                if self.slider1_rect.collidepoint(self.mouse):
                    if self.buy_panel_rect.centerx == 1750:
                        self.slide_1 = False
                    else:
                        self.slide_1 = True
                if self.slider2_rect.collidepoint(self.mouse):
                    if self.call_panel_rect.centerx == 200:
                        self.slide_2 = False
                    else:
                        self.slide_2 = True


        if self.slide_1 == True:
                if self.buy_panel_rect.centerx > 1750:
                    self.buy_panel_rect.centerx = self.buy_panel_rect.centerx - 10
        else:
            if self.buy_panel_rect.centerx < 2100:
                self.buy_panel_rect.centerx = self.buy_panel_rect.centerx + 10


        if self.slide_2 == True:
                if self.call_panel_rect.centerx < 200:
                    self.call_panel_rect.centerx = self.call_panel_rect.centerx + 10
        else:
            if self.call_panel_rect.centerx > -200:
                self.call_panel_rect.centerx = self.call_panel_rect.centerx - 10


       
        






    def draw(self, screen):
        self.update_pos()
        self.interaction()
        screen.blit(self.image, self.rect)
        screen.blit(self.buy_panel, self.buy_panel_rect)
        screen.blit(self.slider1, self.slider1_rect)
        screen.blit(self.call_panel, self.call_panel_rect)
        screen.blit(self.slider2, self.slider2_rect)
 