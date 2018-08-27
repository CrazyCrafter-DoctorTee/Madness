# TODO: fix bug where the leftCorner becomes negative when maxDims are less than screenDims
class Camera(object):

    def __init__(self, screenDims, maxDims):
        self.screenDims = screenDims
        self.maxDims = maxDims

    def generate_offset(self, playerCords):
        playX, playY = playerCords
        if playX + self.screenDims[0]//2 > self.maxDims[0]:
            x = self.maxDims[0] - self.screenDims[0]
        else:
            x = max(0, playX-self.screenDims[0]//2)
        if playY + self.screenDims[1]//2 > self.maxDims[1]:
            y = self.maxDims[1] - self.screenDims[1]
        else:
            y = max(0, playY-self.screenDims[1]//2)
        self.topLeft = (x, y)

    def get_position_in_window(self, objectCords):
        objX, objY = objectCords
        return (objectCords[0] - self.topLeft[0], objectCords[1] - self.topLeft[1])
