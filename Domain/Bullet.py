import math

from Infrastructure.Vector import Vector


class BulletBase:
    SQUARED_FLIGHT_DISTANCE = 0
    radius = 6

    def __init__(self, location, angle):
        self.location = location
        self.angle = angle

    @property
    def should_finish_flight(self):
        return self.SQUARED_FLIGHT_DISTANCE > self.SQUARED_MAX_DISTANCE

    def update_location(self):
        prev_x = self.location.x
        prev_y = self.location.y
        self.location.x += int(self.velocity * math.sin(self.angle))
        self.location.y -= int(self.velocity * math.cos(self.angle))
        self.SQUARED_FLIGHT_DISTANCE += (self.location.x - prev_x) ** 2 + \
                                        (self.location.y - prev_y) ** 2

    def get_destination_after_move(self):
        return Vector(
            self.location.x + int(self.velocity * math.sin(self.angle)),
            self.location.y - int(self.velocity * math.cos(self.angle)))


class BulletFastParams:
    SQUARED_MAX_DISTANCE = 10000
    DAMAGE = 200
    VELOCITY = 20
    TYPE = 1
    RELOAD_TIME = 4


class BulletMediumParams:
    SQUARED_MAX_DISTANCE = 14400
    DAMAGE = 300
    VELOCITY = 15
    TYPE = 2
    RELOAD_TIME = 6


class BulletSlowParams:
    SQUARED_MAX_DISTANCE = 25600
    DAMAGE = 600
    VELOCITY = 10
    TYPE = 3
    RELOAD_TIME = 8


class BulletFast(BulletBase, BulletFastParams):
    name = 'Fast Bullet'

    def __init__(self, location, angle, start_velocity):
        super().__init__(location, angle)
        self.velocity = start_velocity + BulletFastParams.VELOCITY


class BulletMedium(BulletBase, BulletMediumParams):
    name = 'Medium Bullet'

    def __init__(self, location, angle, start_velocity):
        super().__init__(location, angle)
        self.velocity = start_velocity + BulletMediumParams.VELOCITY


class BulletSlow(BulletBase, BulletSlowParams):
    name = 'Slow Bullet'

    def __init__(self, location, angle, start_velocity):
        super().__init__(location, angle)
        self.velocity = start_velocity + BulletSlowParams.VELOCITY
