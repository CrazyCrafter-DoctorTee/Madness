import sys

sys.path.append('..')

import camera

def test_ctor():
    cam = camera.Camera((764, 1280), (4064, 4064))
    assert cam.screenDims == (764, 1280)
    assert cam.maxDims == (4064, 4064)
    
def test_generate_offset():
    cam = camera.Camera((764, 1280), (4064, 4064))
    cam.generate_offset((1600, 1280))
    assert cam.topLeft == (1218, 640)
    cam.screenDims = (756, 1260)
    cam.generate_offset((2240, 2240))
    assert cam.topLeft == (1862, 1610)
    cam.generate_offset((320, 320))
    assert cam.topLeft == (320, 320)