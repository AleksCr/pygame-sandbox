import esper
import pygame
from ecs_components import RenderableComponent, PositionComponent


class RenderProcessor(esper.Processor):
    def __init__(self, user_interface, clear_color=(255, 255, 255)):
        super().__init__()
        self.user_interface = user_interface
        self.window = user_interface.screen
        self.screen_width = user_interface.screen_width
        self.screen_height = user_interface.screen_height
        self.cell_size = user_interface.cell_size
        self.clear_color = clear_color

    def process(self, *args, **kwargs):
        self.window.fill(self.clear_color)
        self.blit_next_layer(self.user_interface.current_camera, 0, 4)
        pygame.display.flip()

    def blit_next_layer(self, camera, layer, max_layer):
        screen_center_x = int(self.screen_width / self.cell_size / 2)
        screen_center_y = int(self.screen_height / self.cell_size / 2)

        for ent, (rend, pos) in self.world.get_components(RenderableComponent, PositionComponent):

            x = (pos.x - camera.get_x() + screen_center_x) * self.cell_size
            y = (pos.y - camera.get_y() + screen_center_y) * self.cell_size
            if rend.layer == layer:
                self.window.blit(rend.image, (x, y))
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
