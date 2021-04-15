import unittest

from Domain.Bullet import BulletFast, BulletSlow, BulletMedium
from Domain.Map import Map
from Domain.Ship import Ship
from Infrastructure.Vector import Vector
from Domain.Game import Game


def get_map(ship_location):
    w, h = 80, 200
    map_ = Map(w, h)
    map_.ship = Ship(ship_location, {
        BulletFast: 50,
        BulletMedium: 50,
        BulletSlow: 50
    })
    game = Game(w, h)
    game.Map = map_  # ship делает шаг длины 2
    return map_


class TestShipMove(unittest.TestCase):

    def test_ship_moved_on_velocity_count_during_one_tick(self):
        map_ = get_map(Vector(40, 100))
        map_.ship.update_ship_location()
        self.assertEqual(100 - map_.ship.velocity, map_.ship.location.y)

    def test_ship_is_faster_on_delta_vel_after_speed_up(self):
        map_ = get_map(Vector(40, 100))
        map_.ship.speed_up(1)
        new_velocity = map_.ship.velocity + map_.ship.delta_vel
        map_.ship.update_ship_location()
        self.assertEqual(100 - new_velocity, map_.ship.location.y)

    def test_ship_can_not_move_faster_than_max_velocity(self):
        map_ = get_map(Vector(40, 100))
        map_.ship.speed_up(1)
        for i in range(20):
            map_.ship.update_ship_location()
            self.assertLessEqual(map_.ship.velocity, map_.ship.max_velocity)

    def test_ship_can_shoot_only_once_during_reload_time(self):
        map_ = get_map(ship_location=Vector(40, 100))
        game = Game(1, 1)
        game.Map = map_
        game.ship.shooting = True
        for i in range(game.ship.current_bullet_type.RELOAD_TIME + 1):
            game.shoot()
            game.ship.reload_bullet()
        self.assertEqual(1, len(map_.bullets))


if __name__ == '__main__':
    unittest.main()
