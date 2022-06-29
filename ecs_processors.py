import esper
import pygame
from ecs_components import RenderableComponent, PositionComponent


class RenderProcessor(esper.Processor):
    def __init__(self, window, clear_color=(255, 255, 255)):
        super().__init__()
        self.window = window
        self.clear_color = clear_color

    def process(self, *args, **kwargs):
        self.window.fill(self.clear_color)
        for ent, (rend, pos) in self.world.get_components(RenderableComponent, PositionComponent):
            self.window.blit(rend.image, (pos.x * 32, pos.y * 32))
        pygame.display.flip()


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
