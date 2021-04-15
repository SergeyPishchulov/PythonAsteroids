import pygame


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, obj):
        self.obj = obj
        pygame.sprite.Sprite.__init__(self)
