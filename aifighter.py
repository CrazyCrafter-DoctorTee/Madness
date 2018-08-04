import random

import critter
import battle

class AIFighter(object):

    def __init__(self, critters=[]):
        self.critters = critters

    def get_actions(self, b):
        myCritters = b.aifighterCritters
        actions = [] # player, critter, move, target
        for crit in myCritters:
            moves = list(crit.currentmoves.keys())
            actions.append(('ai', crit, random.choice(moves), random.randrange(len(b.fighterCritters))))
        return actions
