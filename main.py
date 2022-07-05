import shutil
import pygame
import os
from random import randint
from enemy import Enemy
from settings import Settings
from ships import Carrier, Assault, Dreadnought, Frigate
from starfighters import Starfighter
from camera import *
from menu import *
from gui import *
from logic import *
from minimap import *
from station import *
from facilitiy import *

class Background():
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_bg, filename)).convert()
        self.rect = self.image.get_rect()
        #animation
        self.images = []
        self.imageindex = 0
        self.clock_time = pygame.time.get_ticks()
        self.animation_time = 100
        self.images.append(self.image)

        for i in range(29):
             bitmap = pygame.image.load(os.path.join(
                 Settings.path_bg, f"bg{i+1}.png")).convert()
             self.images.append(bitmap)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, offset):
        self.animate()
        self.rect.centerx = self.rect.centerx + offset[0]
        self.rect.centery = self.rect.centery - offset[1]


    def animate(self):
        if pygame.time.get_ticks() > self.clock_time:
            self.clock_time = pygame.time.get_ticks() + self.animation_time
            self.imageindex += 1
            if self.imageindex >= len(self.images):
                self.imageindex = 0
            self.image = self.images[self.imageindex]

class Cursor():
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_ui, filename)).convert_alpha()
        #self.image = pygame.transform.scale(self.image, (Settings.player_size))
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        

