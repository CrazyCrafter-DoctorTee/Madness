# NOTE: wrapper functions in battleHandler: get_critter_moves, get_critters,
# get_critter_hps, get_targets, and get_switch_options are not currently tested
import pytest
import sys
from unittest import mock
from unittest.mock import patch

sys.path.append('..')

from madness import aifighter
from madness import battle

# =============================================================================
# BattleInfo tests
# =============================================================================

def test_battle_info_init():
    battleInfo = battle.BattleInfo('fighter', 'ai', 'crits')
    assert battleInfo.fighter == 'fighter'
    assert battleInfo.aiFighter == 'ai'
    assert battleInfo.critters == 'crits'
    
def test_get_critter_names():
    crit0Mock = mock.Mock()
    crit0Mock.name = 'crit0'
    crit3Mock = mock.Mock()
    crit3Mock.name = 'crit3'
    battleInfo = battle.BattleInfo('fighter', 'ai', 
                                   [crit0Mock, None, None, crit3Mock])
    assert battleInfo.get_critter_names() == ['crit0', '', '', 'crit3']
    
def test_get_critter_hps():
    crit0Mock = mock.Mock()
    crit0Mock.currenthp = 30
    crit2Mock = mock.Mock()
    crit2Mock.currenthp = 40
    battleInfo = battle.BattleInfo('fighter', 'ai', 
                                   [crit0Mock, None, crit2Mock, None])
    assert battleInfo.get_critter_hps() == ['30', '', '40', '']
    
def test_get_critter_moves():
    crit0Mock = mock.Mock()
    crit0Mock.get_move_list.return_value = 'move list'
    battleInfo = battle.BattleInfo('fighter', 'ai', [crit0Mock, None, None, None])
    assert battleInfo.get_critter_moves(0) == 'move list'
    assert battleInfo.get_critter_moves(1) == None
    
def test_get_targets():
    crit1Mock = mock.Mock()
    crit1Mock.name = 'crit1'
    crit2Mock = mock.Mock()
    crit2Mock.name = 'crit2'
    crit3Mock = mock.Mock()
    crit3Mock.name = 'crit3'
    battleInfo = battle.BattleInfo('fighter', 'ai',
                                   [None, crit1Mock, crit2Mock, crit3Mock])
    assert battleInfo.get_targets(1) == ['', '', 'crit2', 'crit3']
    
def test_critter_leave():
    battleInfo = battle.BattleInfo('fighter', 'ai',
                                   ['crit0', 'crit1', 'crit2', 'crit3'])
    battleInfo.critter_leave(2)
    assert battleInfo.critters == ['crit0', 'crit1', None, 'crit3']
    
def test_critter_switch_options():
    crit0Mock = mock.Mock()
    crit1Mock = mock.Mock()
    crit2Mock = mock.Mock()
    crit3Mock = mock.Mock()
    crit4Mock = mock.Mock()
    fighterMock = mock.Mock()
    fighterMock.critters = [crit0Mock, crit1Mock, crit2Mock, crit3Mock, crit4Mock]
    battleInfo = battle.BattleInfo(fighterMock, 'ai', 
                                   [crit2Mock, crit0Mock, 'aiCrit0', 'aiCrit1'])
    assert battleInfo.critter_switch_options() == [crit1Mock, crit3Mock, crit4Mock]
    
    fighterMock.critters = [crit0Mock, crit2Mock]
    assert battleInfo.critter_switch_options() == []
    
    fighterMock.critters = []
    assert battleInfo.critter_switch_options() == []

def test_perform_switch():
    crit0Mock = mock.Mock()
    crit1Mock = mock.Mock()
    crit2Mock = mock.Mock()
    fighterMock = mock.Mock()
    fighterMock.critters = [crit0Mock, crit1Mock, crit2Mock]
    battleInfo = battle.BattleInfo(fighterMock, 'ai',
                                   [crit0Mock, None, 'aicrit0', None])
    battleInfo.perform_switch(0, 1)
    assert battleInfo.critters == [crit2Mock, None, 'aicrit0', None]
    
    battleInfo.perform_switch(1, 0)
    assert battleInfo.critters == [crit2Mock, crit0Mock, 'aicrit0', None]
    
    with pytest.raises(Exception):
        assert battleInfo.perform_switch(0, 1)
        
