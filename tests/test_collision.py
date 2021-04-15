import unittest

from Domain.Asteroid import AsteroidMediumStrong
from Domain.Map import Map
from Domain.Ship import Ship
from Infrastructure.Vector import Vector
from Domain.Game import Game


class TestCollisionsWithAsteroids(unittest.TestCase):

    def test_col(self):
        w, h = 80, 200
        map_ = Map(w, h)
        map_.ship = Ship(Vector(40, 101), [0, 0, 0])
        map_.asteroids = [AsteroidMediumStrong(Vector(40, 40), radius=40)]
        game = Game(w, h)
        game.Map = map_  # ship делает шаг длины 2
        game.handle_collisions()
        map_.ship.update_ship_location()
        self.assertEqual(103, map_.ship.location.y)


if __name__ == '__main__':
    unittest.main()
