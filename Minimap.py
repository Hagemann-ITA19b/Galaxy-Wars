import pygame
def minimap(self):
    self.minimap_rect = pygame.Rect(self.screen.get_size()[0] - 200, 0, 200, 200)
    #draw a rect around the minimap
    pygame.draw.rect(self.screen, (255,255,255), (self.minimap_rect.left, self.minimap_rect.top, self.minimap_rect.width, self.minimap_rect.height), 1)
    
    #draw ships on the minimap
    for ship in self.ships:
        pygame.draw.circle(self.screen, (200,0,0),)

    