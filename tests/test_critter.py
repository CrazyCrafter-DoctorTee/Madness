import sys
from unittest import mock

sys.path.append('..')

from madness import critter


def create_critter():
    
    def new_get_data(arg0, arg1, infoType):
        if infoType == 'stats':
            return {'hp' : 70,
                    'atk' : 50,
                    'def' : 60,
                    'spd' : 30}
        elif infoType == 'moves':
            return {'move0' : 1,
                    'move1' : 1,
                    'move2' : 3,
                    'move3' : 4,
                    'move5' : 5}
            
    ioManagerMock = mock.Mock()
    ioManagerMock.get_data.side_effect = new_get_data
    return critter.Critter('name', ioManagerMock)

def test_crunch_status():
    crit = create_critter()
    crit.status = ['brn', 'spdup', 'defup', 'atkdn']
    crit.crunch_status()
    assert crit.status == ['brn', 'spdup', 'defup', 'atkdn']
    
    crit.status = ['brn', 'spdup', 'spdup', 'atkup', 'spddn', 'defup',
                   'atkdn']
    crit.crunch_status()
    assert crit.status.count('spdup') == 1
    assert crit.status.count('spddn') == 0
    assert crit.status.count('attkup') == 0
    assert crit.status.count('attkdn') == 0
    assert crit.status.count('defup') == 1
    assert crit.status.count('defdn') == 0
    assert crit.status.count('brn') == 1