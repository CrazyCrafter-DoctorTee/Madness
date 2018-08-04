import pygame
import queue

import aifighter



class Battle(object):

    def __init__(self, fighter, aiFighter, images):
        self.battleImgs = images['battle']
        self.critterImgs = images['critter']
        self.fighter = fighter
        self.aifighter = aiFighter
        self.fighterCritters = []
        self.aifighterCritters = []
        self.logMsgs = queue.Queue()
        i = 0
        while len(self.fighterCritters) < 2 and i < len(self.fighter.critters):
            if self.fighter.critters[i].currenthp > 0:
                self.fighterCritters.append(self.fighter.critters[i])
        if len(self.aifighter.critters) >= 2:
            self.aifighterCritters = self.aifighter.critters[0:2]
        else:
            self.aifighterCritters = list(self.aifighterCritters)
        self.state = 'move'
        self.checkCritter = self.fighterCritters[0]
        self.checkCritterMoves = list(self.checkCritter.currentmoves.keys())
        self.actions = [] # list of lists: player, critter, move, target
        self.checkCritter = self.fighterCritters[0]
        self.stateActions = {'move' : self.try_move,
                        'switch' : self.try_switch,
                        'target' : self.select_target,
                        None : self.do_nothing,
                        'turn': self.execute_actions}

    # DO NOT DELETE, used in self.stateActions
    def do_nothing(self):
        pass

    def try_switch(self, key):
        pass

    def try_move(self, key):
        if key == 5:
            self.state = 'switch'
        elif key <= len(self.checkCritterMoves):
            self.actions.append(['fighter', self.checkCritter, self.checkCritterMoves[key-1], None])
            self.state = 'target'

    def select_target(self, key):
        if 1 <= key <= 3:
            self.actions[-1][3] = key
            if len(self.actions) == 1:
                self.state = 'move'
                self.checkCritter = self.fighterCritters[1]
                self.checkCritterMoves = list(self.fighterCritters[1].currentmoves.keys())
            else:
                self.actions.extend(self.aifighter.get_actions(self))
                self.actionNumber = 0
                self.state = 'turn'

    def get_ai_actions(self):
        self.actions.extend(aifighter.get_action())

    def get_default_battle_images(self):
        images = []
        fonts = []
        self.checkCritterMoves = []
        images.append((self.battleImgs[self.state], (0,1,0,1)))
        x, y = 0.05, 0.8
        for name, value in self.checkCritter.currentmoves.items():
            images.append((self.battleImgs['redbox'], (x, x+0.15, y, y+0.11)))
            fonts.append((name, (x+0.01,x+0.14, y+0.01, y+0.1)))
            self.checkCritterMoves.append(name)
            x += 0.17
        critterImages, critterFonts = self.get_creature_images()
        images.extend(critterImages)
        fonts.extend(critterFonts)
        return images, fonts

    def get_target_battle_images(self):
        images = []
        fonts = []
        fonts.append([self.aifighter.critters[0].name, (0.22, 0.35, 0.65, 0.70)])
        fonts.append([self.aifighter.critters[1].name, (0.22, 0.35, 0.82, 0.87)])
        images.append([self.battleImgs['default'], (0,1,0,1)])
        images.append([self.battleImgs['targetbox'], (0.21, 0.36, 0.6, 0.75)])
        images.append([self.battleImgs['targetbox'], (0.21, 0.36, 0.77, 0.92)])
        if len(self.actions) == 1:
            images.append([self.battleImgs['targetbox'], (0.04, 0.19, 0.77, 0.92)])
            fonts.append([self.fighter.critters[1].name, (0.05, 0.18, 0.82, 0.87)])
        else:
            images.append([self.battleImgs['targetbox'], (0.04, 0.19, 0.6, 0.75)])
            fonts.append([self.fighter.critters[0].name, (0.22, 0.35, 0.82, 0.87)])
        critterImages, critterFonts = self.get_creature_images()
        images.extend(critterImages)
        fonts.extend(critterFonts)
        return images, fonts


    def get_turn_battle_images(self):
        images = []
        fonts = []
        images.append([self.battleImgs['default'], (0, 1, 0, 1)])
        critterImages, critterFonts = self.get_creature_images()
        images.extend(critterImages)
        fonts.extend(critterFonts)
        return images, fonts

    def handle_move_result(self, defender, result):
        stats = {'atk' : 'attack', 'def' : 'defense', 'spd' : 'speed'}
        upOrDown = {'up' : 'up', 'dn' : 'down'}
        for status in result[1]:
            msg = ''
            if status == 'DEAD':
                msg = '{} died'.format(defender)
            elif status == 'psn':
                msg = '{} was poisoned'.format(defender.name)
            elif status == 'slp':
                msg = '{} went to sleep'.format(defender.name)
            elif status == 'con':
                msg = '{} got confused'.format(defender.name)
            elif status == 'brn':
                msg = '{} was burned'.format(defender.name)
            elif status == 'recha':
                msg = '{} is recharging'.format(defender.name)
            elif len(status) == 5 and status[0:3] in stats.keys():
                msg = '{}\'s {} went {}'.format(defender, stats[status[0:3], upOrDown[status[4:6]]])
            else:
                print('ERROR: Could not parse {}'.format(status))
            self.logMsgs.put(msg)

    def execute_actions(self, key=None):
        if self.actionNumber < len(self.actions)-1:
            attacker = self.actions[self.actionNumber][1]
            if not attacker.dead:
                defender = self.actions[self.actionNumber][3]
                move = self.actions[self.actionNumber][2]
                moveresult = attacker.attack(move)
                defendResult = defender.defend(moveresult)
                # (0.1, 0.9, 0.8, 0.9)
                self.logMsg.put('{} attacked {} with {}'.format(attacker.name,
                                                              defender.name,
                                                              move))
                self.handle_move_result(defender, defendResult)
            self.actionNumber += 1
        else:
            self.end_turn()

    def end_turn(self):
        self.actions = []
        self.fighterCritters[0].update_status()
        self.fighterCritters[1].update_status()
        self.aifighterCritters[0].update_status()
        self.aifighterCritters[1].update_status()
        self.state = 'move'
