import tmx

import consts


class LevelManager:
    def __init__(self, game_state):
        self.game_state = game_state

    @staticmethod
    def layer_string_to_int(layer) -> int:
        if layer == 'LAYER_TURF':
            layer = consts.LAYER_TURF
        if layer == 'LAYER_OBJECT':
            layer = consts.LAYER_OBJECT
        if layer == 'LAYER_MOB':
            layer = consts.LAYER_MOB
        if layer == 'LAYER_AREA':
            layer = consts.LAYER_AREA

        return layer

    def import_map_form_tmx(self, tmx_file) -> None:
        chunk_map = tmx.TileMap.load(tmx_file)
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

        for layer in chunk_map.layers:
            layer_l = 'LAYER_TURF'
            for prop in layer.properties:
                if prop.name == 'Layer':
                    layer_l = self.layer_string_to_int(prop.value)

            x = 0
            y = 0
            for tile in layer.tiles:
                gid = tile.gid

                if x == width:
                    x = 0
                    y += 1

                x += 1

                if not gid:
                    continue

                obj_type = obj_types.get(gid)

                object_dict = {
                    'x': x,
                    'y': y,
                    'image': (obj_type.get('image')).source,
                    'layer': layer_l,
                    'is_controllable': False
                }

                self.game_state.create_new_entity(object_dict)

    def save_map_data(self):
        pass

    def load_map_data(self):
        pass
