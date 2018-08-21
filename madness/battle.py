import queue
import random

class BattleInfo(object):

    def __init__(self, fighter, aiFighter, critters):
        self.fighter = fighter
        self.aiFighter = aiFighter
        self.critters = critters

    def get_critter_names(self):
        names = []
        for c in self.critters:
            if c != None:
                names.append(c.name)
            else:
                names.append('')
        return names

    def get_critter_hps(self):
        hps = []
        for c in self.critters:
            if c != None:
                hps.append(str(c.currenthp))
            else:
                hps.append('')
        return hps

    def get_critter_moves(self, critPos):
        if self.critters[critPos] != None:
            return self.critters[critPos].get_move_list()
        return None

    def get_targets(self, critPos):
        targets = []
        for i in range(len(self.critters)):
            if self.critters[i] == None or i == critPos:
                targets.append('')
            else:
                targets.append(self.critters[i].name)
        return targets

    def critter_leave(self, critPos):
        self.critters[critPos] = None

    def critter_switch_options(self):
        options = []
        for c in self.fighter.critters:
            if (self.critters[0] is not c
                and self.critters[1] is not c):
                options.append(c)
        return options

    def perform_switch(self, critPos, newCrit):
        options = self.critter_switch_options()
        if newCrit < len(options):
            self.critters[critPos] = options[newCrit]
        else:
            raise Exception('{} is not a valid critter number!'.format(newCrit))

    def valid_critter(self, critPos):
        if critPos < 4:
            return self.critters[critPos] != None
        else:
            return False

    def valid_switch(self, critPos, switchNum):
        if critPos == 0 or critPos == 1:
            return switchNum < len(self.critter_switch_options())
        else:
            raise Exception('AI switch is not implemented')

    def determine_winner(self):
        fighterIsAlive = self.fighter.has_playable_critters()
        aiIsAlive = self.aiFighter.has_playable_critters()
        if fighterIsAlive and aiIsAlive:
            return None
        elif aiIsAlive:
            return 'ai'
        elif fighterIsAlive:
            return 'fighter'
        else:
            return 'both'

    def switch_defender(self, target):
        if target == 0:
            return 1
        elif target == 1:
            return 0
        elif target == 2:
            return 3
        elif target == 3:
            return 2
        else:
            return None

    def is_attacking_enemy(self, attPos, defPos):
        if attPos == 0 or attPos == 1:
            if defPos == 2 or defPos == 3:
                return True
            else:
                return False
        elif attPos == 2 or attPos == 3:
            if defPos == 0 or defPos == 1:
                return True
            else:
                return False

    def get_defender(self, attPos, defPos):
        if self.is_attacking_enemy(attPos, defPos):
            if self.critters[defPos] == None:
                return self.switch_defender(defPos)
            else:
                return defPos
        else:
            return defPos

    def execute_action(self, action):
        defendResult = []
        if action[2] == -1:
            self.perform_switch(action[0], action[1])
            defendResult = (0, 'Switched', '')
        elif self.critters[action[0]] != None:
            attacker = self.critters[action[0]]
            defendPos = self.get_defender(action[0], action[1])
            defender = self.critters[defendPos]
            move = action[2]
            defendResult.append('{} attacked {} with {}'.format(
                    attacker.name, defender.name, move))
            moveResult = attacker.attack(move)
            if defender != None:
                for msg in defender.defend(moveResult):
                    defendResult.append(msg)
                if defender.dead:
                    self.critter_leave(defendPos)
        return defendResult


    def get_ordered_turns(self, actionList):
        # sorted is stable, will be sorted in reverse order of original sort,
        # so return will be ordered by action priority, then speed
        temp = sorted(actionList,
                key=lambda x: self.critters[x[0]].get_speed()+random.uniform(0,1),
                reverse=True)
        return sorted(temp, key=lambda x: 0 if x[2] == -1 else 1)

    def get_critter_spd_order(self):
        aliveCritters = []
        for c in self.critters:
            if c != None:
                aliveCritters.append(c)
        return sorted(aliveCritters,
                       key=lambda x: x.get_speed()+random.uniform(0,1),
                       reverse=True)

