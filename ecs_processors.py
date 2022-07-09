import esper
import pygame
import consts
from ecs_components import Renderable, Position


class RenderProcessor(esper.Processor):
    def __init__(self, user_interface, clear_color=(255, 255, 255)):
        super().__init__()
        self.user_interface = user_interface
        self.clear_color = clear_color

    def process(self, *args, **kwargs) -> None:
        self.user_interface.screen.fill(self.clear_color)
        self.blit_next_layer(self.user_interface.current_camera, consts.LAYER_TURF, consts.LAYER_AREA)
        pygame.display.flip()

    def blit_next_layer(self, camera, layer, max_layer) -> None:
        screen_center_x, screen_center_y = self.user_interface.get_screen_center_coordinates()

        for ent, (rend, pos) in self.world.get_components(Renderable, Position):

            x = (pos.x - camera.get_x() + screen_center_x) * self.user_interface.cell_size
            y = (pos.y - camera.get_y() + screen_center_y) * self.user_interface.cell_size
            if rend.layer == layer:
                self.user_interface.screen.blit(rend.image, (x, y))
        if layer > max_layer:
            return
        next_layer = layer + 1
        self.blit_next_layer(camera, next_layer, max_layer)


class PositionProcessor(esper.Processor):
    def __init__(self):
        pass

    def process(self, *args, **kwargs):
        pass


class ControlProcessor(esper.Processor):
    def __init__(self):
        pass

    def process(self, *args, **kwargs):
        pass
