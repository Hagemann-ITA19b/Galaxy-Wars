import pygame

class Economy():
    def __init__(self, team, population, income):
        self.team = team
        self.population = population
        self.income = income
        self.additional_income = 0
        self.budget = 0
        self.clock_time = pygame.time.get_ticks()
        self.level = 0

        #prices for ships
        self.corvette_cost = 100
        self.gunship_cost = 275
        self.frigate_cost = 350
        self.assault_cost = 500
        self.carrier_cost = 400
        self.dreadnought_cost = 600

    def check_level(self):
        if self.budget >= 100:
            self.level = 1
        if self.budget >= 275:
            self.level = 2
        if self.budget >= 350:
            self.level = 3
        if self.budget >= 400:
            self.level = 4
        if self.budget >= 500:
            self.level = 5
        if self.budget >= 600:
            self.level = 6

    def update(self):
        if pygame.time.get_ticks() > self.clock_time:
            self.clock_time = pygame.time.get_ticks() + 100
         
            self.budget += self.income + self.additional_income
            self.check_level()
        

