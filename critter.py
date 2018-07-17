import iomanager
import random

class Critter:
    def __init__(self, name, ioman, lvl=1, currentmoves=None, currenthp=None):
        self.ioman = ioman
        statsin = self.ioman.get_data('critters', name, 'stats')
        self.moves = self.ioman.get_data('critters', name, 'moves')
        self.defense = statsin['def']
        self.hp = statsin['hp']
        self.spd = statsin['spd']
        self.atk = statsin['atk']
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
                for j in range(len(self.currentmoves), 4):
                    for key, value in self.moves.items():
                        if(value == i):
                            self.currentmoves.append(key)
                i -= 1
        else:
            self.currentmoves = currentmoves

    def defend(self, attack):
        addedstatus = []
        extrainfo = ''
        dmgtaken = 0
        if(attack[0] > 0):
            dmgtaken = int(attack[0] / self.defense + 1)
            self.hp -= dmgtaken
        if(len(attack) > 1):
            print("handling status effects")
            for i in range(0, len(attack[1]), 2):
                if random.randint(0, 99) < attack[1][i + 1]:
                    self.status.append(attack[1][i])
                    addedstatus.append(attack[1][i])
        return (dmgtaken, addedstatus, extrainfo)

    def attack(self, move):
        movedict = self.ioman.get_data('moves', move)
        status = []
        addedstatus = []
        info = ''
        if 'selfstatus' in movedict:
            for i in range(0, len(movedict['selfstatus']), 2):
                if random.randint(0, 99) < movedict['selfstatus'][i + 1]:
                    self.status.append(movedict['selfstatus'][i])
                    addedstatus.append(movedict['selfstatus'][i])
        if 'acc' in movedict:
            if random.randint(0, 99) > movedict['acc']:
                return (0, (), (), 'miss')
        else:
            if random.randint(0, 255) == 0:
                return (0, (), (), 'gen1miss')
        if 'status' in movedict:
            status.extend(movedict['status'])
        return (movedict['dmg'] * self.atk, status, addedstatus, info)

    def update_status(self):
        if len(self.status) > 0:
            print('status update time')
