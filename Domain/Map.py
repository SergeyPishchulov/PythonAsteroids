from Domain import Bonus, Asteroid
from Domain.Ship import Ship
from Domain.UFO import UFO
from Infrastructure.Vector import Vector


def are_intersected_with_obj(point, obj):
    return (point - obj.location).length() <= obj.radius


def circles_are_intersected(center1, r1, center2, r2):
    return (center1 - center2).length() <= r1 + r2


def bullet_is_intersected_with_asteroid(bullet_location, bullet_radius, astr):
    length = (bullet_location - astr.location).length()
    sum_rad = bullet_radius + astr.radius
    return length <= sum_rad


class Map:
    def __init__(self, w, h, bullets_count_by_type=None, asteroids_count=10):
        self.w = w
        self.h = h
        self.asteroids = Asteroid.get_asteroids(w, h, asteroids_count)
        self.bonuses = Bonus.get_bonuses(w, h, coins_count=20) \
            if bullets_count_by_type else []

        self.ship = Ship(location=Vector(0, 0),
                         bullets_count=bullets_count_by_type)
        self.ufo = UFO(self)
        self.bullets = set()
        self.new_objects = set()
        self.removing_objects = set()

    def contains_asteroids(self):
        return len(self.asteroids) != 0

    @property
    def map_objects(self):
        yield self.ship
        yield self.ufo
        yield from self.asteroids
        yield from self.bonuses

    def update_map_objects_location(self):
        self.ship.update_ship_location()
        self.ufo.update_location(self)
        removing_bullets = set()
        for b in self.bullets:
            b.update_location()
            if b.should_finish_flight:
                removing_bullets.add(b)
        self.bullets = self.bullets.difference(removing_bullets)
        self.removing_objects.update(removing_bullets)
        alive, dead = get_alive_and_dead(self.asteroids)
        self.asteroids = alive
        self.removing_objects.update(dead)


def get_alive_and_dead(asteroids):
    alive = []
    dead = []
    for asteroid in asteroids:
        if asteroid.is_broken:
            dead.append(asteroid)
        else:
            alive.append(asteroid)
    return alive, dead
