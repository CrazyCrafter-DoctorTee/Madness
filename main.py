import gamemanager
import this

if __name__ == '__main__':

    manager = gamemanager.GameManager()
    
    try:
        while manager.state is not None:
            manager.next_frame()
    except Exception as e:
        manager.close()
        raise e
    manager.close()
