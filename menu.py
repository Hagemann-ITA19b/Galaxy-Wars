import pygame
import os
from settings import Settings



def main(self):
    mb = False
    self.screen.fill((0, 0, 0))
    mouse = pygame.mouse.get_pos()
    button1 = pygame.image.load(os.path.join(Settings.path_ui, "start_button.png")).convert_alpha()
    
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:    
                self.running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mb = True
            

    rect = button1.get_rect()
    
    if rect.collidepoint(mouse):
        button1 = pygame.transform.scale(button1, (200,200))
        #rect = button1.get_rect()
        if mb == True:
            self.main_menu = False

    print(rect)
 
    #print(self.clock.get_fps())
    self.screen.blit(button1,rect)
    pygame.display.flip()

    




