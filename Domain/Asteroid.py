import math
import random

from Infrastructure.Vector import Vector


def get_asteroids(map_w, map_h, count):
    types = [AsteroidStrong, AsteroidMediumStrong, AsteroidMediumWeak,
             AsteroidWeak]
    asteroids = []
    for i in range(count):
        r = 40
        w = 1.2 * map_w
        h = 1.2 * map_h
        location = Vector(random.randrange(int(-w), int(w)),
                          random.randrange(int(-h), int(h)))
        astr = random.choice(types)(location, r)
        asteroids.append(astr)
    return asteroids


class AsteroidBase:
    def __init__(self, location, radius):
        self.location = location
        self.starting_radius = self.radius = radius
        self.is_broken = False

    def catch_bullet(self, bullet_damage):
        if bullet_damage > self.STRENGTH:
            new_r = math.sqrt(
                self.radius * self.radius * self.STRENGTH / bullet_damage)
            self.radius = new_r
            if self.radius < self.starting_radius / 3:
                self.is_broken = True


class AsteroidStrongParams:
    STRENGTH = 400
    TYPE = 4


class AsteroidMediumStrongParams:
    STRENGTH = 300
    TYPE = 3


class AsteroidMediumWeakParams:
    STRENGTH = 150
    TYPE = 2


class AsteroidWeakParams:
    STRENGTH = 110
    TYPE = 1


class AsteroidStrong(AsteroidBase, AsteroidStrongParams):
    pass


class AsteroidWeak(AsteroidBase, AsteroidWeakParams):
    pass


class AsteroidMediumStrong(AsteroidBase, AsteroidMediumStrongParams):
    pass


class AsteroidMediumWeak(AsteroidBase, AsteroidMediumWeakParams):
    pass