class Game(object):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.screen_rect = (0,0,1920,1080)
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.clock_time = pygame.time.get_ticks()
        self.screen.fill((0, 0, 0))
        self.background = Background("bg1.png")
        self.ui = GUI()
        self.match = Match(1)
        self.ships = pygame.sprite.Group()
        self.cursor = Cursor("cursor.png")
        self.running = True
        self.selecting = False
        self.starting_point = (0, 0)
        self.dragpoint = (0, 0)
        self.recting = pygame.Rect(self.starting_point[0], self.starting_point[1], 0, 0)
        self.team1 = pygame.sprite.Group()
        self.team2 = pygame.sprite.Group()

        #enemy
        self.enemy = Enemy()
        
        #add 2 stations to the game
        self.stations = pygame.sprite.Group()
        self.stations.add(Spacestation("spacestation0.png", 1, 300, 300)) #team 1
        self.stations.add(Spacestation("spacestation0.png", 2, 2700, 2700)) #team 2
        self.ships.add(self.stations)

        #add mines to the game
        self.mines = pygame.sprite.Group()
        self.mines.add(Mine("mine1.png", 0, 1500, 1500, 2))
        self.ships.add(self.mines)        
        
        #camera setup
        pygame.event.set_grab(True)
        self.offset = (0, 0)

        #radar setup
        self.minimap_rect = pygame.Rect(40, self.screen.get_size()[1] -360, 320, 320)
        self.map_size = (self.screen.get_size()[0], self.screen.get_size()[1])

        #menu setup
        self.main_menu = True
        self.menus = Menu(self.screen)
        self.end = False



    def update_team(self):
        for mine in self.mines:
            if mine.team_changed == True:
                if mine.team == 1:
                    self.team1.add(mine)
                    self.ui.team1.additional_income = mine.income
                    self.team2.remove(mine)
                    self.ui.team2.additional_income = 0
                elif mine.team == 2:
                    self.team2.add(mine)
                    self.ui.team2.additional_income = mine.income    
                    self.team1.remove(mine)
                    self.ui.team1.additional_income = 0
                mine.team_changed = False

    def update_cursor(self):
        if self.ui.call_assault == True:
            self.cursor.image = pygame.image.load(os.path.join(Settings.path_assault, "assault0.png")).convert_alpha()
        elif self.ui.call_carrier == True:
            self.cursor.image = pygame.image.load(os.path.join(Settings.path_carrier, "carrier0.png")).convert_alpha()
        else:
            self.cursor.image = pygame.image.load(os.path.join(Settings.path_ui, "cursor.png")).convert_alpha()

        self.cursor.rect.center = pygame.mouse.get_pos()
        self.cursor.rect = self.cursor.image.get_rect(center = self.cursor.rect.center)


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

    def check_windowstate(self):
        if self.menus.main_menu == False:
            self.main_menu = False
        if self.menus.running == False:
            self.running = False

    def run(self):
        while self.running:
            self.clock.tick(60) 
            #print(self.clock.get_fps())    
            if self.main_menu == True:
                self.check_windowstate()
                self.menus.main()
            elif self.main_menu == False and self.end == False:      
                self.watch_for_events()
                self.update()
                self.draw()
            elif self.end == True and self.won == False:
                self.check_windowstate()
                self.menus.defeat()
            elif self.end == True and self.won == True:
                self.check_windowstate()
                self.menus.win()
        pygame.quit()       

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.ui.click = True
                self.select()
            else:
                self.ui.click = False

            if event.type == pygame.MOUSEMOTION:
                self.update_cursor()
                self.dragpoint = pygame.mouse.get_pos()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                        for ship in self.ships:
                            if ship.selected == True:
                                ship.selected = False
                            elif ship.selected == False:
                                ship.selected = True

                if event.key == pygame.K_ESCAPE:    
                    self.running = False
            elif event.type == pygame.QUIT:
                self.running = False

    def enemy_spawn(self):
        for st in self.stations:
            if st.team == 2:
                pos = st.rect.centerx + randint(-100,300), st.rect.centery + randint(-100,300)
        if self.enemy.spawn == True:
            if self.enemy.ship == 0:
                if self.enemy.eco.budget >= self.enemy.eco.frigate_cost:
                    self.ships.add(Frigate("frigate.png",2,pos))
                    self.enemy.eco.budget -= self.enemy.eco.frigate_cost
            elif self.enemy.ship == 1:
                if self.enemy.eco.budget >= self.enemy.eco.assault_cost:
                    self.ships.add(Assault("assault.png",2, pos))
                    self.enemy.eco.budget -= self.enemy.eco.assault_cost
            elif self.enemy.ship == 2:
                if self.enemy.eco.budget >= self.enemy.eco.carrier_cost:
                    self.ships.add(Carrier("carrier.png",2, pos))
                    self.enemy.eco.budget -= self.enemy.eco.carrier_cost
            self.pick_team()
            self.enemy.spawn == False

        if pygame.time.get_ticks() > self.clock_time:
            self.clock_time = pygame.time.get_ticks() + 2000
            for ship in self.team2:
                if ship not in self.stations:
                    if ship not in self.mines:
                        pos = pygame.math.Vector2(ship.rect.centerx, ship.rect.centery)
                        enemy = min([e for e in self.team1], key=lambda e: pos.distance_to(pygame.math.Vector2(e.rect.centerx, e.rect.centery)))

                        ship.waypoint_x = enemy.rect.centerx + ship.distance_x
                        ship.waypoint_y = enemy.rect.centery + ship.distance_y
                        ship.create_waypoint(self.screen)
                        ship.rotated = True
                        if ship.rotated == True and ship.move == True:
                            ship.move = False


    def spawn(self):
        self.mouse = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()
        if self.click[2] == 1:
            if self.ui.call_assault == True:
                    self.ships.add(Assault("assault.png",1,self.mouse))
                    self.ui.call_assault = False
                    self.ui.assault_count -= 1
            if self.ui.call_carrier == True:
                    self.ships.add(Carrier("carrier.png",1,self.mouse))
                    self.ui.call_carrier = False
                    self.ui.carrier_count -= 1
            if self.ui.call_dreadnought == True:
                    self.ships.add(Dreadnought("dreadnought.png",1, self.mouse))
                    self.ui.call_dreadnought = False
                    self.ui.dreadnought_count -= 1
            self.pick_team()

    def shoot_in_range(self):
        for ship in self.ships:
            ship.range_check(self.screen)

        for team1 in self.team1:
            for team2 in self.team2:
                team1.get_range(team2,self.team2)
                team2.get_range(team1,self.team1)

    def check_status(self):
        for station in self.stations:
            if station.destroyed == True and station.team == 1:
                self.won = False
                self.end = True
            elif station.destroyed == True and station.team == 2:
                self.won = True
                self.end = True

    def pick_team(self):
        for ship in self.ships:
            if ship.team == 1:
                self.team1.add(ship)
            else:
                self.team2.add(ship)
        
    def update(self):
        #print(self.clock.get_fps())
        self.enemy_spawn()
        self.enemy.update()
        self.update_team()
        self.check_status()
        self.spawn()
        self.background.update(self.offset)
        self.shoot_in_range()
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
        radar(self)
        pygame.display.update(self.screen_rect)

if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = "0, 0"
    game = Game()
    game.run()