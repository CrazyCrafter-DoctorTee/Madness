import pygame

import random
import time

import battle
import gamestate

class BattleState(gamestate.GameState):
    
    def __init__(self, screen, screenDims, ioManager, fighter):
        self.screen = screen
        self.screenDims = screenDims
        self.fighter = fighter
        self.ioManager = ioManager
        self.battleImgs = ioManager.get_data('battles', 'images')
        self.battleImgs[None] = self.battleImgs['done']
        self.battleImgs = self.create_images(self.battleImgs)
        self.critterImgs = self.create_images(ioManager.get_data('critters', 'images'))
        self.battle = battle.Battle(self.fighter, {'battle' : self.battleImgs, 'critter' : self.critterImgs})
        self.print_colors()
        self.keyMapping = {pygame.K_1 : 1,
                           pygame.K_2 : 2,
                           pygame.K_3 : 3,
                           pygame.K_4 : 4,
                           pygame.K_5 : 5}
    
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
                if event.key in self.keyMapping:
                    self.battle.stateActions[self.battle.state](self.keyMapping[event.key])
        return 'battle'
        
    def make_actions(self):
        self.battle.run()
    
    def draw(self):
        images, fonts = self.battle.stateDrawings[self.battle.state]()
        for i, pos in images:
            self.load_image(i, pos)
        for i, pos in fonts:
            self.print_words(i, pos)
        pygame.display.flip()
                