import os
import pytest
import sys
from unittest.mock import patch

sys.path.append('..')

from madness import gamemap

def setup_module(module):
    os.chdir(os.path.dirname(__file__))

def test_init():
    gameMap = gamemap.GameMap('largemap.map', (32, 32))
    assert gameMap.tileDims == (32, 32)

def test_generate_template():
    gameMap = gamemap.GameMap('largemap.map', (32, 32))
    gameMap.generate_template('smallmap.map')
    assert gameMap.dims == (6, 6)
    assert gameMap.tiles[0] == ['r','p','p','r','p','r']
    
def test_get_tile_dims():
    gameMap = gamemap.GameMap('largemap.map', (32, 32))
    assert gameMap.get_tile_dims(64, 64, (1280, 960)) == (2, 42, 2, 32)
    assert gameMap.get_tile_dims(64, 64, (1279, 959)) == (2, 41, 2, 31)
    assert gameMap.get_tile_dims(63, 63, (1279, 959)) == (1, 41, 1, 31)
    assert gameMap.get_tile_dims(10, 10, (100, 100)) == (0, 4, 0, 4)
    
def test_get_drawing_info():
    gameMap = gamemap.GameMap('largemap.map', (32, 32))
    info0 = gameMap.get_drawing_info((160, 96), (0, 0))
    assert info0[0][0] == ['g','g','b', 'g']
    assert len(info0[0]) == 6
    assert info0[1] == (0, 0)
    assert info0[2] == (32, 32)
    
    info1 = gameMap.get_drawing_info((100, 100), (0, 0))
    assert info1[0][0] == ['g','g','b','g']
    assert len(info1[0]) == 4
    assert info1[1] == (0, 0)
    assert info1[2] == (32, 32)
    
    info2 = gameMap.get_drawing_info((100, 100), (128, 128))
    assert info2[0][0] == ['g','b','g','g']
    assert len(info2[0]) == 4
    assert info2[1] == (0,0)
    assert info2[2] == (32, 32)
    
    info3 = gameMap.get_drawing_info((100, 100), (127, 127))
    assert info3[0][0] == ['g','g','g','t','g']
    assert len(info3[0]) == 5
    assert info3[1] == (31, 31)
    assert info3[2] == (32, 32)
    
def test_impassable():
    gameMap = gamemap.GameMap('smallmap.map', (32, 32))
    assert gameMap.impassable(0, 0) == True
    assert gameMap.impassable(1, 0) == False
    assert gameMap.impassable(5, 0) == False
    assert gameMap.impassable(4, 5) == True
    assert gameMap.impassable(5, 5) == True

@patch.object(gamemap.GameMap, 'impassable')
def test_get_movement(impassableMock):
    gameMap = gamemap.GameMap('smallmap.map', (32, 32))
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