import ecs_components
import consts


class EntityBuilder:
    def __init__(self, world, ent_id=None):
        self.world = world
        self.ent_id = None
        if not ent_id:
            self.ent_id = self.world.create_entity()
        else:
            self.ent_id = ent_id

    def get_entity_by_id(self, ent_id):
        self.ent_id = ent_id

    def finalize_build(self, attrs):
        for attr in attrs:
            self.world.add_component(self.ent_id, attr)

    def get_id(self):
        return self.ent_id

    def make_turf(self, image, x, y):
        attrs = self.img_and_pos(image, consts.LAYER_TURF, x, y)
        self.finalize_build(attrs)

    def make_object(self, image, x, y):
        attrs = self.img_and_pos(image, consts.LAYER_OBJECT, x, y)
        self.finalize_build(attrs)

    def make_mob(self, image, x, y):
        attrs = self.img_and_pos(image, consts.LAYER_MOB, x, y)
        self.finalize_build(attrs)

    @classmethod
    def make_area(cls):
        pass

    @classmethod
    def img_and_pos(cls, image, layer, x, y) -> tuple:
        return (
            ecs_components.Renderable(image=image, layer=layer),
            ecs_components.Position(x, y)
        )

