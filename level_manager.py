import tmx


class LevelManager:
    def __init__(self, game_state):
        self.game_state = game_state

    def import_chunk_form_tmx(self):
        chunk_map = tmx.TileMap.load('testmap.tmx')
        height, width = chunk_map.height, chunk_map.width
        obj_types = {}
        tile_set = chunk_map.tilesets[0].tiles
        for tile in tile_set:
            gid = tile.id + 1
            obj_type_data = {
                'obj_type': None or tile.type,
                'image': None or tile.image
            }

            obj_types.update({gid: obj_type_data})

        layer_i = 0
        for layer in chunk_map.layers:
            x = 0
            y = 0
            for tile in layer.tiles:
                gid = tile.gid

                x += 1

                if x == width:
                    x = 0
                    y += 1

                if not gid:
                    continue

                obj_type = obj_types.get(gid)

                object_dict = {
                    'x': x,
                    'y': y,
                    'image': (obj_type.get('image')).source,
                    'layer': layer_i,
                    'is_controllable': False
                }

                self.game_state.create_new_object(object_dict)
            layer_i += 1

    def save_chunk_data(self):
        pass

    def load_chunk_data(self):
        pass
