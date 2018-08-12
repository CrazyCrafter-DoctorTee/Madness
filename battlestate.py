import pygame

import random
import time

import aifighter
import battle
import critter
import gamestate

'''
stepFuncs function error codes:
    0: don't change step
    1: go to next step
    2: player won
    3: player lost
    4: tie
'''

class BattleState(gamestate.GameState):
    
    def __init__(self, screen, screenDims, ioManager, fighter):
        self.screen = screen
        self.screenDims = screenDims
        self.ioManager = ioManager
        self.battleImgs = ioManager.get_data('battles', 'images')
        self.battleImgs[None] = self.battleImgs['done']
        self.battleImgs = self.create_images(self.battleImgs)
        self.critterImgs = self.create_images(ioManager.get_data('critters', 'images'))
        aiFighter = aifighter.AIFighter(self.generate_ai_critters())
        self.battle = battle.BattleHandler(fighter, aiFighter)
        self.print_colors()
        self.step = ('move', 0)
        self.stepFuncs = {'move' : self.select_move,
                          'target' : self.select_target,
                          'turn' : self.run_turn}
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
                if event.key == pygame.K_m: # TODO: remove when debugging is done
                    return 'map'
                if event.key in self.keyMapping:
                    errorCode = self.stepFuncs[self.step[0]](self.step[1], self.keyMapping[event.key]-1)
                    if errorCode == 1:
                        self.step = self.determine_next_step()
                    elif errorCode == 2 or errorCode == 3 or errorCode == 4:
                        return 'map'
        return 'battle'
        
    def draw(self):
        images, fonts = [[self.battleImgs['default'], (0, 1, 0, 1)]], []
        if self.step[0] == 'move':
            moveImgs, moveFonts = self.get_move_images()
            images.extend(moveImgs)
            fonts.extend(moveFonts)
        elif self.step[0] == 'target':
            targetImgs, targetFonts = self.get_target_images()
            images.extend(targetImgs)
            fonts.extend(targetFonts)
        critterImgs, critterFonts = self.get_critter_images()
        images.extend(critterImgs)
        fonts.extend(critterFonts)
        for i, pos in images:
            self.load_image(i, pos)
        for i, pos in fonts:
            self.print_words(i, pos)
        pygame.display.flip()    

    def make_actions(self):
        pass
    
    def determine_next_step(self):
        if self.step[0] == 'target':
            if self.step[1] == 0 and self.battle.valid_critter(1):
                return ('move', 1)
            else:
                return ('turn', 0)
        elif self.step[0] == 'move':
            return ('target', self.step[1])
        elif self.step[0] == 'turn':
            if self.battle.valid_critter(0):
                return ('move', 0)
            elif self.battle.valid_critter(1):
                return ('move', 1)
            else:
                raise Exception('Turn ended wit no usable critters')
        else:
            raise Exception('Could not determine next step: {}'.format(self.step))
                
        
    def generate_ai_critters(self):
        return [critter.Critter('doge', self.ioManager, 5),
                critter.Critter('doge', self.ioManager, 5)]
        
    def select_move(self, critPos, moveNum):
        if self.battle.valid_move(critPos, moveNum):
            self.currentMoveNum = moveNum
            return 1
        return 0
    
    def select_target(self, critterPos, targetPos):
        if self.battle.valid_target(critterPos, targetPos):
            self.battle.add_action(critterPos, targetPos, self.currentMoveNum)
            self.currentMove = None
            return 1
        return 0
   
    # params there so it can be called even with no     
    def run_turn(self, critterPos=None, targetPos=None):
        return self.battle.next_step()

    def get_move_images(self):
        images, fonts = [], []
        moves = self.battle.get_critter_moves(self.step[1])
        x, y = 0.05, 0.8
        for name in moves:
            images.append((self.battleImgs['redbox'], (x, x+0.15, y, y+0.11)))
            fonts.append((name, (x+0.01,x+0.14, y+0.01, y+0.1)))
            x += 0.17
        return images, fonts

    def get_target_images(self):
        boxPos = [(0.04, 0.19, 0.60, 0.75), (0.04, 0.19, 0.77, 0.92),
                  (0.21, 0.36, 0.60, 0.75), (0.21, 0.36, 0.77, 0.92)]
        fontPos = [(0.05, 0.18, 0.65, 0.70), (0.05, 0.18, 0.82, 0.87),
                   (0.22, 0.35, 0.65, 0.70), (0.22, 0.35, 0.82, 0.87)]
        names = self.battle.get_targets(self.step[1])
        images, fonts = [], []
        fonts = []
        for i in range(4):
            images.append((self.battleImgs['targetbox'], boxPos[i]))
            fonts.append((names[i], fontPos[i]))
        return images, fonts

    def get_critter_images(self):
        crits = self.battle.get_critters()
        hps = self.battle.get_critter_hps()
        critPos = [(0.10, 0.35, 0.00, 0.25), (0.10, 0.35, 0.27, 0.52),
                   (0.55, 0.80, 0.00, 0.25), (0.55, 0.80, 0.27, 0.52)]
        hpPos = [(0.05, 0.10, 0.10, 0.20), (0.05, 0.10, 0.37, 0.47),
                 (0.90, 0.95, 0.10, 0.20), (0.90, 0.95, 0.37, 0.47)]
        images, fonts = [], []
        for i in range(4):
            if crits[i] != '':
                images.append((self.critterImgs[crits[i]],
                               critPos[i]))
            fonts.append((hps[i], hpPos[i]))
        return images, fonts