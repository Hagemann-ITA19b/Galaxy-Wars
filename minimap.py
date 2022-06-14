import pygame
def radar(self):
    #draw ships on the minimap without moving them 1:100
    for ship in self.ships:
        if self.minimap_rect.left + ship.rect.center[0] * (self.minimap_rect.width / self.map_size[0]) < self.minimap_rect.right and self.minimap_rect.left + ship.rect.center[0] * (self.minimap_rect.width / self.map_size[0]) > self.minimap_rect.left and self.minimap_rect.top + ship.rect.center[1] * (self.minimap_rect.height / self.map_size[1]) < self.minimap_rect.bottom and self.minimap_rect.top + ship.rect.center[1] * (self.minimap_rect.height / self.map_size[1]) > self.minimap_rect.top:
            pygame.draw.circle(self.screen, (0,0,255), (self.minimap_rect.left + (ship.rect.center[0] * (self.minimap_rect.width / self.map_size[0])), self.minimap_rect.top + (ship.rect.center[1] * (self.minimap_rect.height / self.map_size[1]))), 7)



    #draw selected ships on the minimap
    for ship in self.ships:
        if ship.selected == True:
            pygame.draw.circle(self.screen, (255,0,255), (self.minimap_rect.left + (ship.rect.center[0] * (self.minimap_rect.width / self.map_size[0])), self.minimap_rect.top + (ship.rect.center[1] * (self.minimap_rect.height / self.map_size[1]))), 6)
    