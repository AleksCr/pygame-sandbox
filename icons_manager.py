import pygame


class IconsManager:
    def __init__(self):
        self.icons_dict = {}

    def get_image(self, image) -> pygame.Surface:
        if not self.icons_dict.get(image):
            image_subdict = {image: pygame.image.load(image)}
            self.icons_dict.update(image_subdict)
        return self.icons_dict.get(image)

    # TODO: compile image for mob method
