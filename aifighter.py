import critter

class AIFighter(object):
    
    def __init__(self, critters=[]):
        self.critters = critters
        if critters == []:
            critters = []
        
    def generate_critters(self):
        pass