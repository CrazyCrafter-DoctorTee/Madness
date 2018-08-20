import sys
from unittest import mock
from unittest.mock import patch

sys.path.append('..')

from madness import enemy

@patch('time.time')
def test_init(timeMock):
    timeMock.return_value = 'currTime'
    cords = [0, 0]
    enemy0 = enemy.Enemy('image', 'gameMap', cords)
    assert enemy0.image == 'image'
    assert enemy0.map == 'gameMap'
    assert enemy0.cords == [0, 0]
    cords[0] += 1
    assert enemy0.cords == [0, 0]
    assert enemy0.lastMove == 'currTime'

@patch('random.choice')
@patch('time.time')
def test_move(timeMock, choiceMock):
    timeMock.return_value = 300
    mapMock = mock.Mock()
    enemy0 = enemy.Enemy('image', mapMock, [0, 0])
    enemy0.move()
    assert enemy0.cords == [0, 0]
    
    choiceMock.side_effect = ['l', 'd']
    mapMock.get_movement.side_effect = [0, 32]
    timeMock.return_value = 301
    enemy0.move()
    assert enemy0.cords == [0, 32]