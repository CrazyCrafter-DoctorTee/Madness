import critter

class Fighter(object):
    
    def __init__(self, iomanager):
        self.iomanager = iomanager
        self.critters = [critter.Critter('doge', iomanager, 5), critter.Critter('doge', iomanager, 5)]