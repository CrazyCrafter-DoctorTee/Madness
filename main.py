import this
import gamemanager

if __name__ == '__main__':

    try:
        manager = gamemanager.GameManager()

        while manager.state is not None:
            manager.next_frame()
    except Exception as e:
        manager.close()
        raise e
    manager.close()
