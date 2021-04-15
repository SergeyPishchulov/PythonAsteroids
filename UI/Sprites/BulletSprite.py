from Infrastructure.Color import COLOR
from UI.Sprites import BaseSprite, Sprite
from Domain.Bullet import BulletSlow, BulletMedium, BulletFast


class BulletBaseSprite(BaseSprite.BaseSprite):

    def __init__(self, bullet):
        super().__init__(bullet)
        self.image = Sprite.get_image(f'bullet{bullet.TYPE}.png')
        self.image.set_colorkey(COLOR.BLACK)
        self.rect = self.image.get_rect()

    def update(self, additional_vector):
        Sprite.update(self.obj, self.rect, additional_vector)


NUMBER_BY_TYPE = {BulletFast: 1,
                  BulletMedium: 2,
                  BulletSlow: 3}
