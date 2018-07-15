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
        self.conctr = 0
        self.slpctr = 0
        self.para = False
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

    #returns a tuple containing the damage taken, any added status effects, and any extra info
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
                    if attack[1][i] == 'slp':
                        self.slpctr = random.randint(1,7)
                    elif attack[1][i] == 'con':
                        self.conctr = random.randint(1,4)
            self.crunch_status()
        return (dmgtaken, addedstatus, extrainfo)

    #returns a tuple containing the damage to deal, status effects to apply, any changes in own status, and any extra info
    def attack(self, move):
        movedict = self.ioman.get_data('moves', move)
        status = []
        addedstatus = []
        info = ''
        if self.status.count('fli') > 0:
            return (0, (), (), 'flinched')
        if self.status.count('frz') > 0:
            return (0, (), (), 'frozen')
        if self.status.count('con') > 0:
            self.conctr -= 1
            if random.randint(0,1) == 0:
                self.defend((40 * self.atk), (), (), '')
                return (0, (), (), 'confused')
        if self.para:
            return (0, (), (), 'paralyzed')
        if 'selfstatus' in movedict:
            for i in range(0, len(movedict['selfstatus']), 2):
                if random.randint(0, 99) < movedict['selfstatus'][i + 1]:
                    self.status.append(movedict['selfstatus'][i])
                    addedstatus.append(movedict['selfstatus'][i])
            self.crunch_status()
        if 'acc' in movedict:
            if random.randint(0, 99) > movedict['acc']:
                return (0, (), (), 'miss')
        else:
            if random.randint(0, 255) == 0:
                return (0, (), (), 'gen1miss')
        if 'status' in movedict:
            status.extend(movedict['status'])
        return (movedict['dmg'] * self.atk, status, addedstatus, info)

    #removes conflicting status effects
    def crunch_status(self):
        spdct = self.status.count('spdup') - self.status.count('spddn')
        defct = self.status.count('defup') - self.status.count('defdn')
        atkct = self.status.count('atkup') - self.status.count('atkdn')
        self.status = [stat for stat in self.status if stat != 'spdup' and stat != 'spddn']
        if spdct > 0:
            for i in range(spdct):
                self.status.append('spdup')
        elif spdct < 0:
            for i in range(-1 * spdct):
                self.status.append('spddn')
        self.status = [stat for stat in self.status if stat != 'defup' and stat != 'defdn']
        if defct > 0:
            for i in range(defct):
                self.status.append('defup')
        elif defct < 0:
            for i in range(-1 * defct):
                self.status.append('defdn')
        self.status = [stat for stat in self.status if stat != 'atkup' and stat != 'atkdn']
        if atkct > 0:
            for i in range(atkct):
                self.status.append('atkup')
        elif atkct < 0:
            for i in range(-1 * atkct):
                self.status.append('atkdn')

    def update_status(self):
        if len(self.status) > 0:
            remslp = False
            remcon = True
            if self.status.count('fli') > 0:
                self.status = [stat for stat in self.status if stat != 'fli']
            for stat in self.status:
                if stat == 'brn':
                    self.currenthp -= int(self.hp / 8)
                elif stat == 'psn':
                    self.currenthp -= int(self.hp / 8)
                elif stat == 'para':
                    if random.randint(0,3) == 0:
                        self.para = True
                elif stat == 'con':
                    if self.conctr == 0:
                        remcon = True
                elif stat == 'slp':
                    self.slpctr -= 1
                    if self.slpctr == 0:
                        remslp = True
            if remslp:
                self.status = [stat for stat in self.status if stat !- 'slp']
            if remcon:
                self.status = [stat for stat in self.status if stat !- 'con']
