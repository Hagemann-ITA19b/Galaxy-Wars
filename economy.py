class Economy():
    def __init__(self, team, population, income):
        self.team = team
        self.population = population
        self.income = income
        self.budget = 0

        #prices for ships
        self.assault_cost = 500
        self.carrier_cost = 400

    def update(self):
        self.budget += self.income

