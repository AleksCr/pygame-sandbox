import pygame


class IconsManager:
    def __init__(self):
        self.icons_dict = {}

    def get_image(self, image):
        if not self.icons_dict.get(image):
            image_subdict = {image: pygame.image.load(image)}
            self.icons_dict.update(image_subdict)
        return pygame.image.load(image)
