import pygame
import os
from random import randint
from Settings import Settings
from Ships import Carrier, Assault# Carrier # , Battleship, Cruiser, Submarine, Destroyer
from Starfighters import Starfighter
from Camera import *
from GUI import *
from Logic import *

class Background():
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_ui, filename)).convert()
        #self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))
        self.rect = self.image.get_rect()


    def draw(self, screen):
        screen.blit(self.image, self.rect)



    def update(self, offset):
    
        self.rect.centerx = self.rect.centerx + offset[0]
        self.rect.centery = self.rect.centery - offset[1]

class Cursor():
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_ui, filename)).convert_alpha()
        #self.image = pygame.transform.scale(self.image, (Settings.player_size))
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

class Game(object):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.screen.fill((0, 0, 0))
        self.background = Background("background.png")
        self.ui = GUI("ui.png")
        self.match = Match(1)
        self.ships = pygame.sprite.Group()
        self.cursor = Cursor("cursor.png")
        self.running = True
        self.selecting = False
        self.starting_point = (0, 0)
        self.dragpoint = (0, 0)
        self.recting = pygame.Rect(self.starting_point[0], self.starting_point[1], 0, 0)
        
        
        #camera setup
        pygame.event.set_grab(True)
        self.offset = (0, 0)

    def select(self):
        if pygame.mouse.get_pressed() == (1, 0, 0):
            for ship in self.ships:
                if ship.rect.collidepoint(pygame.mouse.get_pos()):
                    ship.selected = True
                else:
                    ship.selected = False

    def select_rect(self):
        if pygame.mouse.get_pressed() == (1, 0, 0):
            for ship in self.ships:
                if ship.rect.colliderect(self.recting):
                    ship.selected = True
            if self.selecting == False:
                self.starting_point = pygame.mouse.get_pos()
                self.selecting = True
            self.recting = pygame.draw.rect(self.screen, (255,225,100), pygame.Rect(self.starting_point[0], self.starting_point[1], 0 - (self.starting_point[0] - self.dragpoint[0]), 0 - (self.starting_point[1] - self.dragpoint[1])))
        else:
            self.selecting = False
            self.recting = pygame.Rect(0, 0, 0, 0)



    def run(self):
        while self.running:
            self.clock.tick(60)                         
            self.watch_for_events()
            self.update()
            self.draw()
        pygame.quit()       

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.select()
            if event.type == pygame.MOUSEMOTION:
                self.dragpoint = pygame.mouse.get_pos()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                        for ship in self.ships:
                            if ship.selected == True:
                                ship.selected = False
                            elif ship.selected == False:
                                ship.selected = True
                if event.key == pygame.K_SPACE:
                    self.ships.add(Carrier("carrier.png",self.match.player1))
                if event.key == pygame.K_p:
                    self.ships.add(Assault("assault.png",2))
                if event.key == pygame.K_ESCAPE:    
                    self.running = False
            elif event.type == pygame.QUIT:
                self.running = False

    def shoot_in_range(self):
        self.team1 = pygame.sprite.Group()
        self.team2 = pygame.sprite.Group()
        for ship in self.ships:
            if ship.team == 1:
                self.team1.add(ship)
            else:
                self.team2.add(ship)
        
        for team1 in self.team1:
            for team2 in self.team2:
                team1.range_check(self.screen)
                team2.range_check(self.screen)
                team1.get_range(team2,self.team2)
                team2.get_range(team1,self.team1)
        
    def update(self):
        self.background.update(self.offset)
        self.shoot_in_range()
        self.cursor.update()
        for ship in self.ships:
            ship.update(self.offset)
            if ship.stored_fighters > 0:
                self.ships.add(Starfighter("starfighter.png", ship.team))
                ship.stored_fighters -= 1
 
                
            

            

    def draw(self):
        mouse_control(self)
        self.screen.fill((0, 0, 0))
        self.background.draw(self.screen)
        
        for ships in self.ships:
            ships.draw(self.screen)
        

        self.select_rect()
        self.ui.draw(self.screen)
        self.cursor.draw(self.screen)
        pygame.display.flip()

if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = "0, 0"
    game = Game()
    game.run()