import critter

class Fighter(object):

    def __init__(self, iomanager):
        self.iomanager = iomanager
        self.critters = [critter.Critter('gato', iomanager, 5), critter.Critter('doge', iomanager, 5),
                         critter.Critter('snek', iomanager, 5)]
        
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