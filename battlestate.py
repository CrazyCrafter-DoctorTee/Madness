import pygame

import random
import time

import aifighter
import battle
import critter
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
        self.aiFighter = aifighter.AIFighter(self.generate_ai_critters())
        self.battle = battle.Battle(self.fighter, self.aiFighter, {'battle' : self.battleImgs, 'critter' : self.critterImgs})
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
        pass

    def get_creature_images(self):
        images, fonts = [], []
        images.append([self.critterImgs[self.battle.fighterCritters[0].name], (0.1, 0.35, 0, 0.25)])
        images.append([self.critterImgs[self.battle.fighterCritters[1].name], (0.1, 0.35, 0.27, 0.52)])
        images.append([self.critterImgs[self.battle.aifighterCritters[0].name], (0.65, 0.9, 0, 0.25)])
        images.append([self.critterImgs[self.battle.aifighterCritters[1].name], (0.65, 0.9, 0.27, 0.52)])
        fonts.append([str(self.battle.fighterCritters[0].currenthp), (0.05, 0.1, 0.1, 0.2)])
        fonts.append([str(self.battle.fighterCritters[1].currenthp), (0.05, 0.1, 0.37, 0.47)])
        fonts.append([str(self.battle.aifighterCritters[0].currenthp), (0.9, 0.95, 0.1, 0.2)])
        fonts.append([str(self.battle.aifighterCritters[1].currenthp), (0.9, 0.95, 0.37, 0.47)])
        return images, fonts    

    def get_target_images(self):
        images = []
        fonts = []
        images.append([self.battleImgs['targetbox'], (0.21, 0.36, 0.6, 0.75)])
        images.append([self.battleImgs['targetbox'], (0.21, 0.36, 0.77, 0.92)])
        if len(self.battle.actions) == 1:
            images.append([self.battleImgs['targetbox'], (0.04, 0.19, 0.77, 0.92)])
            fonts.append([self.fighter.critters[1].name, (0.05, 0.18, 0.82, 0.87)])
        else:
            images.append([self.battleImgs['targetbox'], (0.04, 0.19, 0.6, 0.75)])
            fonts.append([self.fighter.critters[0].name, (0.22, 0.35, 0.82, 0.87)])
        return images, fonts

    def get_move_images(self):
        images = []
        fonts = []
        x, y = 0.05, 0.8
        for name in self.battle.checkCritterMoves:
            images.append((self.battleImgs['redbox'], (x, x+0.15, y, y+0.11)))
            fonts.append((name, (x+0.01,x+0.14, y+0.01, y+0.1)))
            x += 0.17
        return images, fonts

    def draw(self):
        images, fonts = [[self.battleImgs['default'], (0, 1, 0, 1)]], []
        if self.battle.state == 'move':
            moveImgs, moveFonts = self.get_move_images()
            images.extend(moveImgs)
            fonts.extend(moveFonts)
        if self.battle.state == 'target':
            targetImgs, targetFonts = self.get_target_images()
            images.extend(targetImgs)
            fonts.extend(targetFonts)
        critterImgs, critterFonts = self.get_creature_images()
        images.extend(critterImgs)
        fonts.extend(critterFonts)
        for i, pos in images:
            print(i)
            self.load_image(i, pos)
        for i, pos in fonts:
            self.print_words(i, pos)
        pygame.display.flip()
        
    def generate_ai_critters(self):
        return [critter.Critter('doge', self.ioManager, 5),
                critter.Critter('doge', self.ioManager, 5)]
                