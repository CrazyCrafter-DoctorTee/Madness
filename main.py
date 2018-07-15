import gamemanager

if __name__ == '__main__':

    manager = gamemanager.GameManager()
    
    while manager.state is not None:
        manager.next_frame()
    manager.close()
