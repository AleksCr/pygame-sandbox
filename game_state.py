from entity import EntityBuilder
from level_manager import LevelManager
import esper
from ecs_components import Position


class GameState:
    def __init__(self, user_interface):
        self.user_interface = user_interface
        self.level_manager = LevelManager(self)
        self.commands = []
        self.game_objects = []

        self.world = esper.World()
        self.player_entity = None

        self.testing_scene_init()

    def testing_scene_init(self) -> None:
        player = EntityBuilder(self.world)
        player.make_mob(self.user_interface.icons_manager.get_image('resources/test.png'), 1, 1)
        player_cam = self.world.component_for_entity(player.get_id(), Position)
        self.user_interface.current_camera.set_owner(player_cam)
        self.player_entity = player.get_id()

        self.level_manager.import_map_form_tmx('testmap.tmx')

    def update(self) -> None:
        player_position_component = self.world.component_for_entity(self.player_entity, Position)
        for command in self.commands:
            if not self.player_entity:
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
