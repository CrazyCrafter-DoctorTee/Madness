import pytest
import sys
from unittest import mock
from unittest.mock import patch

sys.path.append('..')

from madness import aifighter
from madness import critter
from madness import fighter

def create_fighter(className):
    if className == 'ai':
        with patch('madness.critter.Critter'):
            return aifighter.AIFighter()
    else:
        with patch('madness.critter.Critter'):
            return fighter.Fighter('ioManager')

# NOTE: skipped test critter part because it is not clear how it should behave
@patch('madness.critter.Critter') # patched to avoid calls to iomanager
def test_init(critMock): 
    fight = fighter.Fighter('ioManager')
    assert fight.iomanager == 'ioManager'
    assert len(fight.critters) == 3
    
    fight1 = fighter.Fighter('ioManager', ['crit0', 'crit1', 'crit2', 'crit3'])
    assert fight1.critters == ['crit0', 'crit1', 'crit2', 'crit3']

@pytest.mark.parametrize('className', ['fighter', 'ai']) 
def test_get_start_critters(className):
    fight = create_fighter(className)
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

@pytest.mark.parametrize('className', ['fighter', 'ai'])    
def test_has_playable_critters(className):
    fighter = create_fighter(className)
    assert fighter.has_playable_critters() == False
    
    crit0 = mock.Mock()
    crit1 = mock.Mock()
    crit0.dead = False
    fighter.critters = [crit0]
    assert fighter.has_playable_critters() == True
    
    crit0.dead = True
    assert fighter.has_playable_critters() == False
    
    crit1.dead = False
    fighter.critters = [crit0, crit1]
    assert fighter.has_playable_critters() == True

@pytest.mark.parametrize('className', ['fighter', 'ai'])    
def test_alive_critter_count(className):
    fight = create_fighter(className)
    fight.critters = []
    assert fight.alive_critter_count() == 0
    
    crit0Mock = mock.Mock()
    crit0Mock.dead = False
    crit1Mock = mock.Mock()
    crit1Mock.dead = False
    fight.critters = [crit0Mock, crit1Mock]
    assert fight.alive_critter_count() == 2
    
    crit0Mock.dead = True
    assert fight.alive_critter_count() == 1