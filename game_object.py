class GameObject:
    def __init__(self, x=0, y=0, image=None, layer=1, is_controllable=False):
        self.x = x
        self.y = y
        self.x_bias = 0
        self.y_bias = 0
        self.image = image
        self.layer = layer
        self.is_controllable = is_controllable

    def set_image(self, image):
        self.image = image
