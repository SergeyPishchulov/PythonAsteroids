import pygame

from Domain.Bullet import BulletFast
from Infrastructure.Color import COLOR
from UI import UI


class ShopScreen:
    def __init__(self, win_params, shop, ui):
        self.win_params = win_params
        self.shop = shop
        self.bullet_type_name = 'Fast'
        self.bullet_types = list(shop.price_by_type.keys())
        self.pointer = 0
        self.during_the_game = None
        self.ui = ui

    @property
    def current_type(self):
        return self.bullet_types[self.pointer]

    def fill_menu(self):
        self.win_params.win.fill(COLOR.BLACK)
        UI.draw_text(f'Coins: {self.shop.resources.coins_count}', COLOR.WHITE,
                     self.win_params.win, None, self.win_params.width / 2, 100)
        UI.draw_text(self.current_type.name, COLOR.WHITE,
                     self.win_params.win, None, self.win_params.width / 2, 200)
        UI.draw_text(f'Price: {self.shop.price_by_type[self.current_type]}',
                     COLOR.WHITE,
                     self.win_params.win, None, self.win_params.width / 2, 240)
        button_buy = UI.draw_button((
            self.win_params.width / 2, 400), 200,
            50, self.win_params.win, 'BUY')
        button_quit = UI.draw_button((
            self.win_params.width / 2, 500), 200,
            50, self.win_params.win, 'QUIT')
        button_right = UI.draw_button((
            100 + self.win_params.width / 2, 200), 50,
            50, self.win_params.win, '>')
        button_left = UI.draw_button((
            -100 + self.win_params.width / 2, 200), 50,
            50, self.win_params.win, '<')
        return button_buy, button_quit, button_left, button_right

    def swipe_left(self):
        count = len(self.bullet_types)
        self.pointer = (self.pointer - 1 + count) % count
        return self.fill_menu()

    def swipe_right(self):
        count = len(self.bullet_types)
        self.pointer = (self.pointer + 1) % count
        return self.fill_menu()

    def show(self, during_the_game):
        click = False
        button_buy, button_quit, button_left, button_right = self.fill_menu()
        while 1:
            mx, my = pygame.mouse.get_pos()
            if button_buy.collidepoint((mx, my)) and click:
                self.shop.buy(self.current_type,
                              with_discount=not during_the_game)
                button_buy, button_quit, button_left, button_right = \
                    self.fill_menu()
            if button_left.collidepoint((mx, my)) and click:
                button_buy, button_quit, button_left, button_right = \
                    self.swipe_left()
            if button_right.collidepoint((mx, my)) and click:
                button_buy, button_quit, button_left, button_right = \
                    self.swipe_right()
            if button_quit.collidepoint((mx, my)) and click:
                break

            click = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            pygame.display.update()
            self.ui.clock.tick(UI.FPS)
