import pygame

from Infrastructure.Color import COLOR
from UI import UI


class GamePlayScreen:
    def __init__(self, run_game, win_params, ui):
        self.run_game = run_game
        self.win_params = win_params
        self.ui = ui

    def show(self):
        game_results = self.run_game()
        self.show_results(game_results)

    def show_results(self, results):
        click = False
        self.win_params.win.fill(COLOR.BLACK)
        if results['res'] == 'WIN':
            label_str = 'YOU WON!!!'
        else:
            label_str = "YOU LOSE"
        UI.draw_text(label_str, COLOR.WHITE,
                     self.win_params.win, None, self.win_params.width / 2, 200)

        button_quit = UI.draw_button((
            self.win_params.width / 2, 100 + self.win_params.height / 2), 200,
            50, self.win_params.win, 'QUIT')

        while 1:
            mx, my = pygame.mouse.get_pos()
            if button_quit.collidepoint((mx, my)) and click:
                break
            click = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            pygame.display.update()
            self.ui.clock.tick(UI.FPS)
