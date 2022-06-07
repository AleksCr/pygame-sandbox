import tmx


class LevelManager:
    def __init__(self):
        pass

    def get_level_objects(self):
        map = tmx.TileMap.load('testmap.tmx')