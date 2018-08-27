import random

from madness import critter
from madness import battle
from madness import fighter

class AIFighter(fighter.Fighter):

    def __init__(self, critters=[]):
        self.critters = list(critters)

    def get_actions(self, critters):
        myCritters = []
        actions = []
        if critters[2] != None:
            myCritters.append(2)
        if critters[3] != None:
            myCritters.append(3)
        for crit in myCritters:
            moves = len(critters[crit].get_move_list())
            # doesn't matter if crit 0/1 is dead, will get redirected
            actions.append((crit, random.choice([0,1]), random.randrange(moves)))
        return actions
    
    def do_switch(self, battleCrits):
        possibleCrits = []
        newCrits = []
        for c in self.critters:
            if c not in battleCrits and (not c.dead):
                possibleCrits.append(c)
        for i in range(2, 4):
            if battleCrits[i] == None and len(possibleCrits) > 0:
                critNum = random.randrange(len(possibleCrits))
                newCrits.append(possibleCrits[critNum])
                del possibleCrits[critNum]
        return newCrits