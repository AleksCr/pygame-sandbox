from dataclasses import dataclass as component
import pygame


@component
class Renderable:
    image: pygame.Surface
    layer: int


@component
class Collide:
    pass


@component
class Position:
    x: int
    y: int


class Input:
    def __init__(self):
        pass

