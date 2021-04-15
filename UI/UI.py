import math
import random
import pygame
from Domain.Game import Game, Resources
from Domain.Shop import Shop
from UI.Sprites import Sprite
from Domain.Bullet import BulletSlow, BulletMedium, BulletFast
from Infrastructure.Color import COLOR
from UI.Screens.PauseScreen import PauseScreen
from UI.Screens.ShopScreen import ShopScreen

from UI.Screens.MainMenuScreen import MainMenuScreen
from Infrastructure.Vector import Vector

pygame.font.init()
font = pygame.font.SysFont(None, 20)
FPS = 30


def get_sprites_additional_vector(map_):
    return -1 * map_.ship.location + Vector(map_.w / 4, map_.h / 4)


def draw_text(text, color, surface, rect=None, x=None, y=None):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    if rect is not None:
        (x, y) = rect.center
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


def draw_button(center, width, height, surface,
                text):
    button = pygame.Rect(0, 0, width, height)
    button.center = center
    pygame.draw.rect(surface, COLOR.GREY, button)
    draw_text(text, COLOR.BLACK, surface,
              button)
    return button


class WinParams:
    def __init__(self, win, width, height):
        self.win = win
        self.width = width
        self.height = height


def _get_stat_str(game):
    d = game.ship.bullets_count
    health = game.ship.health
    coins_count = game.resources.coins_count
    return ''.join((f'HEALTH = {health}, ',
                    f'COINS : {coins_count}',
                    f'BulletFast:{d[BulletFast]}, ',
                    f'BulletMedium:{d[BulletMedium]} ,',
                    f'BulletSlow:{d[BulletSlow]} '))


class UI:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        info = pygame.display.Info()
        self.win_params = WinParams(
            # pygame.display.set_mode((0, 0)),
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN),
            info.current_w, info.current_h)
        pygame.display.set_caption("Asteroids")
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.drawing_circle = False
        self.stars = self.get_stars_location()
        self.resources = Resources()
        self.shop = Shop(self.resources)
        self.shop_screen = ShopScreen(self.win_params, self.shop, self)
        self.pause_scr = PauseScreen(self.win_params, self.shop_screen, self)
        self.start_scr = MainMenuScreen(self.win_params, self,
                                        self.run_game, self.shop_screen)

    def run_app(self):
        self.start_scr.show()

    def run_game(self):
        game = Game(self.win_params.width, self.win_params.height, self.shop)
        game.shop.reset_if_arsenal_is_empty()
        self.all_sprites = pygame.sprite.Group()
        self.add_starting_sprites(game.Map.map_objects)
        while game.running:
            game.Map.removing_objects.clear()
            game.Map.new_objects.clear()

            self.clock.tick(FPS)
            self.handle_keys_events(game)
            game.finish_if_required()
            game.handle_collisions()
            game.update()

            self.update_sprites_list(game.Map)
            self.draw(game)

        return game.get_results()

    def pause(self, game):
        self.pause_scr.show(game)

    def add_starting_sprites(self, map_objects):
        for map_obj in map_objects:
            self.all_sprites.add(Sprite.get_sprite(map_obj))

    def print_stat(self, game):
        stat = _get_stat_str(game)
        font_name = pygame.font.match_font('arial')
        font = pygame.font.Font(font_name, 20)
        text_surface = font.render(stat,
                                   True, COLOR.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (0, 0)
        self.win_params.win.blit(text_surface, text_rect)

    def get_stars_location(self):
        k = 3
        return [(random.randrange(-self.win_params.width * k,
                                  self.win_params.width * k),
                 random.randrange(-self.win_params.height * k,
                                  self.win_params.height * k))
                for i in range(1000)]

    def update_sprites_list(self, map_):
        removing_sprites = set(
            s for s in self.all_sprites if s.obj in map_.removing_objects)
        self.all_sprites.remove(removing_sprites)
        for obj in map_.new_objects:
            self.all_sprites.add(Sprite.get_sprite(obj))

    def draw_sight(self, game):
        length = 400
        scope_angle = game.ship.scope_angle
        if game.ship.scope_mode:
            dst = int(length * math.sin(scope_angle) + self.center[0]), \
                  int(-length * math.cos(scope_angle) + self.center[1])
            pygame.draw.aalines(self.win, COLOR.RED, True,
                                [self.center, dst])

    @property
    def center(self):
        return int(self.win_width / 2), int(self.win_height / 2)

    def draw_circle(self, game):
        circle_radius = 400
        rect = pygame.Rect(0, 0, circle_radius * 2,
                           circle_radius * 2)
        rect.center = self.center
        if self.drawing_circle:
            for vector_to_asteroid in game.get_vectors_to_asteroids():
                vector_to_asteroid.normalize(circle_radius)
                self.draw_segment_with_asteroid(vector_to_asteroid, rect)
            pygame.draw.circle(self.win, COLOR.BLUE, self.center,
                               circle_radius, 1)

    def draw_segment_with_asteroid(self, vector_to_asteroid, rect):
        angle = -math.atan2(vector_to_asteroid.y, vector_to_asteroid.x)
        start = angle - 0.1
        stop = angle + 0.1
        pygame.draw.arc(self.win, COLOR.BLUE, rect, start, stop, width=6)

    def draw(self, game):
        additional_vector = get_sprites_additional_vector(game.Map)
        self.win.fill(COLOR.BLACK)
        self.all_sprites.update(additional_vector)
        self.draw_stars(additional_vector)
        self.all_sprites.draw(self.win)
        self.print_stat(game)
        self.draw_circle(game)
        self.draw_sight(game)
        pygame.display.flip()

    def draw_stars(self, additional_vector):
        for star in self.stars:
            location = int(star[0] + additional_vector.x), int(
                star[1] + additional_vector.y)
            pygame.draw.circle(self.win, COLOR.WHITE, location, 1, 1)

    def handle_keys_events(self, game):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.ship.turn_left(1)
                if event.key == pygame.K_RIGHT:
                    game.ship.turn_right(1)
                if event.key == pygame.K_UP:
                    game.ship.speed_up(1)
                if event.key == pygame.K_DOWN:
                    game.ship.speed_down(1)
                if event.key == pygame.K_SPACE:
                    game.ship.shooting = 1
                if event.key == pygame.K_ESCAPE:
                    self.pause(game)
                if event.key == pygame.K_LSHIFT or \
                        event.key == pygame.K_RSHIFT:
                    game.ship.switch_scope_mode()
                if event.key == pygame.K_RCTRL or event.key == pygame.K_LCTRL:
                    self.drawing_circle = not self.drawing_circle
                change_bullet_type(game, event)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    game.ship.shooting = 0
                if event.key == pygame.K_LEFT:
                    game.ship.turn_left(0)
                if event.key == pygame.K_RIGHT:
                    game.ship.turn_right(0)
                if event.key == pygame.K_UP:
                    game.ship.speed_up(0)
                if event.key == pygame.K_DOWN:
                    game.ship.speed_down(0)

    @property
    def win(self):
        return self.win_params.win

    @property
    def win_width(self):
        return self.win_params.width

    @property
    def win_height(self):
        return self.win_params.height


def change_bullet_type(game, event):
    if event.key == pygame.K_1:
        game.ship.change_bullet_type(BulletFast)
    if event.key == pygame.K_2:
        game.ship.change_bullet_type(BulletMedium)
    if event.key == pygame.K_3:
        game.ship.change_bullet_type(BulletSlow)
