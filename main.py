import pygame


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


class Camera:
    def __init__(self, x=0, y=0, owner_obj=None):
        self.__world_x_bias = x
        self.__world_y_bias = y
        self.__owner_obj = owner_obj

    def get_x(self) -> int:
        return self.__owner_obj.x if self.__owner_obj else self.__world_x_bias

    def get_y(self) -> int:
        return self.__owner_obj.y if self.__owner_obj else self.__world_y_bias

    def set_x(self, x) -> None:
        self.__world_x_bias = x

    def set_y(self, y) -> None:
        self.__world_x_bias = y

    def set_owner(self, owner_obj) -> None:
        self.__owner_obj = owner_obj


class UserInterface:
    def __init__(self):
        self.running = True
        self.game_state = GameState(self)
        self.current_camera = Camera(10, 3)

        pygame.init()

        self.cell_size = 32
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.commands_queue = []

        self.objects_rendering_queue = {}

        self.game_state.testing_scene_init()

    def update_objects_rendering_queue(self) -> None:
        self.objects_rendering_queue = {}
        for obj in self.game_state.game_objects:
            l = self.objects_rendering_queue.get(obj.layer) or []
            l.append(obj)
            d = {obj.layer: l}
            self.objects_rendering_queue.update(d)
        self.objects_rendering_queue = dict(sorted(self.objects_rendering_queue.items()))

    def run_game_loop(self) -> None:
        fps = pygame.time.Clock()
        while self.running:
            fps.tick(60)
            self.process_input()
            self.update()
            self.render()

    def process_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.game_state.commands.append('K_RIGHT')
                if event.key == pygame.K_LEFT:
                    self.game_state.commands.append('K_LEFT')
                if event.key == pygame.K_UP:
                    self.game_state.commands.append('K_UP')
                if event.key == pygame.K_DOWN:
                    self.game_state.commands.append('K_DOWN')
            if event.type == pygame.QUIT:
                self.running = False

    def update(self) -> None:
        self.game_state.update()

    def render(self) -> None:
        self.screen.fill((255, 255, 255))
        # TODO: layers render need a better approach
        for layer in self.objects_rendering_queue:
            for obj in self.objects_rendering_queue.get(layer):
                magic_number_x = int(self.screen_width / self.cell_size / 2)
                magic_number_y = int(self.screen_height / self.cell_size / 2)

                x = (obj.x - self.current_camera.get_x() + magic_number_x) * self.cell_size
                y = (obj.y - self.current_camera.get_y() + magic_number_y) * self.cell_size
                self.screen.blit(obj.image, (x, y))
        pygame.display.flip()


class GameObject:
    def __init__(self, x=0, y=0, image=None, layer=1, owner=None):
        self.x = x
        self.y = y
        self.x_bias = 0
        self.y_bias = 0
        self.image = pygame.image.load(image)
        self.layer = layer
        self.owner = owner


def main() -> None:
    ui = UserInterface()
    ui.run_game_loop()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
