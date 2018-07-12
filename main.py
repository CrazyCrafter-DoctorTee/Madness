import gamemanager

if __name__ == '__main__':

    manager = gamemanager.GameManager()

    while 'gary': ## TODO: fix this so that next frame returns in a way to allow graceful closing
        manager.next_frame()
