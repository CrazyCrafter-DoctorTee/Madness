import random
import sys
from unittest import mock
from unittest.mock import patch

sys.path.append('..')

from madness import aifighter

def test_init():
    ai0 = aifighter.AIFighter()
    assert ai0.critters == []
    
    crits = ['crit0', 'crit1', 'crit2']
    ai1 = aifighter.AIFighter(crits)
    assert ai1.critters == ['crit0', 'crit1', 'crit2']
    crits.remove('crit2') # make sure it keeps a copy, not the original
    assert ai1.critters == ['crit0', 'crit1', 'crit2']

@patch('random.choice')
@patch('random.randrange')    
def test_get_actions(rangeMock, choiceMock):
    ai = aifighter.AIFighter()
    crits = [mock.Mock() for i in range(4)]
    crits[2].get_move_list.return_value = ['move0', 'move1', 'move2', 'move3']
    crits[3].get_move_list.return_value = ['move0', 'move1', 'move2']
    choiceMock.return_value = 0
    rangeMock.return_value = 1
    actions = ai.get_actions(crits)
    assert actions[0] == (2, 0, 1)
    assert actions[1] == (3, 0, 1)
    choiceMock.assert_called_with([0, 1])
    rangeMock.assert_any_call(4)
    rangeMock.assert_any_call(3)
    
def test_get_start_critters():
    ai = aifighter.AIFighter()
    assert ai.get_start_critters() == [None, None]
    
    crit0 = mock.Mock()
    crit1 = mock.Mock()
    crit2 = mock.Mock()
    ai.critters = [crit0]
    crit0.dead = False
    assert ai.get_start_critters() == [crit0, None]
    
    crit0.dead = True
    assert ai.get_start_critters() == [None, None]
    
    crit0.dead = False
    crit1.dead = False
    crit2.dead = False
    ai.critters = [crit0, crit1, crit2]
    assert ai.get_start_critters() == [crit0, crit1]
    
    crit1.dead = True
    assert ai.get_start_critters() == [crit0, crit2]
    
    crit0.dead = True
    assert ai.get_start_critters() == [crit2, None]
    
def test_has_playable_critters():
    ai = aifighter.AIFighter()
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