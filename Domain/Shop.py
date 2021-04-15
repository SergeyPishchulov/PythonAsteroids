from Domain.Bullet import BulletFast, BulletMedium, BulletSlow

bullet_type_by_name = \
    {
        'Fast': BulletFast,
        'Medium': BulletMedium,
        'Slow': BulletSlow
    }


class Shop:
    discount = 0.2
    price_by_type = {
        BulletFast: 60,
        BulletMedium: 70,
        BulletSlow: 80
    }

    def __init__(self, resources):
        self.resources = resources

    def buy(self, bullet_type, with_discount):
        count = 10
        price = self.price_by_type[
                    bullet_type] * (1 - self.discount * int(with_discount))
        if self.resources.coins_count >= count * price:
            self.resources.bullets_count_by_type[bullet_type] += count
            self.resources.coins_count -= int(count * price)

    def get_price_by_type_name(self, type_name):
        return self.price_by_type[bullet_type_by_name[type_name]]

    def get_count_by_type_name(self, type_name):
        return self.resources.bullets_count_by_type[
            bullet_type_by_name[type_name]]

    def reset_if_arsenal_is_empty(self):
        if self.resources.bullets_count_by_type[BulletMedium] == 0:
            self.resources.bullets_count_by_type[BulletMedium] = 1
