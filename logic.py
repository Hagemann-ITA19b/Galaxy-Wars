import pygame


def build_ship(self):
    self.build_queue = []
    if len(self.build_queue) > 0:
        self.build_queue[0]
        self.constructing = True

    if self.constructing == True:
        if self.build_queue[0] == "assault":
            self.construct_time = pygame.time.get_ticks() + self.assault_time
            print(self.construct_time)


    



class Match():
    def __init__(self, player1):
        self.player1 = player1
