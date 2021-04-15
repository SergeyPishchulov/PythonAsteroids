from Domain import Map
from Domain.Bullet import BulletSlow, BulletMedium, BulletFast
from Infrastructure.Vector import Vector


class Resources:
    def __init__(self):
        self.coins_count = 10000
        self.bullets_count_by_type = {
            BulletFast: 50,
            BulletMedium: 50,
            BulletSlow: 50
        }

    def arsenal_is_empty(self):
        return all(map(lambda x: x == 0, self.bullets_count_by_type.values()))


class Game:
    @property
    def ship(self):
        return self.Map.ship

    @property
    def ufo(self):
        return self.Map.ufo

    def __init__(self, win_w, win_h, shop=None):
        self.running = True
        self.ticks = 0
        self.shop = shop
        self.result = None
        self.resources = shop.resources if shop else None
        self.Map = Map.Map(win_w * 2, win_h * 2,
                           self.resources.bullets_count_by_type
                           if self.resources else None,
                           asteroids_count=12)

    def handle_collisions(self):
        self.handle_ship_collisions()
        self.handle_bullet_collision()

    def handle_ship_collisions(self):
        ship_bow_destination = self.ship.get_bow_destination_after_move()
        for astr in self.Map.asteroids:
            collision = Map.are_intersected_with_obj(
                ship_bow_destination, astr)
            if collision:
                self.ship.velocity = -2
                self.ship.get_damage_by_asteroid(astr)

        for bonus in self.Map.bonuses:
            collision = Map.circles_are_intersected(self.ship.location, 30,
                                                    bonus.location,
                                                    bonus.radius)
            if collision:
                bonus.take(self.resources)
                self.Map.removing_objects.add(bonus)

    def handle_bullet_collision(self):
        for bullet in self.Map.bullets:
            for astr in self.Map.asteroids:
                bullet_destination = bullet.get_destination_after_move()
                if Map.bullet_is_intersected_with_asteroid(
                        bullet_destination, bullet.radius, astr):
                    astr.catch_bullet(bullet.DAMAGE)
                    self.Map.removing_objects.add(bullet)
                    break
        for bullet in self.Map.bullets.difference(self.Map.removing_objects):
            bullet_destination = bullet.get_destination_after_move()
            if Map.circles_are_intersected(self.ship.location, 10,
                                           bullet_destination, bullet.radius):
                self.ship.catch_bullet()
                self.Map.removing_objects.add(bullet)

    def finish_if_required(self):
        if not self.ship.is_alive or self.resources.arsenal_is_empty() and \
                self.Map.contains_asteroids():
            self.result = 'LOSE'
            self.running = False
        if self.ship.is_alive and not self.Map.contains_asteroids():
            self.result = 'WIN'
            self.running = False

    def get_vectors_to_asteroids(self):
        ship = self.ship
        for asteroid in self.Map.asteroids:
            yield Vector(asteroid.location.x - ship.location.x,
                         asteroid.location.y - ship.location.y)

    def update(self):
        self.shoot()
        self.Map.update_map_objects_location()
        self.ship.reload_bullet()
        self.ufo.reload_bullet()

    def shoot(self):
        if self.ship.shooting and self.ship.bullet_is_loaded:
            bullet = self.ship.shoot()
            self.Map.bullets.add(bullet)
            self.Map.new_objects.add(bullet)
        if self.ufo.bullet_count > 0 and self.ufo.bullet_is_loaded:
            bullet_u = self.ufo.shoot(self.ship.location)
            self.Map.bullets.add(bullet_u)
            self.Map.new_objects.add(bullet_u)

    def get_results(self):
        return {'res': self.result}  # можно еще возвращать статистику матча
