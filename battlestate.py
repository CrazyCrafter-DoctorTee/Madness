import random
import time

import gamestate

class BattleState(gamestate.GameState):
    
    def __init__(self, screen, fighter, aifighter):
        self.fighter = fighter
        self.aifighter = aifighter
        self.playerCreatures = fighter.creatures
        self.aiPlayerCreatures = aifighter.creatures
        self.print_colors()
    
    def print_colors(self):
        stime = time.time()
        lastChange = 0
        last_color = [0, 0, 0]
        while time.time() < stime + 3:
            if time.time() > lastChange + 0.2:
                i = random.randrange(0,2)
                last_color[i] = (last_color[i] + 99) % 256
                self.screen.fill(last_color)
                
    def process_input(self):
        return 'battle'
    
    def make_actions(self):
        pass
    
    def draw(self):
        pass
    
                