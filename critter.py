import IOManager

class Critter:
    def __init__(self, name, iomanager, lvl=1, currentmoves=None, currenthp=None):
        statsin = iomanager.get_data('critters', name, 'stats')
        self.moves = iomanager.get_data('critters', name, 'moves')
        self.iomanager = iomanager
        self.def = statsin['def']
        self.hp = statsin['hp']
        self.spd = statsin['spd']
        self.atk = statsin['atk']
        self.exp = exp
        self.lvl = lvl
        self.status = []
        if(currenthp == None or currenthp > self.hp):
            self.currenthp = self.hp
        else:
            self.currenthp = currenthp
        if(currentmoves == None):
            self.currentmoves = []
            i = self.lvl
            while len(self.currentmoves) < 4 and i > 0:
                for j in range(len(bestmoves), 4):
                    for key, value in self.moves.items():
                        if(value == i):
                            self.currentmoves.append(key)
                i -= 1
        else:
            self.currentmoves = currentmoves

    def defend(self, attack):

    def attack(self, move):
        if self.currenthp == 0:
            return (0)
        else:
            movedict = self.iomanager.get_data('moves', move)
            if 'status' in movedict:
                return (movedict['dmg'] * self.atk, movedict['status'])
            else:
                return (movedict['dmg'] * self.atk)

    def update_status(self):
        if len(self.status) > 0:
            print('status update time')
