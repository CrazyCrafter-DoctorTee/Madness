import pygame
import queue

import aifighter

class BattleInfo(object):
    
    def __init__(self, fighter, aiFighter, critters):
        self.fighter = fighter
        self.aiFighter = aiFighter
        self.critters = critters
    
    def get_critter_names(self):
        names = []
        for c in self.critters:
            if c != None:
                names.append(c.name)
            else:
                names.append('')
        return names
    
    def get_critter_hps(self):
        hps = []
        for c in self.critters:
            if c != None:
                hps.append(str(c.currenthp))
            else:
                hps.append('')
        return hps
                
    def get_critter_moves(self, critPos):
        if self.critters[critPos] != None:
            return self.critters[critPos].get_move_list()
        return None
    
    def get_targets(self, critPos):
        targets = []
        for i in range(len(self.critters)):
            if self.critters[i] == None or i == critPos:
                targets.append('')
            else:
                targets.append(self.critters[i].name)
        return targets
        
    def critter_death(self, critPos):
        self.critters[critPos] = None
        
    def critter_switch_options(self):
        options = []
        for c in self.fighter.critters:
            if (self.critters[0] is not c
                and self.critters[1] is not c):
                options.append(c)
        return options
    
    def perform_switch(self, critPos, crit):
        for c in self.fighter.critters:
            if c is crit:
                self.critters[critPos] = crit
                break
            
    def valid_critter(self, critPos):
        return self.critters[critPos] != None
    
    def determine_winner(self):
        fighterIsAlive = self.fighter.has_playable_critters()
        aiIsAlive = self.aiFighter.has_playable_critters()
        if fighterIsAlive and aiIsAlive:
            return None
        elif aiIsAlive:
            return 'ai'
        elif fighterIsAlive:
            return 'fighter'
        else:
            return 'both'

    def switch_defender(self, target):
        if target == 0:
            return 1
        if target == 1:
            return 0
        if target == 2:
            return 3
        if target == 3:
            return 2
    
    def attacking_enemy(self, attPos, defPos):
        if attPos == 0 or attPos == 1:
            if defPos == 2 or defPos == 3:
                return True
            else:
                return False
        elif attPos == 2 or attPos == 3:
            if defPos == 0 or defPos == 1:
                return True
            else:
                return False

    def get_defender(self, attPos, defPos):
        if self.attacking_enemy(attPos, defPos):
            if self.critters[defPos] == None:
                return self.switch_defender(defPos)
            else:
                return defPos
        else:
            return defPos
        
    def execute_action(self, action):
        defendResult = None
        if self.critters[action[0]] != None:
            attacker = self.critters[action[0]]
            defendPos = self.get_defender(action[0], action[1])
            defender = self.critters[defendPos]
            move = action[2]
            moveResult = attacker.attack(move)
            if defender != None:
                defendResult = defender.defend(moveResult)
                if 'DEAD' in defendResult[1]:
                    self.critter_death(defendPos)
        return defendResult

class BattleHandler(object):
    
    def __init__(self, fighter, aiFighter):
        self.fighter = fighter
        self.aiFighter = aiFighter
        critters = self.fighter.get_start_critters()
        critters.extend(self.aiFighter.get_start_critters())
        self.battleInfo = BattleInfo(fighter, aiFighter, critters)
        self.end_turn()
    
    def end_turn(self):
        winner = self.battleInfo.determine_winner()
        if winner is None:
            self.turnActions = []
            self.turnInitialized = False
            return 0
        elif winner == 'fighter':
            return 1
        elif winner == 'ai':
            return 2
        elif winner == 'both':
            return 3
        else:
            raise Exception('Weird output from determine_winner: {}'.format(winner))
        
    def valid_move(self, critPos, move):
        moves = self.battleInfo.get_critter_moves(critPos)
        if moves != None:
            return move < len(moves)
        return False
    
    def valid_target(self, critPos, target):
        if critPos != target and target < 4:
            return True
        return False
    
    def valid_critter(self, critPos):
        return self.battleInfo.valid_critter(critPos)
    
    def add_action(self, critPos, target, move):
        if self.valid_critter(critPos) and self.valid_target(critPos, target):
            self.turnActions.append((critPos, target, move))
        else:
            raise Exception('Invalid action added!')
    
    def next_step(self):
        if self.turnInitialized == False:
            self.initialize_turn()
        if not self.actionQueue.empty():
            self.nextAction = self.actionQueue.get(block=False)
        turnStatus = self.battleInfo.execute_action(self.nextAction)
        while turnStatus == None:
            turnStatus = self.battleInfo.execute_action(self.nextAction)
        
        winner = self.battleInfo.determine_winner()
        if winner == 'fighter':
            return 2
        elif winner == 'ai':
            return 3
        elif winner == 'both':
            return 4
        elif self.actionQueue.empty():
            return 1
        else:
            return 0
        
    def initialize_turn(self):
        self.actionQueue = queue.Queue()
        self.nextAction = None
        self.turnActions.extend(self.aiFighter.get_actions(self.battleInfo.critters))
        for a in self.turnActions:
            self.actionQueue.put(a)
        self.turnInitialized = True
    
    def get_critter_moves(self, critPos):
        return self.battleInfo.get_critter_moves(critPos)
    
    def get_critters(self):
        return self.battleInfo.get_critter_names()
    
    def get_critter_hps(self):
        return self.battleInfo.get_critter_hps()
    
    def get_targets(self, critPos):
        return self.battleInfo.get_targets(critPos)