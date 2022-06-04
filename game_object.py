import pygame


class GameObject:
    def __init__(self, x=0, y=0, image=None, layer=1, owner=None):
        self.x = x
        self.y = y
        self.x_bias = 0
        self.y_bias = 0
        self.image = pygame.image.load(image)
        self.layer = layer
        self.owner = owner
