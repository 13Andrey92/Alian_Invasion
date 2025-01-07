import pygame.font

class Scoreboard():
    '''Инициализируем атрибуты подсчета очков'''
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Настройка шрифта для вывода счета
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # Подготовка исходного изображения
        self.prep_score()

    '''Преобразуем текущий счет в графическое изображение'''
    def prep_score(self):
        rounded_score = round(self.stats.score, -1) # Округляем значение счета до десятков
        score_str = '{:,}'.format(rounded_score) # Ставим запятую при преобразовании числового значения в строку
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Вывод счета в правой верхней части экрана
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    '''Вывод счета на экран'''
    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)