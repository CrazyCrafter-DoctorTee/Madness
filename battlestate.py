import pygame

import random
import time

import battle
import gamestate

class BattleState(gamestate.GameState):
    
    def __init__(self, screen, ioManager, fighter):
        self.screen = screen
        self.fighter = fighter
        self.ioManager = ioManager
        self.battleImages = ioManager.get_data('battles', 'images')
        self.battleImages[None] = self.battleImages.pop('plain')
        self.battleImages = self.create_images(self.battleImages)
        self.battle = battle.Battle(self.fighter)
        self.print_colors()
        self.keyMapping = {pygame.K_1 : 1,
                           pygame.K_2 : 2,
                           pygame.K_3 : 3,
                           pygame.K_4 : 4,
                           pygame.K_5 : 5}
        self.critterImgs = ioManager.get_data('critters')
    
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
        for i, pos in self.battle.get_battle_images():
            self.load_image(self.battleImages[i], pos)
        for i, pos in self.battle.get_creature_images():
            self.load_image(self.battleImages[i], pos)
        pygame.display.flip()
                