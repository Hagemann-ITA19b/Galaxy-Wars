import pygame
import os
from random import randint
from Settings import Settings
from Ships import Carrier# Carrier # , Battleship, Cruiser, Submarine, Destroyer

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
        self.carriers = pygame.sprite.Group()
        self.cursor = Cursor("cursor.png")
        self.running = True


    def select(self):
        if pygame.mouse.get_pressed() == (1, 0, 0):
            for carrier in self.carriers:
                if carrier.rect.collidepoint(pygame.mouse.get_pos()):
                    carrier.selected = True
                else:
                    carrier.selected = False

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
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.carriers.add(Carrier("carrier.png"))
                if event.key == pygame.K_ESCAPE:    
                    self.running = False
            elif event.type == pygame.QUIT:
                self.running = False


    def update(self):
        self.carriers.update()
        self.cursor.update()
        self.select()
        for carrier in self.carriers:
            carrier.get_slots()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.cursor.draw(self.screen)
        self.carriers.draw(self.screen)
        for carrier in self.carriers:
            carrier.draw_turrets(self.screen)
            carrier.mark(self.screen)
        pygame.display.flip()

if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = "0, 0"
    game = Game()
    game.run()