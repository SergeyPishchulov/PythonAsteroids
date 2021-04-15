import random

from Infrastructure.Vector import Vector


def get_bonuses(map_width, map_height, coins_count):
    coins = []
    for i in range(coins_count):
        r = 40
        w = 1.2 * map_width
        h = 1.2 * map_height
        location = Vector(random.randrange(int(-w), int(w)),
                          random.randrange(int(-h), int(h)))
        coins.append(Coin(location, random.randrange(1, 5) * 100))
    return coins


class Bonus:
    def __init__(self, location):
        self.location = location

    def take(self, ship):
        pass


class Coin(Bonus):
    def __init__(self, location, value):
        super().__init__(location)
        self.value = value
        self.radius = 15

    def take(self, resources):
        resources.coins_count += self.value
