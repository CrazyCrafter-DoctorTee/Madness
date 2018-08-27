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

@patch('random.randrange')    
def test_do_switch(rangeMock):
    ai = aifighter.AIFighter()
    crit0Mock = mock.Mock()
    crit0Mock.dead = False
    crit1Mock = mock.Mock()
    crit1Mock.dead = False
    crit2Mock = mock.Mock()
    crit2Mock.dead = True
    crit3Mock = mock.Mock()
    crit3Mock.dead = False
    ai.critters = [crit0Mock, crit1Mock, crit2Mock, crit3Mock]
    battleCrits = ['crit0', 'crit1', None, crit1Mock]
    rangeMock.return_value = 1
    assert ai.do_switch(battleCrits) == [crit3Mock]
    rangeMock.assert_called_with(2)
    
    battleCrits = ['crit0', 'crit1', None, None]
    rangeMock.return_value = 0
    assert ai.do_switch(battleCrits) == [crit0Mock, crit1Mock]
    
    battleCrits = [None, None, 'crit2', 'crit3']
    assert ai.do_switch(battleCrits) == []