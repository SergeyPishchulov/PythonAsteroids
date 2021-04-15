import copy
import math
from Infrastructure.Vector import Vector
from Domain.Bullet import BulletMedium


class Ship:
    delta_vel = 1
    delta_angle = 0.10
    max_velocity = 15

    def __init__(self, location, bullets_count):
        self.location = location
        self.angle = 0
        self.scope_angle = 0
        self.min_velocity = self.velocity = 2
        self.length = 40
        self.health = 1000000000000000000000000000000000
        self.current_bullet_type = BulletMedium
        self.bullets_count = bullets_count  # <-dict
        self.loading_ticks = 0
        self.movement = Movement()
        self.scope_rotation = Rotation()
        self.shooting = 0
        self.scope_mode = False

    def switch_scope_mode(self):
        self.movement.right = 0
        self.movement.left = 0
        self.scope_mode = not self.scope_mode

    @property
    def bullet_is_loaded(self):
        return self.loading_ticks == self.current_bullet_type.RELOAD_TIME

    def change_bullet_type(self, new_type):
        self.current_bullet_type = new_type
        self.loading_ticks = 0

    def reload_bullet(self):
        if self.bullets_count[self.current_bullet_type] > 0 and \
                self.loading_ticks < self.current_bullet_type.RELOAD_TIME:
            self.loading_ticks += 1

    def shoot(self):
        self.loading_ticks = 0
        self.bullets_count[self.current_bullet_type] -= 1
        return self.current_bullet_type(copy.deepcopy(self.location),
                                        self.scope_angle,
                                        self.velocity)

    def turn_left(self, value):
        if self.scope_mode:
            self.scope_rotation.left = value
        else:
            self.movement.left = value

    def turn_right(self, value):
        if self.scope_mode:
            self.scope_rotation.right = value
        else:
            self.movement.right = value

    def speed_up(self, value):
        self.movement.speed_up = value

    def speed_down(self, value):
        self.movement.speed_down = value

    def get_damage_by_asteroid(self, astr):
        self.health -= 10

    def update_scope_rotation(self):
        if self.scope_mode:
            if self.scope_rotation.left:
                self.scope_angle -= self.delta_angle
            if self.scope_rotation.right:
                self.scope_angle += self.delta_angle
        else:
            self.scope_angle = self.angle

    def update_ship_location(self):
        self.update_scope_rotation()
        if self.movement.left:
            self.angle -= self.delta_angle
        if self.movement.right:
            self.angle += self.delta_angle
        if self.movement.speed_up:
            self.velocity = min(self.velocity + self.delta_vel,
                                self.max_velocity)
        if self.movement.speed_down:
            self.velocity = max(self.velocity - self.delta_vel,
                                self.min_velocity)
        self.location.x += int(self.velocity * math.sin(self.angle))
        self.location.y -= int(self.velocity * math.cos(self.angle))

    def get_move_destination(self):
        return (self.location.x + int(self.velocity * math.sin(self.angle)),
                self.location.y - int(self.velocity * math.cos(self.angle)))

    def get_bow_destination_after_move(self):
        return Vector(self.location.x + (self.velocity + 0.5 * self.length)
                      * math.sin(self.angle),
                      self.location.y - (self.velocity + 0.5 * self.length)
                      * math.cos(self.angle))

    def catch_bullet(self):
        self.health -= 5

    @property
    def is_alive(self):
        return self.health > 0


class Movement:
    def __init__(self):
        self.left = 0
        self.right = 0
        self.speed_up = 0
        self.speed_down = 0


class Rotation:
    def __init__(self):
        self.left = 0
        self.right = 0
