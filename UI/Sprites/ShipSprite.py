import pygame

from Infrastructure.Color import COLOR
from UI.Sprites import BaseSprite, Sprite


class ShipBaseSprite(BaseSprite.BaseSprite):

    def __init__(self, ship):
        super().__init__(ship)
        self.orig_image = self.image = Sprite.get_image('ship40.png')
        self.image.set_colorkey(COLOR.WHITE)
        self.rect = self.image.get_rect()

    def update(self, additional_vector):
        self.rotate()
        Sprite.update(self.obj, self.rect, additional_vector)

    def rotate(self):
        rotated_image = pygame.transform.rotate(self.orig_image,
                                                self.obj.angle * (-57.325))
        new_rect = rotated_image.get_rect(
            center=self.image.get_rect(topleft=self.rect.topleft).center)
        self.rect = new_rect
        self.image = rotated_image
