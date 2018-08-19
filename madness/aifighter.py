import random

from madness import critter
from madness import battle

class AIFighter(object):

    def __init__(self, critters=[]):
        self.critters = critters

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
    
    def get_start_critters(self):
        critters = []
        i = 0
        while len(critters) < 2 and i < len(self.critters):
            if not self.critters[i].dead:
                critters.append(self.critters[i])
            i += 1
        while len(critters) < 2:
            critters.append(None)
        return critters
     
    def has_playable_critters(self):
        for c in self.critters:
            if not c.dead:
                return True
        return False