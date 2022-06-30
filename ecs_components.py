class RenderableComponent:
    def __init__(self, image, layer):
        self.image = image
        self.layer = layer


class ControlComponent:
    def __init__(self):
        self.control = True


class PositionComponent:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class InputComponent:
    def __init__(self):
        pass

