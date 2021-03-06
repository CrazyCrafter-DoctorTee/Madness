import pygame

import random
import time

from madness import aifighter
from madness import battle
from madness import critter
from gamemanager import button
from gamemanager import gamestate

'''
stepFuncs function codes:
    0: don't change step
    1: go to next step
    2: player won
    3: player lost
    4: tie
    5: perform switch
    6: perform enterance
    7: go back to previous move
'''

class BattleState(gamestate.GameState):

    def __init__(self, screen, screenDims, ioManager, fighter):
        self.screen = screen
        self.screenDims = screenDims
        self.battleOver = False
        self.ioManager = ioManager
        self.battleImgs = ioManager.get_data('battles', 'images')
        self.battleImgs = self.create_images(self.battleImgs)
        self.critterImgs = self.create_images(ioManager.get_data('critters', 'images'))
        aiFighter = aifighter.AIFighter(self.generate_ai_critters())
        self.battle = battle.BattleHandler(fighter, aiFighter)
        self.buttons = []
        self.displayOutcome = False
        self.quit = False
        self.print_colors()
        self.step = ('move', 0)
        self.buttons = self.get_buttons()
        self.stepFuncs = {'move' : self.select_move,
                          'target' : self.select_target,
                          'turn' : self.run_turn,
                          'end' : self.run_end,
                          'switch' : self.try_switch,
                          'enter' : self.try_enter,
                          'win' : self.back_to_map,
                          'lose' : self.quit_game}
        # TODO: make keyMapping global
        self.keyMapping = {pygame.K_1 : 1,
                           pygame.K_2 : 2,
                           pygame.K_3 : 3,
                           pygame.K_4 : 4,
                           pygame.K_5 : 5,
                           pygame.K_6 : 6}

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
                self.quit = True
            if event.type == pygame.KEYDOWN:
                if event.key in self.keyMapping:
                    self.process_key_action(self.keyMapping[event.key]-1)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                actionNum = self.get_button_action_type(mousePos)
                # if step[1] is -1, player isn't selecting, they are just going through text
                if actionNum != None or self.step[1] == -1:
                    self.process_key_action(actionNum)
        
    def make_actions(self):
        if self.quit:
            return None
        elif self.battleOver:
            return 'map'
        return 'battle'

    def draw(self):
        images, fonts = [[self.battleImgs['default'], (0, 1, 0, 1)]], []
        critterImgs, critterFonts = self.get_critter_images()
        images.extend(critterImgs)
        fonts.extend(critterFonts)
        if self.displayOutcome:
            if self.step[0] == 'win':
                fonts.append(('You defeated the wild critters', (0.1, 0.9, 0.8, 0.9)))
            else:
                fonts.append(('You lost!', (0.1, 0.9, 0.8, 0.9)))
        else:
            fonts.append((self.battle.logMsg, (0.1, 0.9, 0.8, 0.9)))
            
        for i, pos in images:
            self.load_image(i, pos)
        for i, pos in fonts:
            self.print_words(i, pos)
        for b in self.buttons:
            imgInfo, fontInfo = b.get_drawing_info()
            self.load_image(imgInfo[0], imgInfo[1])
            self.print_words(fontInfo[0], fontInfo[1])
        pygame.display.flip()

    # step[0]: the current substate
    # step[1]: the critter to keep track of, or -1 if no critter
    def process_key_action(self, actionNum):
        returnCode = self.stepFuncs[self.step[0]](self.step[1], actionNum)
        if returnCode == 1:
            self.step = self.determine_next_step()
            self.buttons = self.get_buttons()
        elif returnCode == 2:
            self.step = ('win', -1)
        elif returnCode == 3 or returnCode == 4:
            self.step = ('lose', -1)
        elif returnCode == 5:
            self.step = ('switch', self.step[1])
            self.buttons = self.get_buttons()
        elif returnCode == 6:
            self.step = ('enter', -1)
            self.buttons = self.get_buttons()
        elif returnCode == 7:
            self.go_to_previous_step()

    # Only works for steps the user can undo (steps for selecting actions)
    def go_to_previous_step(self):
        if self.step == ('move', 1):
            self.step = ('move', 0)
            self.battle.remove_action()
        elif self.step[0] == 'target' or self.step[0] == 'switch':
            self.step = ('move', self.step[1])
            self.battle.remove_action()
        self.buttons = self.get_buttons()

    def determine_next_step(self): # TODO: clean up this function
        if self.step[0] == 'target' or self.step[0] == 'switch':
            if self.step[1] == 0 and self.battle.valid_critter(1):
                return ('move', 1)
            else:
                return ('turn', -1)
        elif self.step[0] == 'move':
            return ('target', self.step[1])
        elif self.step[0] == 'end':
            if self.battle.enter_is_possible():
                return ('enter', 0)
            else:
                if self.battle.valid_critter(0):
                    return ('move', 0)
                elif self.battle.valid_critter(1):
                    return ('move', 1)
        elif self.step[0] == 'enter':
            if self.battle.valid_critter(0):
                return ('move', 0)
            elif self.battle.valid_critter(1):
                return ('move', 1)
            else:
                raise Exception('Turn ended with no usable critters')
        elif self.step[0] == 'turn':
            return ('end', -1)
        else:
            raise Exception('Could not determine next step: {}'.format(self.step))


    def generate_ai_critters(self):
        critNames = list(self.critterImgs.keys())
        return [critter.Critter(random.choice(critNames), self.ioManager, 50),
                critter.Critter(random.choice(critNames), self.ioManager, 50)]

    def select_move(self, critPos, moveNum):
        if moveNum == 5: # if back
            self.battle.remove_action()
            return 7
        elif moveNum == 4: # if switch
            return 5
        elif self.battle.valid_move(critPos, moveNum):
            self.currentMoveNum = moveNum
            return 1
        else:
            return 0

    def select_target(self, critterPos, targetPos):
        if targetPos == 5:
            return 7
        elif self.battle.valid_target(critterPos, targetPos):
            self.battle.add_action(critterPos, targetPos, self.currentMoveNum)
            self.currentMove = None
            return 1
        else:
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
        elif switchNum == 5:
            return 7
        else:
            return 0
    
    def try_enter(self, critPos, switchNum):
        return self.battle.try_enter(switchNum)

    def get_button_action_type(self, position):
        x, y = position
        xNorm, yNorm = x/self.screenDims[0], y/self.screenDims[1]
        key = None
        i = 0
        while key == None and i < len(self.buttons):
            key = self.buttons[i].update(xNorm, yNorm)
            i += 1
        return key

    def get_buttons(self):
        phase, actionCrit = self.step
        if phase == 'move':
            return self.get_move_buttons(actionCrit)
        elif phase == 'target':
            return self.get_target_buttons(actionCrit)
        elif phase == 'switch' or phase == 'enter':
            return self.get_switch_buttons()
        else:
            return []

    def get_back_button(self):
        return button.Button(self.battleImgs['redbox'], 'back', (0.8, 0.9, 0.82, 0.9), 5)

    def get_move_buttons(self, actionCrit):
        buttons = []
        moves = self.battle.get_critter_moves(actionCrit)
        x, y = 0.05, 0.82
        for i in range(4):
            if i < len(moves):
                buttons.append(button.Button(self.battleImgs['graybox'], moves[i],
                                             (x, x+0.13, y, y+0.08), i))
            x += 0.15
        buttons.append(button.Button(self.battleImgs['darkbluebox'], 'switch',
                                     (0.65, 0.78, 0.82, 0.90), 4))
        buttons.append(self.get_back_button())
        return buttons

    def get_target_buttons(self, actionCrit):
        buttons = []
        boxPos = [(0.04, 0.19, 0.60, 0.75), (0.04, 0.19, 0.77, 0.92),
                  (0.21, 0.36, 0.60, 0.75), (0.21, 0.36, 0.77, 0.92)]
        names = self.battle.get_targets(actionCrit)
        for i in range(4):
            buttons.append(button.Button(self.battleImgs['targetbox'],
                        names[i], boxPos[i], i))
        buttons.append(self.get_back_button())
        return buttons

    def get_switch_buttons(self):
        buttons = []
        switchCrits = self.battle.get_switch_options()
        x, y = 0.05, 0.82
        i = 0
        while i < len(switchCrits):
            buttons.append(button.Button(self.battleImgs['greenbox'], switchCrits[i].name,
                                         (x, x+0.13, y, y+0.08), i))
            x += 0.15
            i += 1
        buttons.append(self.get_back_button())
        return buttons
    
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
    
    def back_to_map(self, arg0=None, arg1=None):
        if self.displayOutcome == False:
            self.displayOutcome = True
        else:
            self.battleOver = True
        
    def quit_game(self, arg0=None, arg1=None):
        if self.displayOutcome == False:
            self.displayOutcome = True
        else:
            self.quit = True