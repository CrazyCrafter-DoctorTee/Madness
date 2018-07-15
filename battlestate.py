import pygame

import random
import time

import battle
import gamestate

class BattleState(gamestate.GameState):
    
    def __init__(self, screen, ioManger, fighter):
        self.screen = screen
        self.fighter = fighter
        self.ioManager = ioManager
        self.battle = battle.Battle()
        self.print_colors()
    
    def print_colors(self):
        stime = time.time()
        lastChange = 0
        last_color = [0, 0, 0]
        while time.time() < stime + 2:
            if time.time() > lastChange + 0.2:
                i = random.randrange(0,2)
                last_color[i] = (last_color[i] + 99) % 256
                self.screen.fill(last_color)
                pygame.display.flip()
                lastChange = time.time()
                
    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    return 'map'
                self.battle.key_down(event.key)
        return 'battle'
        
    def make_actions(self):
        self.battle.run()
    
    def draw(self):
        self.load_image(self.battle.background, (0, 0))
        for name, location in self.battle.get_locations():
            self.load_image(self.critterImages[name], location)
    
                