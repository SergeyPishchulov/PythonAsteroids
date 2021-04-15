from Infrastructure.Color import COLOR
from UI.Sprites import BaseSprite, Sprite
from Domain.Bullet import BulletSlow, BulletMedium, BulletFast


class UFOSprite(BaseSprite.BaseSprite):

    def __init__(self, ufo):
        super().__init__(ufo)
        self.image = Sprite.get_image(f'UFO40.png')
        self.image.set_colorkey(COLOR.BLACK)
        self.rect = self.image.get_rect()

    def update(self, additional_vector):
        Sprite.update(self.obj, self.rect, additional_vector)
