import pygame
import midiutil
import random

class Musicbox:

    def __init__(self):
        pygame.mixer.init( 44100, -16, 1, 1024)
        self.scale = (0,2,4,5,7,9,11)
        self.home = 60

    def play_file(self, filename):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play(-1)

    def generate_file(self, filename):
        ofile = midiutil.MIDIFile(1)
        ofile.addTrackName(0,0,"Track")
        ofile.addTempo(0,0,300)
        self.populate(ofile, 80)
        binf = open(filename, 'wb')
        ofile.writeFile(binf)
        binf.close()

    def populate(self, midf, length):
        for i in range(0, length):
            midf.addNote(0,0,self.home + random.choice(self.scale),i,1,100)

    def test(self, fname):
        self.generate_file(fname)
        pygame.mixer.music.load(fname)
        pygame.mixer.music.play()
