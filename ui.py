import pygame
from game_state import GameState
from icons_manager import IconsManager


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
        self.icons_manager = IconsManager()
        self.current_camera = Camera(10, 3)

        pygame.init()

        self.cell_size = 32
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.commands_queue = []

        self.objects_rendering_queue = {}

        self.game_state.testing_scene_init()

    def update_objects_layers_rendering_queue(self) -> None:
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
            pygame.display.set_caption(f'FPS: {fps.get_fps()}')

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
                self.screen.blit(self.icons_manager.get_image(obj.image), (x, y))
        pygame.display.flip()