# TODO: give up fighter/aifighter, so it's not in battle info, and handeler
class BattleHandler(object):

    def __init__(self, fighter, aiFighter):
        self.fighter = fighter
        self.aiFighter = aiFighter
        critters = self.fighter.get_start_critters()
        critters.extend(self.aiFighter.get_start_critters())
        self.battleInfo = BattleInfo(fighter, aiFighter, critters)
        self.end_turn()

    def end_turn(self):
        self.turnActions = []
        self.turnInitialized = False
        self.endInitialized = False
        self.logMsg = ''
        self.logQueue = queue.Queue()

    def valid_move(self, critPos, move):
        moves = self.battleInfo.get_critter_moves(critPos)
        return move < len(moves)

    def valid_target(self, critPos, target):
        if critPos != target and target < 4:
            return True
        return False

    def valid_critter(self, critPos):
        return self.battleInfo.valid_critter(critPos)

    def valid_switch(self, critPos, switchNum):
        return self.battleInfo.valid_switch(critPos, switchNum)

    def add_action(self, critPos, target, move):
        if move == -1:
            if self.valid_switch(critPos, target):
                self.turnActions.append((critPos, target, move))
            else:
                raise Exception('Invalid switch tried!')
        elif self.valid_critter(critPos) and self.valid_target(critPos, target):
            self.turnActions.append((critPos, target, move))
        else:
            raise Exception('Invalid action added!')

    def get_battle_return_status(self):
        winner = self.battleInfo.determine_winner()
        if winner == 'fighter':
            return 2
        elif winner == 'ai':
            return 3
        elif winner == 'both':
            return 4
        elif self.actionQueue.empty():
            self.end_turn()
            return 1
        else:
            return 0

    def next_step(self):
        if self.turnInitialized == False:
            self.initialize_turn()
        if self.logQueue.empty() == False:
            self.logMsg = self.logQueue.get(block=False)
            return self.get_battle_return_status()
        turnStatus = None
        while turnStatus == None and not self.actionQueue.empty():
            self.nextAction = self.actionQueue.get(block=False)
            turnStatus = self.battleInfo.execute_action(self.nextAction)
        if turnStatus == None:
            self.logMsg = ''
        else:
            for msg in turnStatus:
                self.logQueue.put(msg)
            self.logMsg = self.logQueue.get(block=True)
        return self.get_battle_return_status()

    def end_action(self):
        status = None
        if self.endInitialized == False:
            self.initialize_end()
        status = None
        while status == None and not self.critterQueue.empty():
            self.nextCritter = self.critterQueue.get(block=False)
            status = self.nextCritter.update_status()
        if status == None:
            self.logMsg = ''
        else:
            self.logMsg = status[-1]
        return self.get_battle_return_status()
    
    def initialize_turn(self):
        self.actionQueue = queue.Queue()
        self.nextAction = None
        self.turnActions.extend(self.aiFighter.get_actions(self.battleInfo.critters))
        for a in self.battleInfo.get_ordered_turns(self.turnActions):
            self.actionQueue.put(a)
        self.turnInitialized = True

    def initialize_end(self):
        self.critterQueue = queue.Queue()
        self.nextAction = None
        for c in self.battleInfo.get_critter_spd_order():
            self.critterQueue.put(c)
        self.endInitialized = True

    def get_critter_moves(self, critPos):
        return self.battleInfo.get_critter_moves(critPos)

    def get_critters(self):
        return self.battleInfo.get_critter_names()

    def get_critter_hps(self):
        return self.battleInfo.get_critter_hps()

    def get_targets(self, critPos):
        return self.battleInfo.get_targets(critPos)

    def get_switch_options(self):
        return self.battleInfo.critter_switch_options()
