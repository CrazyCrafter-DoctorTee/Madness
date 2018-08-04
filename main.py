import gamemanager
import time
#dank memes
#import this

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
