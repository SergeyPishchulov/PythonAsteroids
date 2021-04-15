from Domain.Bonus import Coin
from Domain.Ship import Ship
from Domain.UFO import UFO
from UI.Sprites.AsteroidSprite import AsteroidBaseSprite
from UI.Sprites.BulletSprite import BulletBaseSprite
from UI.Sprites.ShipSprite import ShipBaseSprite
from UI.Sprites.CoinSprite import CoinBaseSprite
import os
import pygame
from Domain.Asteroid import AsteroidBase
from Domain.Bullet import BulletBase
from UI.Sprites.UFOSprite import UFOSprite


def get_image(image_name):
    folder = os.path.dirname(__file__)
    img_folder = os.path.join(folder, 'img')
    return pygame.image.load(os.path.join(img_folder, image_name)).convert()


def get_sprite(map_obj):
    if isinstance(map_obj, Ship):
        return ShipBaseSprite(map_obj)
    elif isinstance(map_obj, AsteroidBase):
        return AsteroidBaseSprite(map_obj)
    elif isinstance(map_obj, BulletBase):
        return BulletBaseSprite(map_obj)
    elif isinstance(map_obj, Coin):
        return CoinBaseSprite(map_obj)
    elif isinstance(map_obj, UFO):
        return UFOSprite(map_obj)


def update(obj, rect, additional_vector):
    rect.x = obj.location.x - rect.width / 2 + additional_vector.x
    rect.y = obj.location.y - rect.height / 2 + additional_vector.y
