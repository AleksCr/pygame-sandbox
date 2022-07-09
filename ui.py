import consts
import pygame
from game_state import GameState
from icons_manager import IconsManager
from ecs_processors import RenderProcessor
from ecs_components import Renderable, Position


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
            if event.type == pygame.MOUSEBUTTONUP:
                self.game_state.commands.append('MOUSEBUTTONUP')
                print(self.find_clicked_entity(event.pos))
            if event.type == pygame.QUIT:
                self.running = False

    def update(self) -> None:
        self.game_state.world.process()
        self.game_state.update()

    def find_clicked_entity(self, pos) -> None or int:
        x, y = self.get_click_absolute_coordinates(pos)

        clicked_entity = None
        max_layer = 0
        x_bias, y_bias = self.get_click_tile_pixels(pos)

        for entity, (rend, position) in self.game_state.world.get_components(Renderable, Position):
            if position.x == x and position.y == y:
                surface = rend.image
                mask = pygame.mask.from_surface(surface)
                mask_pos = (x_bias, y_bias)

                if mask.get_at(mask_pos) and rend.layer >= max_layer:
                    max_layer = rend.layer
                    clicked_entity = entity  # last element is overlap each other becasue Renderable sorts same order as blit order
        return clicked_entity

    def get_click_tile_pixels(self, pos) -> tuple:
        x, y = self.get_click_relative_coordinates(pos)
        x_tile = abs(32 * x - pos[0])
        y_tile = abs(32 * y - pos[1])
        return x_tile, y_tile

    def get_screen_center_coordinates(self) -> tuple:
        screen_center_x = int(self.screen_width / self.cell_size / 2)
        screen_center_y = int(self.screen_height / self.cell_size / 2)
        return screen_center_x, screen_center_y

    def get_click_relative_coordinates(self, pos) -> tuple:
        x = pos[0] // self.cell_size
        y = pos[1] // self.cell_size
        return x, y

    def get_click_absolute_coordinates(self, pos) -> tuple:
        x, y = self.get_click_relative_coordinates(pos)

        screen_center_x, screen_center_y = self.get_screen_center_coordinates()

        x = x + self.current_camera.get_x() - screen_center_x
        y = y + self.current_camera.get_y() - screen_center_y
        return x, y

