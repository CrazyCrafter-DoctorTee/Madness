import iomanager
import critter
import pygame

#use this file for unit test scenario startup
ioguy = iomanager.IOManager('assets/config.cfg')
dog = critter.Critter('doge', ioguy, currentmoves={'bork':1})
print(dog.currentmoves)
gato = critter.Critter('gato', ioguy)
dog.defend(gato.attack('bite'))
gato.defend(dog.attack('bork'))
print(dog.status)
print(gato.status)
print(dog.currentmoves)
attack = dog.attack('bork')
print(attack)
dog.defend(gato.attack('bite'))
gato.defend(attack)
print(dog.status)
print(gato.status)
print(dog.currentmoves)
