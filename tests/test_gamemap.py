import sys

sys.path.append('..')

import gamemap

def test_ctor():
    gameMap = gamemap.GameMap('largemap.map', (32, 32))
    assert gameMap.tileDims == (32, 32)

def test_generate_template():
    gameMap = gamemap.GameMap('largemap.map', (32, 32))
    gameMap.generate_template('smallmap.map')
    assert gameMap.dims == (6, 6)
    assert gameMap.tiles[0] == ['r','p','p','p','p','g']
    
def test_get_tile_dims():
    gameMap = gamemap.GameMap('largemap.map', (32, 32))
    assert gameMap.get_tile_dims(64, 64, (1280, 960)) == (2, 42, 2, 32)
    assert gameMap.get_tile_dims(64, 64, (1279, 959)) == (2, 41, 2, 31)
    assert gameMap.get_tile_dims(63, 63, (1279, 959)) == (1, 41, 1, 31)
    assert gameMap.get_tile_dims(10, 10, (100, 100)) == (0, 4, 0, 4)
    
def test_get_drawing_info():
    gameMap = gamemap.GameMap('largemap.map', (32, 32))
    