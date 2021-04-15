import pygame
from Infrastructure.Color import COLOR
from UI.Sprites import BaseSprite, Sprite


class CoinBaseSprite(BaseSprite.BaseSprite):

    def __init__(self, coin):
        super().__init__(coin)
        self.image = Sprite.get_image('coin.png')
        self.image.set_colorkey(COLOR.BLACK)
        self.rect = self.image.get_rect()

    def update(self, additional_vector):
        center_coordinates = self.rect.center
        self.image = pygame.transform.scale(self.image,
                                            (2 * int(self.obj.radius),
                                             2 * int(self.obj.radius)))
        self.rect = self.image.get_rect()
        self.rect.move_ip(center_coordinates)
        Sprite.update(self.obj, self.rect, additional_vector)