def test_valid_critter_info():
    battleInfo = battle.BattleInfo('fighter', 'ai',
                                   ['crit0', None, None, 'crit3'])
    assert battleInfo.valid_critter(0) == True
    assert battleInfo.valid_critter(1) == False
    assert battleInfo.valid_critter(2) == False
    assert battleInfo.valid_critter(3) == True
    assert battleInfo.valid_critter(4) == False # out of bounds
    
def test_vaild_switch_info():
    crit0Mock = mock.Mock()
    crit1Mock = mock.Mock()
    crit2Mock = mock.Mock()
    crit3Mock = mock.Mock()
    fighterMock = mock.Mock()
    fighterMock.critters = [crit0Mock, crit1Mock, crit2Mock, crit3Mock]
    battleInfo = battle.BattleInfo(fighterMock, 'ai',
                                   [crit1Mock, crit3Mock, None, 'aicrit0'])
    assert battleInfo.valid_switch(0, 0) == True
    assert battleInfo.valid_switch(1, 1) == True
    assert battleInfo.valid_switch(0, 2) == False
    with pytest.raises(Exception):
        battleInfo.valid_switch(2, 0)
        
def test_determine_winner():
    fighterMock = mock.Mock()
    aiMock = mock.Mock()
    battleInfo = battle.BattleInfo(fighterMock, aiMock, [])
    fighterMock.has_playable_critters.return_value = True
    aiMock.has_playable_critters.return_vale = True
    assert battleInfo.determine_winner() == None
    
    fighterMock.has_playable_critters.return_value = False
    assert battleInfo.determine_winner() == 'ai'
    
    aiMock.has_playable_critters.return_value = False
    assert battleInfo.determine_winner() == 'both'
    
    fighterMock.has_playable_critters.return_value = True
    assert battleInfo.determine_winner() == 'fighter'
    
def test_switch_defender():
    battleInfo = battle.BattleInfo('fighter', 'ai', [])
    assert battleInfo.switch_defender(0) == 1
    assert battleInfo.switch_defender(1) == 0
    assert battleInfo.switch_defender(2) == 3
    assert battleInfo.switch_defender(3) == 2
    
def test_is_attacking_enemy():
    battleInfo = battle.BattleInfo('fighter', 'ai', [])
    assert battleInfo.is_attacking_enemy(0, 1) == False
    assert battleInfo.is_attacking_enemy(0, 2) == True
    assert battleInfo.is_attacking_enemy(1, 0) == False
    assert battleInfo.is_attacking_enemy(1, 3) == True
    assert battleInfo.is_attacking_enemy(2, 0) == True
    assert battleInfo.is_attacking_enemy(2, 3) == False
    assert battleInfo.is_attacking_enemy(3, 1) == True
    assert battleInfo.is_attacking_enemy(3, 2) == False
    
def test_get_defender():
    battleInfo = battle.BattleInfo('fighter', 'ai', ['crit0', None, 'crit2', None])
    assert battleInfo.get_defender(0, 2) == 2
    assert battleInfo.get_defender(0, 1) == 1
    assert battleInfo.get_defender(0, 3) == 2
    assert battleInfo.get_defender(2, 1) == 0
    assert battleInfo.get_defender(2, 3) == 3

def test_execute_action():
    crit0Mock = mock.Mock()
    crit1Mock = mock.Mock()
    crit2Mock = mock.Mock()
    critSwitchMock = mock.Mock()
    fighterMock = mock.Mock()
    fighterMock.critters = [crit0Mock, crit1Mock, critSwitchMock]
    battleInfo = battle.BattleInfo(fighterMock, 'ai', 
                                   [crit0Mock, critSwitchMock, crit2Mock, None])
    assert battleInfo.execute_action((1, 0, -1)) == (0, 'Switched', '')
    assert battleInfo.critters == [crit0Mock, crit1Mock, crit2Mock, None]
    
    crit0Mock.attack.return_value = 'attack info'
    crit2Mock.defend.return_value = 'defend info'
    crit2Mock.dead = True
    assert battleInfo.execute_action((0, 3, 'move')) == 'defend info'
    crit0Mock.attack.assert_called_with('move')
    crit2Mock.defend.assert_called_with('attack info')
    assert battleInfo.critters == [crit0Mock, crit1Mock, None, None]
    
