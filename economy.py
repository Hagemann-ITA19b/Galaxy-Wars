class Economy():
    def __init__(self, team, population, income):
        self.team = team
        self.population = population
        self.income = income
        self.additional_income = 0
        self.budget = 0


        #prices for ships
        self.assault_cost = 500
        self.carrier_cost = 400
        self.dreadnought_cost = 600

    def update(self):
        self.budget += self.income + self.additional_income
        print(self.additional_income, self.team)

