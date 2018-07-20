import iomanager
import critter
import pygame

#use this file for unit test scenario startup
ioguy = iomanager.IOManager('assets/config.cfg')
doge = critter.Critter('doge', ioguy, 1)
print(doge.currentmoves)
doge.addexp(1500)
print(doge.lvl)
