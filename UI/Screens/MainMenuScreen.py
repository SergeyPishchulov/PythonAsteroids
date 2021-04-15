import pygame

from Infrastructure.Color import COLOR
from UI.Screens.GamePlayScreen import GamePlayScreen
from UI import UI
from UI.Screens.ShopScreen import ShopScreen


class MainMenuScreen:
    def __init__(self, win_params, ui, run_game, shop_scr):
        self.win_params = win_params
        self.ui = ui
        self.gameplay_scr = GamePlayScreen(run_game, win_params, ui)
        self.shop_scr = shop_scr

    def fill_menu(self):
        self.win_params.win.fill(COLOR.BLACK)
        UI.draw_text('Asteroids', COLOR.WHITE,
                     self.win_params.win, None, self.win_params.width / 2, 200)

        button_play = UI.draw_button((
            self.win_params.width / 2, -100 + self.win_params.height / 2), 200,
            50, self.win_params.win, 'PLAY')

        button_shop = UI.draw_button((
            self.win_params.width / 2, self.win_params.height / 2), 200,
            50, self.win_params.win, 'SHOP')

        button_quit = UI.draw_button((
            self.win_params.width / 2, 100 + self.win_params.height / 2), 200,
            50, self.win_params.win, 'QUIT')
        return button_play, button_shop, button_quit

    def show(self):
        click = False
        button_play, button_shop, button_quit = self.fill_menu()
        while 1:
            mx, my = pygame.mouse.get_pos()
            if button_play.collidepoint((mx, my)) and click:
                self.gameplay_scr.show()
                button_play, button_shop, button_quit = self.fill_menu()
            if button_shop.collidepoint((mx, my)) and click:
                self.shop_scr.show(False)
                button_play, button_shop, button_quit = self.fill_menu()
            if button_quit.collidepoint((mx, my)) and click:
                exit()
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            pygame.display.update()
            self.ui.clock.tick(UI.FPS)
