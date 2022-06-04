import pygame
from game_object import GameObject


class GameState:
    def __init__(self, user_interface):
        self.user_interface = user_interface
        self.commands = []
        self.game_objects = []
        self.world_size = [10, 10]
        self.player_mob = self.fast_test_owner()

    def create_new_object(self, **obj_kwargs):
        obj = GameObject(
            x=obj_kwargs.get('x'),
            y=obj_kwargs.get('y'),
            image=obj_kwargs.get('image'),
            layer=obj_kwargs.get('layer'),
            owner=obj_kwargs.get('owner')
        )
        self.game_objects.append(obj)

        self.user_interface.update_objects_rendering_queue()
        return obj

    def testing_scene_init(self) -> None:
        self.create_new_object(x=0, y=0, layer=2, image='test.png', owner='test')
        self.player_mob = self.fast_test_owner()
        self.user_interface.current_camera.set_owner(self.player_mob)

        for x in range(1, 10):
            for y in range(1, 10):
                self.create_new_object(x=x, y=y, layer=1, image='bf2.png')

    def fast_test_owner(self):
        for obj in self.game_objects:
            if obj.owner:
                return obj

    def update(self) -> None:
        for command in self.commands:
            if command == 'K_RIGHT':
                self.player_mob.x += 1
            if command == 'K_LEFT':
                self.player_mob.x -= 1
            if command == 'K_UP':
                self.player_mob.y -= 1
            if command == 'K_DOWN':
                self.player_mob.y += 1
            self.commands.remove(command)
