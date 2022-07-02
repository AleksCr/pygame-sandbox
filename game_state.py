from level_manager import LevelManager
import esper
from ecs_components import RenderableComponent, PositionComponent, ControlComponent


class GameState:
    def __init__(self, user_interface):
        self.user_interface = user_interface
        self.level_manager = LevelManager(self)
        self.commands = []
        self.game_objects = []

        self.world = esper.World()
        self.player_mob = None

        self.testing_scene_init()

    def create_new_entity(self, obj_kwargs) -> int:
        entity = self.world.create_entity()
        self.world.add_component(entity, RenderableComponent(
            image=self.user_interface.icons_manager.get_image(obj_kwargs.get('image')),
            layer=obj_kwargs.get('layer')
        ))
        self.world.add_component(entity, PositionComponent(obj_kwargs.get('x'), obj_kwargs.get('y')))

        return entity

    def testing_scene_init(self) -> None:
        player = self.create_new_entity({'x': 0, 'y': 0, 'layer': 2, 'image': 'resources/test.png'})
        player_cam = self.world.component_for_entity(player, PositionComponent)
        self.user_interface.current_camera.set_owner(player_cam)
        self.player_mob = player

        self.level_manager.import_map_form_tmx('testmap.tmx')

    def update(self) -> None:
        for command in self.commands:
            player_position_component = self.world.component_for_entity(self.player_mob, PositionComponent)
            if not self.player_mob:
                return
            if command == 'K_RIGHT':
                player_position_component.x += 1
            if command == 'K_LEFT':
                player_position_component.x -= 1
            if command == 'K_UP':
                player_position_component.y -= 1
            if command == 'K_DOWN':
                player_position_component.y += 1
            if command == 'MOUSEBUTTONUP':
                pass
            self.commands.remove(command)
