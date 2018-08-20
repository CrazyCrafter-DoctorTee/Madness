import sys
from unittest import mock
from unittest.mock import patch

sys.path.append('..')

from madness import critter
from madness import fighter

# NOTE: skipped test critter part because it is not clear how it should behave
@patch('madness.critter.Critter') # patched to avoid calls to iomanager
def test_init(critMock): 
    fight = fighter.Fighter('ioManager')
    assert fight.iomanager == 'ioManager'

@patch('madness.critter.Critter')    
def test_get_start_critters(critMock):
    fight = fighter.Fighter('ioManager')
    fight.critters = []
    assert fight.get_start_critters() == [None, None]
    
    crit0 = mock.Mock()
    crit1 = mock.Mock()
    crit2 = mock.Mock()
    fight.critters = [crit0]
    crit0.dead = False
    assert fight.get_start_critters() == [crit0, None]
    
    crit0.dead = True
    assert fight.get_start_critters() == [None, None]
    
    crit0.dead = False
    crit1.dead = False
    crit2.dead = False
    fight.critters = [crit0, crit1, crit2]
    assert fight.get_start_critters() == [crit0, crit1]
    
    crit1.dead = True
    assert fight.get_start_critters() == [crit0, crit2]
    
    crit0.dead = True
    assert fight.get_start_critters() == [crit2, None]

@patch('madness.critter.Critter')    
def test_has_playable_critters(critMock):
    ai = fighter.Fighter('ioManager')
    assert ai.has_playable_critters() == False
    
    crit0 = mock.Mock()
    crit1 = mock.Mock()
    crit0.dead = False
    ai.critters = [crit0]
    assert ai.has_playable_critters() == True
    
    crit0.dead = True
    assert ai.has_playable_critters() == False
    
    crit1.dead = False
    ai.critters = [crit0, crit1]
    assert ai.has_playable_critters() == True