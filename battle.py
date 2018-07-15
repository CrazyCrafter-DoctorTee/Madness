import pygame

import aifighter

class Battle(object):
    
    def __init__(self, fighter):
        self.figher = fighter
        self.aifigher = aifighter.AIFighter()
        
    def key_down(self, key):
        if key == pygame.K_1:
            self.use_move(1)
        elif key == pygame.K_2:
            self.use_move(2)
        elif key == pygame.K_3:
            self.use_move(3)
        elif key == pygame.K_4:
            self.use_move(4)
            
    def use_move(self, moveNum):
        pass