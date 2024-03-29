from game_object import GameObject
from level_manager import LevelManager


class GameState:
    def __init__(self, user_interface):
        self.user_interface = user_interface
        self.level_manager = LevelManager(self)
        self.commands = []
        self.game_objects = []

        self.player_mob = None

    def create_new_object(self, obj_kwargs, chunk_key='Center'):
        obj = GameObject(
            x=obj_kwargs.get('x'),
            y=obj_kwargs.get('y'),
            image=obj_kwargs.get('image'),
            layer=obj_kwargs.get('layer'),
            is_controllable=obj_kwargs.get('is_controllable')
        )
        self.game_objects.append(obj)

        self.user_interface.update_objects_layers_rendering_queue()
        return obj

    def testing_scene_init(self) -> None:
        self.create_new_object({'x': 0, 'y': 0, 'layer': 2, 'image': 'resources/test.png', 'is_controllable': True})
        self.player_mob = self.testing_find_controllable_mob()  # TODO: EC for input
        self.user_interface.current_camera.set_owner(self.player_mob)

        self.level_manager.import_map_form_tmx('testmap.tmx')

    def testing_find_controllable_mob(self):
        # TODO: refactor it in accordance with upcoming level load system
        for obj in self.game_objects:
            if obj.is_controllable:
                return obj

    def update(self) -> None:
        for command in self.commands:
            if not self.player_mob:
                return
            if command == 'K_RIGHT':
                self.player_mob.x += 1
            if command == 'K_LEFT':
                self.player_mob.x -= 1
            if command == 'K_UP':
                self.player_mob.y -= 1
            if command == 'K_DOWN':
                self.player_mob.y += 1
            self.commands.remove(command)
