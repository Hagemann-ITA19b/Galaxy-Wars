import pygame
import os
from settings import Settings
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
        self.call_assault = False
        self.call_support = False
        self.call_carrier = False

        #count of the units
        self.assault_count = 0
        self.support_count = 0
        self.carrier_count = 0

        self.build_queue = []
        self.assault_time = 1000
        self.carrier_time = 500

        self.construction_time = 1000


    def animate(self,screen):
            if pygame.time.get_ticks() > self.clock_time:
                self.clock_time = pygame.time.get_ticks() + self.animation_time
                self.imageindex += 1
                if self.imageindex >= len(self.images):
                    self.imageindex = 0
                self.image = self.images[self.imageindex]
            screen.blit(self.image, self.rect)
        

    def panel_build(self, screen):
        Font = pygame.font.SysFont("comicsansms", 30)

        #for the build panel buttons
        build_assault = Font.render("assault", True, (0, 0, 0))
        build_assault_rect = build_assault.get_rect()
        build_assault_rect.center = (self.build_panel_rect.centerx, self.build_panel_rect.centery)

        build_carrier = Font.render("carrier", True, (0, 0, 0))
        build_carrier_rect = build_carrier.get_rect()
        build_carrier_rect.center = (self.build_panel_rect.centerx, self.build_panel_rect.centery + 50)


        #blit the buttons
        screen.blit(build_assault, build_assault_rect)
        screen.blit(build_carrier, build_carrier_rect)

        #logic for the buttons
        if build_assault_rect.collidepoint(self.mouse):
            build_assault = Font.render("assault", True, (255, 255, 255))
            screen.blit(build_assault, build_assault_rect)
            if self.click == True:
                self.build_queue.append("assault")
                self.click = False
        
        if build_carrier_rect.collidepoint(self.mouse):
            build_carrier = Font.render("carrier", True, (255, 255, 255))
            screen.blit(build_carrier, build_carrier_rect)
            if self.click == True:
                self.build_queue.append("carrier")
                self.click = False
                

        
        


    def panel_call(self, screen):
        Font = pygame.font.SysFont("comicsansms", 30)

        #for the call panel buttons
        assault = Font.render("Assault" + " " + str(self.assault_count)+"x", True, (0, 0, 0))
        assault_rect = assault.get_rect()
        assault_rect.center = (self.call_panel_rect.centerx, self.call_panel_rect.centery)

        carrier = Font.render("Carrier"+ " " + str(self.carrier_count)+"x", True, (0, 0, 0))
        carrier_rect = carrier.get_rect()
        carrier_rect.center = (self.call_panel_rect.centerx, self.call_panel_rect.centery + 50)

        #blit the buttons
        screen.blit(carrier, carrier_rect)
        screen.blit(assault, assault_rect)

        #logic for the buttons
        if assault_rect.collidepoint(self.mouse) and self.assault_count > 0:
            assault = Font.render("Assault", True, (255, 255, 255))
            screen.blit(assault, assault_rect)
            if self.click == True:
                self.call_assault = True
                self.call_carrier = False

        
        if carrier_rect.collidepoint(self.mouse) and self.carrier_count > 0:
            carrier = Font.render("Carrier", True, (255, 255, 255))
            screen.blit(carrier, carrier_rect)
            if self.click == True:
                self.call_carrier = True
                self.call_assault = False

    




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
            
            print(self.build_queue)
        else:
            self.constructing = False

        if self.constructing == True:
            if self.build_queue[0] == "assault":
                
                self.assault_time = self.assault_time - 1
                self.construction_time = self.assault_time
                if self.assault_time == 1:
                    self.assault_count += 1
                    self.build_queue.pop(0)
                    self.constructing = False
                    self.assault_time = 1000

            elif self.build_queue[0] == "carrier":
                self.carrier_time = self.carrier_time - 1
                self.construction_time = self.carrier_time
                if self.carrier_time == 0:
                    self.carrier_count += 1
                    self.build_queue.pop(0)
                    self.constructing = False
                    self.carrier_time = 500

    def calculate_multiplier(self):
        if self.build_queue[0] == "assault" and self.assault_time == 1000:
                self.construction_time = self.assault_time           
                self.multiplier = 1000 // self.construction_time
        elif self.build_queue[0] == "carrier" and self.carrier_time == 500:
                self.construction_time = self.carrier_time
                self.multiplier = 1000 // self.construction_time
                print(1000 // self.construction_time)
                print(self.multiplier)
                print("it works")

    def display_build_queue(self, screen):
        Font = pygame.font.SysFont("comicsansms", 30)
        assault = Font.render(str(self.build_queue), True, (255, 255, 255))
        screen.blit(assault, (20, Settings.window_height - 450))
        if self.constructing == True:
            
            print(self.multiplier)
            pygame.draw.rect(screen, (255,0,0), pygame.Rect(10, 700, self.construction_time * self.multiplier, 10))





    


       
        






    def draw(self, screen):
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
 