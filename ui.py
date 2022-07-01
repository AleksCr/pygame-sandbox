import pygame
from game_state import GameState
from icons_manager import IconsManager
from ecs_processors import RenderProcessor


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
        self.icons_manager = IconsManager()
        self.current_camera = Camera(5, 3)
        self.game_state = GameState(self)

        pygame.init()

        self.cell_size = 32
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.commands_queue = []

        self.objects_rendering_queue = {}

        render_processor = RenderProcessor(self)
        self.game_state.world.add_processor(render_processor)

    def run_game_loop(self) -> None:
        fps = pygame.time.Clock()
        while self.running:
            fps.tick(60)
            self.process_input()
            self.update()
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
        self.game_state.world.process()
        self.game_state.update()
