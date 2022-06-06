import pygame
import os
from random import randint
from Settings import Settings
from Ships import Carrier, Assault# Carrier # , Battleship, Cruiser, Submarine, Destroyer

class Background(pygame.sprite.Sprite):
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_ui, filename)).convert()
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        pass

class Cursor(pygame.sprite.Sprite):
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
        self.ships = pygame.sprite.Group()
        self.cursor = Cursor("cursor.png")
        self.running = True


    def select(self):
        if pygame.mouse.get_pressed() == (1, 0, 0):
            for ship in self.ships:
                if ship.rect.collidepoint(pygame.mouse.get_pos()):
                    ship.selected = True
                else:
                    ship.selected = False

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.ships.add(Carrier("carrier.png", 1))
                if event.key == pygame.K_a:
                    self.ships.add(Assault("assault.png",2))
                if event.key == pygame.K_ESCAPE:    
                    self.running = False
            elif event.type == pygame.QUIT:
                self.running = False

    def shot_in_range(self):
        self.team1 = pygame.sprite.Group()
        self.team2 = pygame.sprite.Group()
        self.teams = pygame.sprite.Group()
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
        
        for ships in self.team1:
            self.teams.add(ships)
        for ships in self.team2:
            self.teams.add(ships)
  


    def update(self):
        self.shot_in_range()
        self.cursor.update()
        for ships in self.teams:
            ships.update()
            

    def draw(self):
        self.background.draw(self.screen)
        self.cursor.draw(self.screen)
        for ships in self.teams:
            ships.draw(self.screen)

        pygame.display.flip()

if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = "0, 0"
    game = Game()
    game.run()