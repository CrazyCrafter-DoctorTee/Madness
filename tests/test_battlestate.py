# NOTE: skipped print_colors, process_input, and draw
import pygame
import sys
from unittest import mock
from unittest.mock import patch

sys.path.append('..')

from madness import battlestate


@patch('madness.battle.BattleHandler')
@patch('madness.aifighter.AIFighter')
@patch.object(battlestate.BattleState, 'print_colors')
@patch.object(battlestate.BattleState, 'generate_ai_critters')
@patch.object(battlestate.BattleState, 'create_images')
def create_state(createMock, genMock, printMock, aiMock, handlerMock):
    ioMock = mock.Mock() 
    return battlestate.BattleState('screen', (1280, 640), ioMock, 'fighter')

@patch('madness.battle.BattleHandler')
@patch('madness.aifighter.AIFighter')
@patch.object(battlestate.BattleState, 'get_buttons')
@patch.object(battlestate.BattleState, 'print_colors')
@patch.object(battlestate.BattleState, 'generate_ai_critters')
@patch.object(battlestate.BattleState, 'create_images')
def test_init(createMock, genMock, printMock, buttonMock, aiMock, handlerMock):
    ioMock = mock.Mock()
    ioMock.get_data.return_value = 'images'
    aiMock.return_value = 'ai'
    state = battlestate.BattleState('screen', 'screenDims', ioMock, 'fighter')
    assert state.screen == 'screen'
    assert state.screenDims == 'screenDims'
    assert state.battleOver == False
    assert state.ioManager == ioMock
    assert state.step == ('move', 0)
    createMock.assert_called_with('images')
    handlerMock.assert_called_once_with('fighter', 'ai')
    buttonMock.assert_called_once()
    printMock.assert_called_once()
    assert state.stepFuncs == {'move' : state.select_move,
                         'target' : state.select_target,
                         'turn' : state.run_turn,
                         'end' : state.run_end,
                         'switch' : state.try_switch,
                         'enter' : state.try_enter}

@patch.object(battlestate.BattleState, 'determine_next_step')
@patch.object(battlestate.BattleState, 'get_buttons')
def test_process_key_action(buttonMock, deterMock):
    state = create_state()
    buttonMock.reset_mock()
    stepFuncMock = mock.Mock()
    stepFuncMock.return_value = 0
    state.stepFuncs = {'stepType' : stepFuncMock}
    state.step = ('stepType', 1)
    state.process_key_action(0)
    assert state.step == ('stepType', 1)
    deterMock.assert_not_called()
    buttonMock.assert_not_called()
    
    stepFuncMock.return_value = 1
    state.process_key_action(0)
    deterMock.assert_called_once()
    buttonMock.assert_called_once()
    state.step = ('stepType', 1)
    
    for i in range(2, 5):
        buttonMock.reset_mock()
        stepFuncMock.return_value = i
        state.battleOver = False
        state.process_key_action(0)
        assert state.battleOver == True
        
    buttonMock.reset_mock()
    stepFuncMock.return_value = 5
    state.process_key_action(0)
    assert state.step == ('switch', 1)
    buttonMock.assert_called_once()
    
    buttonMock.reset_mock()
    state.step = ('stepType', 1)
    stepFuncMock.return_value = 6
    state.process_key_action(0)
    assert state.step == ('enter', -1)
    buttonMock.assert_called_once()
    
def test_make_actions():
    state = create_state()
    assert state.make_actions() == 'battle'    
    state.battleOver = True
    assert state.make_actions() == 'map'    
    state.quit = True
    assert state.make_actions() == None