@patch('random.uniform')
def test_get_ordered_turns(randomMock):
    crit0Mock = mock.Mock()
    crit0Mock.get_speed.return_value = 50
    crit1Mock = mock.Mock()
    crit1Mock.get_speed.return_value = 70
    crit2Mock = mock.Mock()
    crit2Mock.get_speed.return_value = 30
    crit3Mock = mock.Mock()
    crit3Mock.get_speed.return_value = 50
    actions = [(0, 2, 'bite'), (1, 0, -1), (2, 0, 'growl'), (3, 0, 'tackle')]
    randomMock.side_effect = [0.1, 0.6, 0.2, 0.8]
    battleInfo = battle.BattleInfo('fighter', 'ai', 
                                   [crit0Mock, crit1Mock, crit2Mock, crit3Mock])
    assert battleInfo.get_ordered_turns(actions) == \
        [(1, 0, -1), (3, 0, 'tackle'), (0, 2, 'bite'), (2, 0, 'growl')]

@patch('random.uniform')        
def test_get_critter_spd_order(randomMock):
    crit1Mock = mock.Mock()
    crit1Mock.get_speed.return_value = 40
    crit2Mock = mock.Mock()
    crit2Mock.get_speed.return_value = 40
    crit3Mock = mock.Mock()
    crit3Mock.get_speed.return_value = 50
    randomMock.side_effect = [0.1, 0.2, 0.6]
    battleInfo = battle.BattleInfo('fighter', 'ai', 
                               [None, crit1Mock, crit2Mock, crit3Mock])
    assert battleInfo.get_critter_spd_order() == \
        [crit3Mock, crit2Mock, crit1Mock] 

# =============================================================================
# BattleHandler Tests
# =============================================================================

def create_handler():
    fighterMock = mock.Mock()
    aiMock = mock.Mock()
    handler = battle.BattleHandler(fighterMock, aiMock)
    return handler

def test_battle_handler_init():
    fighterMock = mock.Mock()
    fighterMock.get_start_critters.return_value = ['crit0', 'crit1']
    aiMock = mock.Mock()
    aiMock.get_start_critters.return_value = ['crit2', 'crit3']
    handler = battle.BattleHandler(fighterMock, aiMock)
    assert handler.fighter == fighterMock
    assert handler.aiFighter == aiMock
    assert handler.battleInfo.fighter == fighterMock
    assert handler.battleInfo.aiFighter == aiMock
    assert handler.battleInfo.critters == ['crit0', 'crit1', 'crit2', 'crit3']
    assert handler.turnActions == []
    assert handler.turnInitialized == False
    assert handler.endInitialized == False

def test_end_turn():
    handler = create_handler()
    handler.turnActions = ['action1']
    handler.turnInitialized = True
    handler.endInitialized = True
    handler.end_turn()
    assert handler.turnActions == []
    assert handler.turnInitialized == False
    assert handler.endInitialized == False
    
def test_valid_move():
    handler = create_handler()
    battleInfoMock = mock.Mock()
    battleInfoMock.get_critter_moves.return_value = ['move0', 'move1']
    handler.battleInfo = battleInfoMock
    assert handler.valid_move(0, 1) == True
    assert handler.valid_move(0, 2) == False
    battleInfoMock.get_critter_moves.assert_called_with(0)
    
def test_valid_target():
    handler = create_handler()
    assert handler.valid_target(0, 1) == True
    assert handler.valid_target(0, 3) == True
    assert handler.valid_target(0, 0) == False
    assert handler.valid_target(0, 4) == False
    
def test_valid_critter_handler():
    handler = create_handler()
    battleInfoMock = mock.Mock()
    battleInfoMock.valid_critter.return_value = True
    handler.battleInfo = battleInfoMock
    assert handler.valid_critter(1) == True
    battleInfoMock.valid_critter.assert_called_once_with(1)
    
def test_vaild_switch_handler():
    handler = create_handler()
    battleInfoMock = mock.Mock()
    battleInfoMock.valid_switch.return_value = True
    handler.battleInfo = battleInfoMock
    assert handler.valid_switch(0, 1) == True
    battleInfoMock.valid_switch.assert_called_once_with(0, 1)

