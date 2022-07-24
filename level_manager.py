import consts
from entity import EntityBuilder

import tmx


class LevelManager:
    def __init__(self, game_state):
        self.game_state = game_state

    def create_entity_from_string(self, layer_string, image, x, y):
        entity = EntityBuilder(self.game_state.world)
        image = self.game_state.user_interface.icons_manager.get_image(image)
        if layer_string == 'LAYER_TURF':
            entity.make_turf(image, x, y)
        if layer_string == 'LAYER_OBJECT':
            entity.make_object(image, x, y)
        if layer_string == 'LAYER_MOB':
            entity.make_mob(image, x, y)

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
            layer_string = 'LAYER_TURF'
            for prop in layer.properties:
                if prop.name == 'Layer':
                    layer_string = prop.value

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

                self.create_entity_from_string(layer_string, (obj_type.get('image')).source, x, y)

    def save_map_data(self):
        pass

    def load_map_data(self):
        pass
