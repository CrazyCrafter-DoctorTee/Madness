import sys

sys.path.append('..')

from gamemanager import button

def test_init():
    button0 = button.Button('image', 'words', (0, 0.5, 0.3, 0.7), 3)
    assert button0.image == 'image'
    assert button0.words == 'words'
    assert button0.x1 == 0
    assert button0.x2 == 0.5
    assert button0.y1 == 0.3
    assert button0.y2 == 0.7
    assert button0.keytype == 3
    
def test_update():
    button0 = button.Button('image', 'words', (0, 0.5, 0.3, 0.7), 3)
    assert button0.update(0.25, 0.35) == 3
    assert button0.update(0.4, 0.6) == 3
    assert button0.update(0, 0.3) == 3
    assert button0.update(1, 1) == None
    assert button0.update(0.6, 0.3) == None
    assert button0.update(0.4, 0.2) == None
    
def test_get_drawing_info():
    button0 = button.Button('image', 'words', (0, 0.5, 0.3, 0.7), 3)
    print(button0.get_drawing_info())
    assert button0.get_drawing_info() == (('image', (0, 0.5, 0.3, 0.7)), 
                                        ('words', (0.01, 0.49, 0.31, 0.69)))