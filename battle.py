import pygame

import aifighter

class Battle(object):
    
    def __init__(self, fighter, images):
        self.battleImgs = images['battle']
        self.critterImgs = images['critter']
        self.fighter = fighter
        self.aifighter = aifighter.AIFighter()
        self.fighterCritters = []
        self.aifighterCritters = []
        i = 0
        while len(self.fighterCritters) < 2 and i < len(self.fighter.critters):
            if self.fighter.critters[i].currenthp > 0:
                self.fighterCritters.append(self.fighter.critters[i])
        if len(self.aifighter.critters) >= 2:
            self.aifighterCritters = self.aifighter.critters[0:2]
        else:
            self.aifighterCritters = list(self.aifighterCritters)
        self.state = 'default'
        self.checkingCritter = self.fighterCritters[0]
        self.actions = [] # list of lists: player, critter, move, target
        self.stateActions = {'default' : self.try_move,
                        'switch' : self.try_switch,
                        'target' : self.select_target,
                        None : self.do_nothing,
                        'turn': self.execute_actions}
        self.stateDrawings = {'default' : self.get_default_battle_images,
                              'target' : self.get_target_battle_images}
        
    # DO NOT DELETE, used in self.stateActions
    def do_nothing(self):
        pass
            
    def try_switch(self, key):
        pass

    def try_move(self, key):
        if key == 5:
            self.state = 'switch'
        if key <= len(self.checkCritterMoves):
            self.actions.append([self.fighter, self.checkingCritter, 
                                 self.checkingCritter.currentmoves[self.checkCritterMoves[key]]])
            self.state = 'target'
            
    def select_target(self, key):
        if key < 3:
            self.actions[-1].append(key)
            if len(self.actions) < 2:
                self.state = 'default'
                self.checkingCritter = self.fighterCritters[1]
            else:
                self.state = 'turn'
            
    def get_ai_actions(self):
        self.actions.extend(aifighter.get_action())

    def get_default_battle_images(self):
        images = []
        fonts = []
        self.checkCritterMoves = []
        images.append((self.battleImgs[self.state], (0,1,0,1)))
        x, y = 0.05, 0.8
        for name, value in self.checkingCritter.currentmoves.items():
            images.append((self.battleImgs['redbox'], (x, x+0.2, y, y+0.13)))
            fonts.append((name, (x+0.01,x+0.19, y+0.01, y+0.12)))
            self.checkCritterMoves.append(name)
            x += 0.21
        return images, fonts

    def get_target_battle_images(self):
        images = []
        fonts = []
        print(self.aifighter.critters)
        fonts.append([self.aifighter.critters[0].name, (0.1, 0.2, 0.8, 0.9)])
        images.append([self.battleImgs[self.state], (0,1,0,1)])
        return images, fonts
    

    def get_creature_images(self):
        return []

    def run(self):
        pass
    
    def execute_actions(self):
        pass