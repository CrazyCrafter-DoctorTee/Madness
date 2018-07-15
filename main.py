import gamemanager

if __name__ == '__main__':

    manager = gamemanager.GameManager()
    
    while manager.active:
        manager.next_frame()
    manager.close()
