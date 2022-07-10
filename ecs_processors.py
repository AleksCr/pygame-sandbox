import time
import esper
import pygame
import consts
from ecs_components import Renderable, Position


class DelayedProcessor(esper.Processor):
    def __init__(self, process_delay=0):
        super().__init__()
        self.process_delay = process_delay
        self.next_call = 0

    def process(self, *args, **kwargs) -> bool:
        now = time.time()
        if now <= self.next_call:
            return False
        else:
            self.next_call = now + self.process_delay
            return True


class RenderProcessor(DelayedProcessor):
    def __init__(self, user_interface, clear_color=(255, 255, 255), process_delay=0):
        super().__init__(process_delay)
        self.user_interface = user_interface
        self.clear_color = clear_color

    def process(self, *args, **kwargs) -> None:
        if not super().process():
            return

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
