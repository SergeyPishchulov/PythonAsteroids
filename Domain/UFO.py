import copy
import math
import random
from Domain import Map
from Domain.Bullet import BulletMedium
from Infrastructure.Vector import Vector

k = 10


class UFO:
    velocity = 10
    reload_time = 12

    def __init__(self, map_):
        r = map_.h
        self.location = Vector(100, 100)
        self.loading_ticks = 0
        self.bullet_count = 100

    @property
    def bullet_is_loaded(self):
        return self.loading_ticks == self.reload_time

    def reload_bullet(self):
        if self.loading_ticks < self.reload_time:
            self.loading_ticks += 1

    def shoot(self, target_location):
        v = target_location - self.location
        self.loading_ticks = 0
        angle = math.atan2(v.x, -v.y)
        self.bullet_count -= 1
        return BulletMedium(copy.deepcopy(self.location), angle, self.velocity)

    def update_location(self, map_):
        move = map_.ship.location - self.location
        self.velocity = move.length() / 30
        move.normalize(self.velocity)
        destination = self.location + move
        if is_correct_move(map_, destination):
            self.location = destination
            return
        while 1:
            move += Vector(random.randrange(int(-k), int(k)),
                           random.randrange(int(-k), int(k)))
            move.normalize(self.velocity)
            destination = self.location + move
            if is_correct_move(map_, destination):
                self.location = destination
                return


def is_correct_move(map_, destination):
    for astr in map_.asteroids:
        if Map.are_intersected_with_obj(destination, astr):
            return False
    return True
