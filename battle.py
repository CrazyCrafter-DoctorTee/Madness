import pygame

import aifighter

class Battle(object):
    
    def __init__(self, fighter):
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
        self.actions = []
        self.stateActions = {'default' : self.try_move,
                        'switch' : self.try_switch,
                        'target' : self.select_target,
                        None : self.do_nothing,
                        'done': self.do_nothing}
        
    # DO NOT DELETE, used in self.actions
    def do_nothing(self):
        pass
            
    def try_switch(self, key):
        pass

    def try_move(self, key):
        if key == 5:
            self.state = 'switch'
        if len(self.checkingCritter.currentmoves) <= key:
            self.actions.append([self.checkingCritter, key])
            self.state = 'target'
            
    def select_target(self, key):
        self.actions[-1].append(key)
        if self.fighterCritters[0] == self.checkingCritter:
            self.state = 'default'
            self.checkingCritter = self.fighterCritters[1]
        else:
            print(None)
            self.state = None
            
    def get_battle_images(self):
        return [(self.state, (0, 0))]

    def get_creature_images(self):
        return []

    def run(self):
        pass