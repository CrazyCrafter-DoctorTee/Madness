"""import sys
from unittest import mock
from unittest.mock import patch

sys.path.append('..')

from madness import musicbox

@patch('random.choice')
def test_populate(choiceMock):
    choiceMock.side_effect = (3,4,2,5,6,1,3,0,3)
    mbox = Musicbox()
    ofile = midiutil.MIDIFile(1)
    ofile.addTrackName(0,0,"Track")
    ofile.addTempo(0,0,300)
    self.populate(ofile, 80)
    binf = open(filename, 'wb')
    ofile.writeFile(binf)
    binf.close()
"""
