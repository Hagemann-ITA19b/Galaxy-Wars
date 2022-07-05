from asyncio import QueueEmpty
import pygame
import os
from settings import Settings
from economy import Economy
from ships import Carrier, Assault

class GUI():
    def __init__(self) -> None:
        super().__init__()
        ##ui radar image
        self.image = pygame.image.load(os.path.join(Settings.path_ui_radar, "radar0.png"))
        #for animation
        self.images = []
        self.imageindex = 0
        self.clock_time = pygame.time.get_ticks()
        self.animation_time = 100
        self.images.append(self.image)
        for i in range(29):
             bitmap = pygame.image.load(os.path.join(
                 Settings.path_ui_radar, f"radar{i}.png"))
             self.images.append(bitmap)

        self.rect = pygame.Rect(0, 1080 -400, 400, 400)

        self.build_panel = pygame.image.load(os.path.join(Settings.path_ui, "buildpanel.png")).convert_alpha()
        self.build_panel_rect = self.build_panel.get_rect()
        self.build_panel_rect.center = (2100, 500)

        self.slider1 = pygame.image.load(os.path.join(Settings.path_ui, "slider.png")).convert_alpha()
        self.slider1_rect = self.slider1.get_rect()
        self.slider1_rect.center = (self.build_panel_rect.centerx - 180, 500)

        self.call_panel = pygame.image.load(os.path.join(Settings.path_ui, "callpanel.png")).convert_alpha()
        self.call_panel_rect = self.call_panel.get_rect()
        self.call_panel_rect.center = (0, 300)

        self.slider2 = pygame.image.load(os.path.join(Settings.path_ui, "slider.png")).convert_alpha()
        self.slider2_rect = self.slider2.get_rect()
        self.slider2_rect.center = (self.call_panel_rect.centerx + 180, 300)

        self.slide_1 = False
        self.slide_2 = False

        self.click = False

        #for the call panel
        self.call_conqueror = False
        self.call_frigate = False
        self.call_assault = False
        self.call_support = False
        self.call_carrier = False
        self.call_dreadnought = False

        #count of the units
        self.conqueror_count = 0
        self.assault_count = 0
        self.frigate_count = 0
        self.carrier_count = 0
        self.dreadnought_count = 0

        self.build_queue = []
        self.conqueror_time = 350
        self.assault_time = 1000
        self.carrier_time = 500
        self.frigate_time = 350
        self.dreadnought_time = 1000
        self.construction_time = 1000
        self.multiplier = 1000 // self.construction_time

        #finace
        self.team1 = Economy(1, 50, 1)

        #font
        self.font = pygame.font.Font(os.path.join(Settings.path_font, "ChillPixels-Matrix.otf"), 30)

    def animate(self,screen):
            if pygame.time.get_ticks() > self.clock_time:
                self.clock_time = pygame.time.get_ticks() + self.animation_time
                self.imageindex += 1
                if self.imageindex >= len(self.images):
                    self.imageindex = 0
                self.image = self.images[self.imageindex]
            screen.blit(self.image, self.rect)
        

    def panel_build(self, screen):
        #for the build panel buttons
        build_conqueror = self.font.render("Conqueror" + " " +str(self.team1.conqueror_cost)+"$", True, (0, 0, 0))
        build_conqueror_rect = build_conqueror.get_rect()
        build_conqueror_rect.center = (self.build_panel_rect.centerx, self.build_panel_rect.centery - 50)

        build_assault = self.font.render("Assault" + " " +str(self.team1.assault_cost)+"$", True, (0, 0, 0))
        build_assault_rect = build_assault.get_rect()
        build_assault_rect.center = (self.build_panel_rect.centerx, self.build_panel_rect.centery + 100)

        build_carrier = self.font.render("Carrier" + " " + str(self.team1.carrier_cost)+"$", True, (0, 0, 0))
        build_carrier_rect = build_carrier.get_rect()
        build_carrier_rect.center = (self.build_panel_rect.centerx, self.build_panel_rect.centery + 50)

        build_dreadnought = self.font.render("Dreadnought" + " " + str(self.team1.dreadnought_cost)+"$", True, (0, 0, 0))
        build_dreadnought_rect = build_dreadnought.get_rect()
        build_dreadnought_rect.center = (self.build_panel_rect.centerx, self.build_panel_rect.centery + 150)

        build_frigate = self.font.render("Frigate" + " " + str(self.team1.frigate_cost) + "$", True, (0,0,0))
        build_frigate_rect = build_frigate.get_rect()
        build_frigate_rect.center = (self.build_panel_rect.centerx, self.build_panel_rect.centery)

        #blit the buttons
        screen.blit(build_conqueror, build_conqueror_rect)
        screen.blit(build_frigate, build_frigate_rect)
        screen.blit(build_assault, build_assault_rect)
        screen.blit(build_carrier, build_carrier_rect)
        screen.blit(build_dreadnought, build_dreadnought_rect)

        #logic for the buttons
        if build_conqueror_rect.collidepoint(self.mouse):
            build_conqueror = self.font.render("Conqueror" + " " + str(self.team1.conqueror_cost)+ "$", True, (255, 255, 255))
            screen.blit(build_conqueror, build_conqueror_rect)
            if self.click == True and self.team1.budget > self.team1.conqueror_cost:
                if len(self.build_queue) < 5:
                    self.queue_full = False
                    self.build_queue.append("Conqueror")
                    self.team1.budget -= self.team1.conqueror_cost
                else:
                    self.queue_full = True
                self.click = False

        if build_frigate_rect.collidepoint(self.mouse):
            build_frigate = self.font.render("Frigate" + " " + str(self.team1.frigate_cost)+ "$", True, (255, 255, 255))
            screen.blit(build_frigate, build_frigate_rect)
            if self.click == True and self.team1.budget > self.team1.frigate_cost:
                if len(self.build_queue) < 5:
                    self.queue_full = False
                    self.build_queue.append("Frigate")
                    self.team1.budget -= self.team1.frigate_cost
                else:
                    self.queue_full = True
                self.click = False

        if build_assault_rect.collidepoint(self.mouse):
            build_assault = self.font.render("Assault" + " " + str(self.team1.assault_cost)+ "$", True, (255, 255, 255))
            screen.blit(build_assault, build_assault_rect)
            if self.click == True and self.team1.budget > self.team1.assault_cost:
                if len(self.build_queue) < 5:
                    self.queue_full = False
                    self.build_queue.append("Assault")
                    self.team1.budget -= self.team1.assault_cost
                else:
                    self.queue_full = True
                self.click = False
        
        if build_carrier_rect.collidepoint(self.mouse):
            build_carrier = self.font.render("Carrier" + " " + str(self.team1.carrier_cost) + "$", True, (255, 255, 255))
            screen.blit(build_carrier, build_carrier_rect)
            if self.click == True and self.team1.budget > self.team1.carrier_cost:
                if len(self.build_queue) < 5:
                    self.queue_full = False
                    self.build_queue.append("Carrier")
                    self.team1.budget -= self.team1.carrier_cost
                else:
                    self.queue_full = True
                self.click = False

        if build_dreadnought_rect.collidepoint(self.mouse):
            build_dreadnought = self.font.render("Dreadnought" + " " + str(self.team1.dreadnought_cost) + "$", True, (255, 255, 255))
            screen.blit(build_dreadnought, build_dreadnought_rect)
            if self.click == True and self.team1.budget > self.team1.dreadnought_cost:
                if len(self.build_queue) < 5:
                    self.queue_full = False
                    self.build_queue.append("Dreadnought")
                    self.team1.budget -= self.team1.dreadnought_cost
                else:
                    self.queue_full = True
                self.click = False

                
    def panel_call(self, screen):
        #for the call panel buttons
        conqueror = self.font.render("Conqueror" + " " + str(self.conqueror_count)+"x", True, (0, 0, 0))
        conqueror_rect = conqueror.get_rect()
        conqueror_rect.center = (self.call_panel_rect.centerx, self.call_panel_rect.centery - 100)

        frigate = self.font.render("Frigate" + " " + str(self.frigate_count)+"x", True, (0, 0, 0))
        frigate_rect = frigate.get_rect()
        frigate_rect.center = (self.call_panel_rect.centerx, self.call_panel_rect.centery - 50)

        assault = self.font.render("Assault" + " " + str(self.assault_count)+"x", True, (0, 0, 0))
        assault_rect = assault.get_rect()
        assault_rect.center = (self.call_panel_rect.centerx, self.call_panel_rect.centery)

        carrier = self.font.render("Carrier"+ " " + str(self.carrier_count)+"x", True, (0, 0, 0))
        carrier_rect = carrier.get_rect()
        carrier_rect.center = (self.call_panel_rect.centerx, self.call_panel_rect.centery + 50)

        dreadnought = self.font.render("Dreadnought" + " " + str(self.dreadnought_count)+"x", True, (0, 0, 0))
        dreadnought_rect = dreadnought.get_rect()
        dreadnought_rect.center = (self.call_panel_rect.centerx, self.call_panel_rect.centery + 100)

        #blit the buttons
        screen.blit(conqueror, conqueror_rect)
        screen.blit(frigate, frigate_rect)
        screen.blit(carrier, carrier_rect)
        screen.blit(assault, assault_rect)
        screen.blit(dreadnought, dreadnought_rect)

        #logic for the buttons
        if conqueror_rect.collidepoint(self.mouse) and self.conqueror_count > 0:
            conqueror = self.font.render("Conqueror", True, (255, 255, 255))
            screen.blit(conqueror, conqueror_rect)
            if self.click == True:
                self.call_conqueror = True
                self.call_frigate = False
                self.call_assault = False
                self.call_carrier = False
                self.call_dreadnought = False

        if frigate_rect.collidepoint(self.mouse) and self.frigate_count > 0:
            frigate = self.font.render("Frigate", True, (255, 255, 255))
            screen.blit(frigate, frigate_rect)
            if self.click == True:
                self.call_frigate = True
                self.call_assault = False
                self.call_carrier = False
                self.call_dreadnought = False
                self.call_conqueror = False

        if assault_rect.collidepoint(self.mouse) and self.assault_count > 0:
            assault = self.font.render("Assault", True, (255, 255, 255))
            screen.blit(assault, assault_rect)
            if self.click == True:
                self.call_assault = True
                self.call_carrier = False
                self.call_dreadnought = False
                self.call_frigate = False
                self.call_conqueror = False

        
        if carrier_rect.collidepoint(self.mouse) and self.carrier_count > 0:
            carrier = self.font.render("Carrier", True, (255, 255, 255))
            screen.blit(carrier, carrier_rect)
            if self.click == True:
                self.call_carrier = True
                self.call_assault = False
                self.call_dreadnought = False
                self.call_frigate = False
                self.call_conqueror = False

        if dreadnought_rect.collidepoint(self.mouse) and self.dreadnought_count > 0:
            dreadnought = self.font.render("Dreadnought", True, (255, 255, 255))
            screen.blit(dreadnought, dreadnought_rect)
            if self.click == True:
                self.call_dreadnought = True
                self.call_carrier = False
                self.call_assault = False
                self.call_frigate = False
                self.call_conqueror = False

    def update_pos(self):
        self.slider1_rect.centerx = self.build_panel_rect.centerx - 180
        self.slider2_rect.centerx = self.call_panel_rect.centerx + 180

    def interaction(self):
        self.mouse = pygame.mouse.get_pos()
        # self.click = pygame.mouse.get_pressed()
        if self.click == True:
                if self.slider1_rect.collidepoint(self.mouse):
                    self.click = False
                    if self.build_panel_rect.centerx == 1750:
                        self.slide_1 = False
                    else:
                        self.slide_1 = True
                if self.slider2_rect.collidepoint(self.mouse):
                    self.click = False
                    if self.call_panel_rect.centerx == 200:
                        self.slide_2 = False
                    else:
                        self.slide_2 = True

        if self.slide_1 == True:
                if self.build_panel_rect.centerx > 1750:
                    self.build_panel_rect.centerx = self.build_panel_rect.centerx - 10
        else:
            if self.build_panel_rect.centerx < 2100:
                self.build_panel_rect.centerx = self.build_panel_rect.centerx + 10


        if self.slide_2 == True:
                if self.call_panel_rect.centerx < 200:
                    self.call_panel_rect.centerx = self.call_panel_rect.centerx + 10
        else:
            if self.call_panel_rect.centerx > -180:
                self.call_panel_rect.centerx = self.call_panel_rect.centerx - 10


    def build_ship(self):
        if len(self.build_queue) > 0:
            self.calculate_multiplier()
            self.constructing = True
        else:
            self.constructing = False

        if self.constructing == True:

            if self.build_queue[0] == "Dreadnought":
                self.dreadnought_time = self.dreadnought_time - 1
                self.construction_time = self.dreadnought_time
                if self.dreadnought_time == 1:
                    self.dreadnought_count += 1
                    self.build_queue.pop(0)
                    self.constructing = False
                    self.dreadnought_time = 1000

            elif self.build_queue[0] == "Assault":
                self.assault_time = self.assault_time - 1
                self.construction_time = self.assault_time
                if self.assault_time == 1:
                    self.assault_count += 1
                    self.build_queue.pop(0)
                    self.constructing = False
                    self.assault_time = 1000

            elif self.build_queue[0] == "Carrier":
                self.carrier_time = self.carrier_time - 1
                self.construction_time = self.carrier_time
                if self.carrier_time == 0:
                    self.carrier_count += 1
                    self.build_queue.pop(0)
                    self.constructing = False
                    self.carrier_time = 500

            elif self.build_queue[0] == "Frigate":
                self.frigate_time = self.frigate_time - 1
                self.construction_time = self.frigate_time
                if self.frigate_time == 0:
                    self.frigate_count += 1
                    self.build_queue.pop(0)
                    self.constructing = False
                    self.frigate_time = 500

            elif self.build_queue[0] == "Conqueror":
                self.conqueror_time = self.conqueror_time - 1
                self.construction_time = self.conqueror_time
                if self.conqueror_time == 0:
                    self.conqueror_count += 1
                    self.build_queue.pop(0)
                    self.constructing = False
                    self.conqueror_time = 500

                    
    def calculate_multiplier(self):
        if self.build_queue[0] == "Assault" and self.assault_time == 1000:
                self.construction_time = self.assault_time           
                self.multiplier = 1000 // self.construction_time
        elif self.build_queue[0] == "Carrier" and self.carrier_time == 500:
                self.construction_time = self.carrier_time
                self.multiplier = 1000 // self.construction_time
        elif self.build_queue[0] == "Dreadnought" and self.dreadnought_time == 1000:
                self.construction_time = self.dreadnought_time
                self.multiplier = 1000 // self.construction_time
        elif self.build_queue[0] == "Frigate" and self.frigate_time == 1000:
                self.construction_time = self.frigate_time
                self.multiplier = 1000 // self.construction_time
        elif self.build_queue[0] == "Conqueror" and self.conqueror_time == 1000:
                self.construction_time = self.conqueror_time
                self.multiplier = 1000 // self.construction_time
        



    def display_build_queue(self, screen):
        if self.constructing == True:
            queue = self.font.render(str(self.build_queue), True, (255, 255, 255))
            screen.blit(queue, (20, Settings.window_height - 450))
            pygame.draw.rect(screen, (255,0,0), pygame.Rect(10, 700, self.construction_time * self.multiplier, 10))

            if self.queue_full == True:
                queue_full = self.font.render("Queue is full", True, (255, 100, 0))
                screen.blit(queue_full, (900, Settings.window_height - 450))
                if len(self.build_queue) < 5:
                    self.queue_full = False

    def display_budget(self, screen):
        budget = self.font.render("Budget: " + str(self.team1.budget), True, (0, 255, 255))
        screen.blit(budget, (20, Settings.window_height - 600))


    def draw(self, screen):
        self.team1.update()
        self.build_ship()
        self.animate(screen)
        self.update_pos()
        self.interaction()
        
        screen.blit(self.build_panel, self.build_panel_rect)
        screen.blit(self.slider1, self.slider1_rect)
        screen.blit(self.call_panel, self.call_panel_rect)
        screen.blit(self.slider2, self.slider2_rect)
        self.panel_call(screen)
        self.panel_build(screen)
        self.display_build_queue(screen)
        self.display_budget(screen)
 