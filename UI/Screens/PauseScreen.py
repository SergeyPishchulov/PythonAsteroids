import pygame

from Infrastructure.Color import COLOR
from UI import UI


class PauseScreen:
    def __init__(self, win_params, shop_scr, ui):
        self.win_params = win_params
        self.shop_scr = shop_scr
        self.ui = ui
        self.game = None

    def fill_menu(self):
        self.win_params.win.fill(COLOR.BLACK)
        UI.draw_text('PAUSE', COLOR.WHITE,
                     self.win_params.win, None, self.win_params.width / 2, 200)
        button_continue = UI.draw_button((
            self.win_params.width / 2, -100 + self.win_params.height / 2), 200,
            50, self.win_params.win, 'Continue')
        button_shop = UI.draw_button((
            self.win_params.width / 2, self.win_params.height / 2), 200,
            50, self.win_params.win, 'Shop')
        button_finish = UI.draw_button((
            self.win_params.width / 2, 100 + self.win_params.height / 2), 200,
            50, self.win_params.win, 'Finish')
        return button_continue, button_finish, button_shop

    def show(self, game):
        click = False
        button_continue, button_finish, button_shop = self.fill_menu()
        while 1:
            mx, my = pygame.mouse.get_pos()
            if button_finish.collidepoint((mx, my)) and click:
                game.running = False
                break
            if button_shop.collidepoint((mx, my)) and click:
                self.shop_scr.show(True)
                button_continue, button_finish, button_shop = self.fill_menu()
            if button_continue.collidepoint((mx, my)) and click:
                break
            click = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            pygame.display.update()
            self.ui.clock.tick(UI.FPS)
