import iomanager
import random

class Critter:
    #requires at minimum the critter tag and io manager, also takes a level, dict of moves and their pp, and current hit points
    def __init__(self, name, ioman, lvl=1, currentmoves=None, currenthp=None, extraexp=0):
        self.ioman = ioman
        self.name = name
        statsin = self.ioman.get_data('critters', name, 'stats')
        self.moves = self.ioman.get_data('critters', name, 'moves')
        self.lvl = lvl
        self.defense = int(statsin['def'] * (self.lvl / 50 + 1) / 3)
        self.hp = int(statsin['hp'] * (self.lvl / 50 + 1) / 3)
        self.spd = int(statsin['spd'] * (self.lvl / 50 + 1) / 3)
        self.atk = int(statsin['atk'] * (self.lvl / 50 + 1) / 3)
        self.exp = extraexp + self.lvl * self.lvl * self.lvl
        if self.exp > 100 * 100 * 100:
            self.exp = 100*100*100
        self.conctr = 0
        self.slpctr = 0
        self.recctr = 0
        self.dead = False
        self.status = []
        if(currenthp == None or currenthp > self.hp):
            self.currenthp = self.hp
        else:
            self.currenthp = currenthp
        if(currentmoves == None):
            self.currentmoves = {}
            i = self.lvl
            j = 0
            movenames = list(self.moves.keys())
            needmoves = True
            while needmoves:
                if self.moves[movenames[j]] == i:
                    self.currentmoves[movenames[j]] = self.ioman.get_data('moves', movenames[j], 'pp')
                if len(self.currentmoves) == 4:
                    needmoves = False
                j += 1
                if j == len(movenames):
                    j = 0
                    i -= 1
                if i < 0:
                    needmoves = False
        else:
            #picks 4 moves from the given ones, no gurantees on which ones
            if len(currentmoves) > 4:
                currentmoves = dict(currentmoves.items()[:3])
            self.currentmoves = currentmoves

    #returns a tuple containing the damage taken, any added status effects, and any extra info
    def defend(self, attack):
        addedstatus = []
        extrainfo = ''
        dmgtaken = 0
        if(attack[0] > 0):
            dmgtaken = int(attack[0] / self.defense + 1)
            self.currenthp -= dmgtaken
            if self.currenthp < 1:
                self.currenthp = 0
                self.dead = True
                addedstatus.append("DEAD")
        if(len(attack) > 1):
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

    #sets the level to a new value and updates stats accordingly
    def setlvl(self, newlvl):
        if newlvl > 0 and newlvl < 101:
            self.lvl += 1
            statsin = self.ioman.get_data('critters', self.name, 'stats')
            self.defense = int(statsin['def'] * (self.lvl / 50 + 1) / 3)
            self.hp = int(statsin['hp'] * (self.lvl / 50 + 1) / 3)
            self.spd = int(statsin['spd'] * (self.lvl / 50 + 1) / 3)
            self.atk = int(statsin['atk'] * (self.lvl / 50 + 1) / 3)

    #add experience after a battle, and levels up if necessesary. gracefully handles repeated level ups
    def addexp(self, amount):
        if self.lvl < 100:
            self.exp += amount
            keepchecking = True
            while keepchecking:
                lvl3 = (self.lvl + 1) * (self.lvl + 1) * (self.lvl + 1)
                if self.exp > lvl3 and self.lvl < 100:
                    self.lvlup()
                else:
                    keepchecking = False

    #convience methond to force a level up
    def lvlup(self):
        if self.lvl < 100:
            self.setlvl(self.lvl + 1)

    #returns a tuple containing the damage to deal, status effects to apply, any changes in own status, and any extra info
    #if the move is not in the dict of current moves returns 0 dmg
    def attack(self, moveNum):
        move = self.get_move_by_num(moveNum)
        movedict = self.ioman.get_data('moves', move)
        status = []
        addedstatus = []
        info = ''
        damage = movedict['dmg'] * self.atk * ((2 + self.status.count('dmgup')) / (2 + self.status.count('dmgdn')))
        #check to make sure attack can be executed:
        if self.dead:
            return (0, (), (), 'DEAD')
        if move not in self.currentmoves:
            return (0, (), (), 'invalid')
        if self.currentmoves[move] == 0:
            return (0, (), (), 'nopp')
        if self.status.count('recha') > 0:
            return (0, (), (), 'recharging')
        if self.status.count('para'):
            if random.randint(0,3) == 0:
                return (0, (), (), 'paralyzed')
        if self.status.count('fli') > 0:
            return (0, (), (), 'flinched')
        if self.status.count('frz') > 0:
            return (0, (), (), 'frozen')
        if self.status.count('con') > 0:
            self.conctr -= 1
            if random.randint(0,1) == 0:
                self.defend((40 * self.atk), (), (), '')
                return (0, (), (), 'confused')
        #decrement pp now
        self.currentmoves[move] -= 1
        #handle accuracy
        if 'acc' in movedict:
            if random.randint(0, 99) > movedict['acc']:
                return (0, (), (), 'miss')
        else:
            if random.randint(0, 255) == 0:
                return (0, (), (), 'gen1miss')
        if 'status' in movedict:
            status.extend(movedict['status'])
        #handle updates to own status
        if 'selfstatus' in movedict:
            for i in range(0, len(movedict['selfstatus']), 2):
                if random.randint(0, 99) < movedict['selfstatus'][i + 1]:
                    self.status.append(movedict['selfstatus'][i])
                    addedstatus.append(movedict['selfstatus'][i])
                    if movedict['selfstatus'][i] == 'recha':
                        self.recctr = 2
            self.crunch_status()
        #actually deal with the attack
        return (damage, status, addedstatus, info)

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

    #removes statuses from the critter. Takes a tuple of keywords as input
    def remove_status(self, statuses):
        self.status = [stat for stat in self.status if stat not in statuses]

    def get_speed(self):
        self.crunch_status()
        return self.spd * ((2 + self.status.count('spdup')) / (2 + self.status.count('spddn')))

    #update stats and deal with burn dmg and such at the end of turn
    def update_status(self): # TODO: complete log messaging
        result = []
        if len(self.status) > 0:
            removestats = []
            if self.status.count('fli') > 0:
                self.status = [stat for stat in self.status if stat != 'fli']
                # result.append('?') # TODO: what does this mean?
            for stat in self.status:
                if stat == 'brn':
                    self.currenthp -= int(self.hp / 8)
                    result.append('brn', '{} took damage from burn'.format(self.name))
                elif stat == 'psn':
                    self.currenthp -= int(self.hp / 8)
                    result.append('psn', '{} took damage from poison'.format(self.name))
                elif stat == 'con':
                    if self.conctr == 0:
                        removestats.append('con')
                elif stat == 'slp':
                    self.slpctr -= 1
                    if self.slpctr == 0:
                        removestats.append('slp')
                elif stat == 'recha':
                    self.recctr -= 1
                    if self.recctr == 0:
                        removestats.append('recha')
            self.remove_status(removestats)
        if self.currenthp < 1:
            self.currenthp = 0
            self.dead = True
            return ('DEAD', '{} died'.format(self.name))
        return result
            
    def get_move_list(self):
        return list(self.currentmoves.keys())
    
    def get_move_by_num(self, num):
        if num < len(self.currentmoves):
            return list(self.currentmoves.keys())[num]
        return None