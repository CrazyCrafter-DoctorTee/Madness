#Helper
class Camera(object):
    def __init__(self, player, gameMap, screenDims, offset=(0,0)):
        self.player = player
        self.map = gameMap
        self.screenDims = screenDims
        self.offset = offset

    def find_offset(self):
        playX, playY = self.player.x, self.player.y
        if playX + self.screenDims[0]//2 > self.map.maxX:
            x = self.map.maxX - self.screenDims[0]
        else:
            x = max(0, playX-self.screenDims[0]//2)
        if playY + self.screenDims[1]//2 > self.map.maxY:
            y = self.map.maxY - self.screenDims[1]
        else:
            y = max(0, playY-self.screenDims[1]//2)
        self.offset = (x, y)
