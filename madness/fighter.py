from madness import critter

class Fighter(object):

    def __init__(self, iomanager, critters=[]):
        self.iomanager = iomanager
        if critters == []:
            self.critters = [critter.Critter('gato', iomanager, 50), critter.Critter('doge', iomanager, 50),
                             critter.Critter('snek', iomanager, 50)]
        else:
            self.critters = critters
        
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
    
    def alive_critter_count(self):
        count = 0
        for c in self.critters:
            if not c.dead:
                count += 1
        return count