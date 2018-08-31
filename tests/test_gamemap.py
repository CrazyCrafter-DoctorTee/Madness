import os
import pytest
import sys
from unittest import mock
from unittest.mock import patch

sys.path.append('..')

from madness import gamemap
from madness import mapgen


@patch('madness.mapgen.Mapgenerator')
def create_map(genMock):
    generatorMock = mock.Mock()
    generatorMock.generate_map.return_value = \
    [['r','p','p','p','p','g'],
     ['p','p','g','g','p','t'],
     ['p','p','g','b','p','t'],
     ['r','p','p','g','p','p'],
     ['p','p','p','g','g','g'],
     ['t','p','p','p','t','b']]
    genMock.return_value = generatorMock
    gameMap = gamemap.GameMap((32, 32), 6)
    return gameMap

@patch('madness.mapgen.Mapgenerator')
@patch.object(gamemap.GameMap, 'generate_template')
def test_init(tempMock, genMock):
    genMock.return_value = 'generator'
    gameMap = gamemap.GameMap()
    assert gameMap.tileDims == (32, 32)
    assert gameMap.tileNum == 80
    assert gameMap.maxDims == (32*79, 32*79)
    assert gameMap.generator == 'generator'
    tempMock.assert_called_once()
    genMock.assert_called_once_with(80)

    gameMap1 = gamemap.GameMap((2,2), 10)
    assert gameMap1.tileDims == (2, 2)
    assert gameMap1.maxDims == (2*9, 2*9)
    assert gameMap1.tileNum == 10

def test_generate_template():
    gameMap = create_map()
    gameMap.generate_template()
    assert gameMap.tiles[0] == ['r','p','p','p','p','g']
    
def test_get_tile_dims():
    gameMap = gamemap.GameMap((32, 32))
    assert gameMap.get_tile_dims(64, 64, (1280, 960)) == (2, 42, 2, 32)
    assert gameMap.get_tile_dims(64, 64, (1279, 959)) == (2, 41, 2, 31)
    assert gameMap.get_tile_dims(63, 63, (1279, 959)) == (1, 41, 1, 31)
    assert gameMap.get_tile_dims(10, 10, (100, 100)) == (0, 4, 0, 4)
    
def test_get_drawing_info():
    gameMap = create_map()
    info0 = gameMap.get_drawing_info((160, 96), (0, 0))
    assert info0[0][0] == ['r','p','p','p']
    assert len(info0[0]) == 6
    assert info0[1] == (0, 0)
    assert info0[2] == (32, 32)
    
    info1 = gameMap.get_drawing_info((100, 100), (0, 0))
    assert info1[0][0] == ['r','p','p','p']
    assert len(info1[0]) == 4
    assert info1[1] == (0, 0)
    assert info1[2] == (32, 32)
    
    info2 = gameMap.get_drawing_info((100, 100), (32, 32))
    assert info2[0][0] == ['p','g','g','p']
    assert len(info2[0]) == 4
    assert info2[1] == (0,0)
    assert info2[2] == (32, 32)
    
    info3 = gameMap.get_drawing_info((100, 100), (63, 63))
    assert info3[0][0] == ['p','g','g','p','t']
    assert len(info3[0]) == 5
    assert info3[1] == (31, 31)
    assert info3[2] == (32, 32)
    
def test_impassable():
    gameMap = create_map()
    assert gameMap.impassable(0, 0) == True
    assert gameMap.impassable(1, 0) == False
    assert gameMap.impassable(5, 0) == True
    assert gameMap.impassable(4, 5) == False
    assert gameMap.impassable(5, 5) == True

@patch.object(gamemap.GameMap, 'impassable')
def test_get_movement(impassableMock):
    gameMap = create_map()
    impassableMock.return_value = False
    assert gameMap.get_movement((0, 0), 'l') == 0
    assert gameMap.get_movement((0, 0), 'u') == 0
    assert gameMap.get_movement((0, 0), 'd') == 32
    assert gameMap.get_movement((0, 0), 'r') == 32
    
    assert gameMap.get_movement((1, 1), 'l') == 0
    assert gameMap.get_movement((32, 32), 'u') == -32
    impassableMock.return_value = True
    assert gameMap.get_movement((1, 1), 'd') == 0
    assert gameMap.get_movement((1, 1), 'r') == 0