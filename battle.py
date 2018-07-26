import pygame

import aifighter

class Battle(object):

    def __init__(self, fighter, aiFighter, images):
        self.actionNumber = None # TODO: remove, here only for debugging
        self.battleImgs = images['battle']
        self.critterImgs = images['critter']
        self.fighter = fighter
        self.aifighter = aiFighter
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
                              'target' : self.get_target_battle_images,
                              'turn' : self.get_turn_battle_images}

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
                                 self.checkCritterMoves[key-1]])
            self.state = 'target'

    def select_target(self, key):
        if key < 4:
            if key < 2:
                self.actions[-1].append(self.aifighterCritters[key])
            else:
                if len(self.actions) == 1:
                    self.actions[-1].append(self.fighterCritters[1])
                else:
                    self.actions[-1].append(self.fighterCritters[0])
            if len(self.actions) < 2:
                self.state = 'default'
                self.checkingCritter = self.fighterCritters[1]
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
        for name, value in self.checkingCritter.currentmoves.items():
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


    def get_creature_images(self):
        images = []
        fonts = []
        images.append([self.critterImgs[self.fighterCritters[0].name], (0.1, 0.35, 0, 0.25)])
        images.append([self.critterImgs[self.fighterCritters[1].name], (0.1, 0.35, 0.27, 0.52)])
        images.append([self.critterImgs[self.aifighterCritters[0].name], (0.65, 0.9, 0, 0.25)])
        images.append([self.critterImgs[self.aifighterCritters[1].name], (0.65, 0.9, 0.27, 0.52)])
        fonts.append([str(self.fighterCritters[0].currenthp), (0.05, 0.1, 0.1, 0.2)])
        fonts.append([str(self.fighterCritters[1].currenthp), (0.05, 0.1, 0.37, 0.47)])
        fonts.append([str(self.aifighterCritters[0].currenthp), (0.9, 0.95, 0.1, 0.2)])
        fonts.append([str(self.aifighterCritters[1].currenthp), (0.9, 0.95, 0.37, 0.47)])
        return images, fonts

    def get_turn_battle_images(self):
        images = []
        fonts = []
        images.append([self.battleImgs['default'], (0, 1, 0, 1)])
        fonts.append(['{} attacked {} with {}'.format(self.actions[self.actionNumber][1].name,
                                                     self.actions[self.actionNumber][3].name,
                                                     self.actions[self.actionNumber][2]),
                        (0.1, 0.9, 0.8, 0.9)])
        critterImages, critterFonts = self.get_creature_images()
        images.extend(critterImages)
        fonts.extend(critterFonts)
        return images, fonts

    def execute_actions(self, key=None):
        if self.actionNumber < len(self.actions)-1:

            attacker = self.actions[self.actionNumber][1]
            defender = self.actions[self.actionNumber][3]
            move = self.actions[self.actionNumber][2]

            moveresult = attacker.attack(move)
            defendresult = defender.defend(moveresult)
            print(moveresult)
            print(defendresult)
            self.actionNumber += 1
        else:
            self.end_turn()

    def end_turn(self):
        self.actions = []
        self.state = 'default'