@patch.object(battle.BattleHandler, 'valid_switch')
@patch.object(battle.BattleHandler, 'valid_critter')
@patch.object(battle.BattleHandler, 'valid_target')    
def test_add_action(targetMock, critMock, switchMock):
    handler = create_handler()
    switchMock.return_value = True
    handler.add_action(0, 1, -1)
    assert handler.turnActions[-1] == (0, 1, -1)
    
    switchMock.return_value = False
    with pytest.raises(Exception):
        handler.add_action(0, 1, -1)
    
    targetMock.return_value = True
    critMock.return_value = True
    handler.add_action(0, 1, 'move')
    assert handler.turnActions[-1] == (0, 1, 'move')
    
    targetMock.return_value = False
    with pytest.raises(Exception):
        handler.add_action(0, 1, 'move')
        
    targetMock.return_value = True
    critMock.return_value = False
    with pytest.raises(Exception):
        handler.add_action(0, 1, 'move')
        
def test_get_battle_return_status():
    handler = create_handler()
    battleInfoMock = mock.Mock()
    handler.battleInfo = battleInfoMock
    handler.actionQueue = mock.Mock()
    handler.actionQueue.empty.return_value = False
    battleInfoMock.determine_winner.return_value = None
    assert handler.get_battle_return_status() == 0
    
    handler.actionQueue.empty.return_value = True
    assert handler.get_battle_return_status() == 1
    
    battleInfoMock.determine_winner.return_value = 'fighter'
    assert handler.get_battle_return_status() == 2
    
    battleInfoMock.determine_winner.return_value = 'ai'
    assert handler.get_battle_return_status() == 3
    
    battleInfoMock.determine_winner.return_value = 'both'
    assert handler.get_battle_return_status() == 4

@patch.object(battle.BattleHandler, 'initialize_turn')
@patch.object(battle.BattleHandler, 'get_battle_return_status')
def test_next_step(returnMock, initTurnMock):
    handler = create_handler()
    handler.turnInitialized = False
    battleInfoMock = mock.Mock()
    battleInfoMock.execute_action.side_effect = [None, None, 'status']
    handler.battleInfo = battleInfoMock
    queueMock = mock.Mock()
    queueMock.get.side_effect = ['action0', 'action1', 'action2']
    queueMock.empty.return_value = False
    handler.actionQueue = queueMock
    returnMock.return_value = 'battle status'
    assert handler.next_step() == 'battle status'
    battleInfoMock.execute_action.assert_any_call('action0')
    battleInfoMock.execute_action.assert_any_call('action1')
    battleInfoMock.execute_action.assert_called_with('action2')#should be last call
    initTurnMock.assert_called_once()
    
    queueMock.empty.return_value = True
    assert handler.next_step() == 'battle status'

@patch.object(battle.BattleHandler, 'initialize_end')
@patch.object(battle.BattleHandler, 'get_battle_return_status')
def test_end_action(returnMock, initEndMock):
    handler = create_handler()
    crit0Mock = mock.Mock()
    crit0Mock.update_status.return_value = None
    crit1Mock = mock.Mock()
    crit1Mock.update_status.return_value = 'status'
    handler.critterQueue = mock.Mock()
    handler.critterQueue.get.side_effect = [crit0Mock, crit1Mock]
    handler.critterQueue.empty.return_value = False
    returnMock.return_value = 'battle status'
    assert handler.end_action() == 'battle status'
    crit0Mock.update_status.assert_called_once()
    crit1Mock.update_status.assert_called_once()
    initEndMock.assert_called_once
    
    handler.critterQueue.empty.return_value = True
    assert handler.end_action() == 'battle status'
    
def test_initialize_turn():
    handler = create_handler()
    handler.turnActions = ['action3', 'action1']
    handler.aiFighter.get_actions.return_value = ['action2', 'action0']
    handler.battleInfo = mock.Mock()
    handler.battleInfo.get_ordered_turns.side_effect = sorted
    handler.turnInitialized = False
    handler.nextAction = 'Action'
    handler.initialize_turn()
    assert handler.turnInitialized == True
    assert handler.nextAction == None
    for i in range(4):
        action = handler.actionQueue.get(block=False)
        assert action == 'action{}'.format(i)
    assert handler.actionQueue.empty()
    
def test_initialize_end():
    handler = create_handler()
    handler.battleInfo = mock.Mock()
    handler.battleInfo.get_critter_spd_order.return_value = ['crit0', 'crit1', 'crit2']
    handler.nextAction = 'Action'
    handler.endInitialized = False
    handler.initialize_end()
    assert handler.endInitialized == True
    assert handler.nextAction == None
    for i in range(3):
        crit = handler.critterQueue.get(block=False)
        assert crit == 'crit{}'.format(i)
    assert handler.critterQueue.empty()