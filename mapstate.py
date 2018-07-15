import pygame

import gamestate
import camera
import player
import enemy
import gamemap


class MapState(gamestate.GameState):

    def __init__(self, ioManager, screen):
        self.ioManager = ioManager
        self.screen = screen
        self.screenDims = pygame.display.get_surface().get_size()
        self.images = self.create_images(self.ioManager.get_data('images'))
        maps = self.ioManager.get_data('maps')
        self.maps = {}
        for name, attribs in maps.items():
            self.maps[name] = gamemap.GameMap(attribs['filename'], attribs['tiledims'])
        self.currMap = self.maps[self.ioManager.get_data('game', 'map', 'startmap')]
        self.player = player.Player(self.currMap, self.ioManager.get_data('game', 'map', 'startdims'))
        self.enemy = enemy.Enemy(self.images['character']['enemy'], self.maps['start'], [320, 320])
        self.camera = camera.Camera(self.screenDims, self.maps['start'].maxDims)

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    return 'battle'
                self.player.key_down(event.key)
            if event.type == pygame.KEYUP:
                self.player.key_up(event.key)
        return 'map'

    def draw_map(self, tileList, startCords, tileSize):
        i, x = 0, startCords[0]
        while i < len(tileList):
            j, y = 0, startCords[1]
            while j < len(tileList[i]):
                tile = self.images['map'][tileList[i][j]]
                self.load_image(tile, (x, y))
                j, y = j+1, y+tileSize[1]
            i, x = i+1, x+tileSize[0]

    def make_actions(self):
        self.player.move()
        self.enemy.move()

    def draw(self):
        playerCords = self.player.position
        self.camera.generate_offset(playerCords)
        tiles, startCords, tileSize = self.currMap.get_drawing_info(self.screenDims, self.camera.topLeft)
        self.draw_map(tiles, startCords, tileSize)
        self.load_image(self.images['character']['enemy'], self.camera.get_position_in_window(self.enemy.cords))
        self.load_image(self.images['character']['player'], self.camera.get_position_in_window(self.player.position))
        pygame.display.flip()
