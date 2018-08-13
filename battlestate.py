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
    5: perform switch
'''

class BattleState(gamestate.GameState):

    def __init__(self, screen, screenDims, ioManager, fighter):
        self.screen = screen
        self.screenDims = screenDims
        self.battleover = False
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
                          'turn' : self.run_turn,
                          'end' : self.run_end,
                          'switch' : self.try_switch}
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
                if event.key in self.keyMapping:
                    returnCode = self.stepFuncs[self.step[0]](self.step[1], self.keyMapping[event.key]-1)
                    if returnCode == 1:
                        self.step = self.determine_next_step()
                    elif returnCode == 2 or returnCode == 3 or returnCode == 4:
                        self.battleover = True
                    elif returnCode == 5:
                        self.step = ('switch', self.step[1])
            if event.type == pygame.MOUSEBUTTONDOWN:
                mpos = pygame.mouse.get_pos()
                for button in self.buttons:
                    bu = button.update(mpos[0],mpos[1])
                    if bu != 0:
                        returncode = self.stepFuncs[self.step[0]](self.step[1], bu-1)
                        if returnCode == 1:
                            self.step = self.determine_next_step()
                        elif returnCode == 2 or returnCode == 3 or returnCode == 4:
                            self.battleover = True
                        elif returnCode == 5:
                            self.step = ('switch', self.step[1])
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
        elif self.step[0] == 'switch':
            switchImages, switchFonts = self.get_switch_images()
            images.extend(switchImages)
            fonts.extend(switchFonts)
        critterImgs, critterFonts = self.get_critter_images()
        images.extend(critterImgs)
        fonts.extend(critterFonts)
        for i, pos in images:
            self.load_image(i, pos)
        for i, pos in fonts:
            self.print_words(i, pos)
        pygame.display.flip()

    def make_actions(self):
        if self.battleover:
            return 'map'
        return 'battle'

    def determine_next_step(self):
        if self.step[0] == 'target' or self.step[0] == 'switch':
            if self.step[1] == 0 and self.battle.valid_critter(1):
                return ('move', 1)
            else:
                return ('turn', 2)
        elif self.step[0] == 'move':
            return ('target', self.step[1])
        elif self.step[0] == 'end':
            if self.battle.valid_critter(0):
                return ('move', 0)
            elif self.battle.valid_critter(1):
                return ('move', 1)
            else:
                raise Exception('Turn ended wit no usable critters')
        elif self.step[0] == 'turn':
            return ('end', 2)
        else:
            raise Exception('Could not determine next step: {}'.format(self.step))


    def generate_ai_critters(self):
        return [critter.Critter('doge', self.ioManager, 5),
                critter.Critter('snek', self.ioManager, 5)]

    def select_move(self, critPos, moveNum):
        if moveNum == 4:
            return 5
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

    def run_end(self, critterPos=None, targetPos=None):
        return self.battle.end_action()

    def try_switch(self, critPos, switchNum):
        if self.battle.valid_switch(critPos, switchNum):
            self.battle.add_action(critPos, switchNum, -1)
            return 1
        return 0

    def get_move_images(self):
        images, fonts = [], []
        moves = self.battle.get_critter_moves(self.step[1])
        x, y = 0.05, 0.8
        for name in moves:
            images.append((self.battleImgs['redbox'], (x, x+0.15, y, y+0.11)))
            fonts.append((name, (x+0.01,x+0.14, y+0.01, y+0.1)))
            x += 0.17
        images.append((self.battleImgs['darkbluebox'], (0.73, 0.93, 0.8, 0.91)))
        fonts.append(('switch', (0.74, 0.92, 0.81, 0.90)))
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

    def get_switch_images(self):
        images, fonts = [], []
        switchCrits = self.battle.get_switch_options()
        x, y = 0.05, 0.8
        for crit in switchCrits:
            images.append((self.battleImgs['greenbox'], (x, x+0.15, y, y+0.11)))
            fonts.append((crit.name, (x+0.01, x+0.14, y+0.01, y+0.1)))
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
