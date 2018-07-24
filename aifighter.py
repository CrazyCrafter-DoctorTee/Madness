import random

import critter
import battle

class AIFighter(object):

    def __init__(self, critters=[]):
        self.critters = critters

    def get_actions(self, battle):
        myCritters = battle.aifighterCritters
        enemyCritters = battle.fighterCritters
        actions = [] # player, critter, move, target
        for crit in myCritters:
            moves = list(crit.currentmoves.keys())
            actions.append((self, crit, random.choice(moves), random.choice(enemyCritters)))
        return actions
