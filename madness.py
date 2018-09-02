import time 
# TODO: prevent switch when no switch-ins
# TODO: figure why battle sometimes infinately loops
# TODO: battle crashes with only one critter
# TODO: make sure the map that gets generated is valid
# TODO: make sure turns work when there is no critter in slot 0
# TODO: make game end when player loses

from gamemanager import gamemanager

if __name__ == '__main__':

    manager = gamemanager.GameManager()
    lasttime = 0
    sleepy = 0
    TARGETSLEEP = 1/24

    try:
        while manager.state is not None:
            lasttime = time.perf_counter()
            manager.next_frame()
            sleepy = TARGETSLEEP - time.perf_counter() + lasttime
            if sleepy < 0:
                sleepy = 0
            time.sleep(sleepy)

    except Exception as e:
        manager.close()
        raise e
    manager.close()