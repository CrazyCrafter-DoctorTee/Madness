class Camera(object):
    
    def __init__(self, screenDims, maxDims):
        self.screenDims = screenDims
        self.maxDims = maxDims

    def find_offset(self, playerCords):
        print(self.screenDims)
        preCords = self.screenDims
        playX, playY = playerCords
        if playX + self.screenDims[0]//2 > self.maxDims[0]:
            x = self.maxDims[0] - self.screenDims[0]
        else:
            x = max(0, playX-self.screenDims[0]//2)
        if playY + self.screenDims[1]//2 > self.maxDims[1]:
            y = self.maxDims[1] - self.screenDims[1]
        else:
            y = max(0, playY-self.screenDims[1]//2)
        assert preCords == self.screenDims
        return (x, y)
