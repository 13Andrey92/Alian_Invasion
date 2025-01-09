from turtledemo.sorting_animate import disable_keys

import pygame.font
from pygame.examples.cursors import image
from pygame.sprite import Group

from ship import Ship

class Scoreboard():
    '''Инициализируем атрибуты подсчета очков'''
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        # Настройка шрифта для вывода счета
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_images()

    '''Отображение игровой информации'''
    def prep_images(self):
        # Подготовка исходного изображения
        self.prep_score()
        # Подготовка изображения рекордного счета
        self.prep_high_score()
        # Вывод текущего уровня
        self.prep_level()
        # Вывод оставшихся кораблей
        self.prep_ships()
        # Вывод подсказки по управлению игрой
        self.help_control()

    '''Создаем подсказку по управлению игрой'''
    def help_control(self):
        self.move_key()
        self.fire_key()
        self.pause_key()

    '''Клавиши движения'''
    def move_key(self):
        self.move_text_image = self.font.render('Движение: ',True,
                                     self.text_color, self.settings.bg_color)
        self.move_text_rect = self.move_text_image.get_rect()
        self.move_text_rect.left = self.screen_rect.left + 10
        self.move_text_rect.bottom = self.screen_rect.bottom - 160

        self.move_left_keys_image = pygame.image.load('images/back.png')
        self.move_left_keys_image = pygame.transform.scale(self.move_left_keys_image,
                                                           (50, 40))  # Устанавливаем размер картинки
        self.move_left_keys_rect = self.move_left_keys_image.get_rect()
        self.move_left_keys_rect.right = self.move_text_rect.right + 60
        self.move_left_keys_rect.bottom = self.screen_rect.bottom - 160

        self.move_right_keys_image = pygame.image.load('images/right.png')
        self.move_right_keys_image = pygame.transform.scale(self.move_right_keys_image,
                                                            (50, 40)) # Устанавливаем размер картинки
        self.move_right_keys_rect = self.move_right_keys_image.get_rect()
        self.move_right_keys_rect.right = self.move_left_keys_rect.right + 60
        self.move_right_keys_rect.bottom = self.screen_rect.bottom - 160

    '''Клавиша стрельбы'''
    def fire_key(self):
        self.fire_text_image = self.font.render('Стрельба: ', True,
                                                self.text_color, self.settings.bg_color)
        self.fire_text_rect = self.fire_text_image.get_rect()
        self.fire_text_rect.left = self.move_text_rect.left
        self.fire_text_rect.bottom = self.move_text_rect.bottom + 60

        self.fire_keys_image = pygame.image.load('images/space.png')
        self.fire_keys_image = pygame.transform.scale(self.fire_keys_image, (110, 40))
        self.fire_keys_rect = self.fire_keys_image.get_rect()
        self.fire_keys_rect.right = self.fire_text_rect.right + 120
        self.fire_keys_rect.bottom = self.move_text_rect.bottom + 60

    '''Клавиша паузы'''
    def pause_key(self):
        self.pause_text_image = self.font.render('Поставить/снять с паузы: ', True,
                                                self.text_color, self.settings.bg_color)
        self.pause_text_rect = self.pause_text_image.get_rect()
        self.pause_text_rect.left = self.fire_text_rect.left
        self.pause_text_rect.bottom = self.fire_text_rect.bottom + 60

        self.pause_keys_image = pygame.image.load('images/p.png')
        self.pause_keys_image = pygame.transform.scale(self.pause_keys_image, (50, 40))
        self.pause_keys_rect = self.pause_keys_image.get_rect()
        self.pause_keys_rect.right = self.pause_text_rect.right + 60
        self.pause_keys_rect.bottom = self.fire_keys_rect.bottom + 60

    '''Преобразуем уровень в графическое изображение'''
    def prep_level(self):
        level_str = str(self.stats.level)
        self.level_image = self.font.render('Уровень ' + level_str, True,
                                            self.text_color, self.settings.bg_color)

        # Уровень выводится под текущим счетом
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    '''Сообщает количество оставшихся кораблей'''
    def prep_ships(self):

        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            self.ship = pygame.image.load('images/alien.bmp')
            ship = Ship(self.ai_game) # Создаем группу для хранения экземпляров кораблей
            ship.rect.x = 10 + ship_number * (10 + ship.rect.width)
            ship.rect.y = 10

            self.ships.add(ship)

    '''Преобразуем рекордный счет в графическое изображение'''
    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = 'Рекорд {:,}'.format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # Выравнивание рекорда по центру верхней стороны
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    '''Преобразуем текущий счет в графическое изображение'''
    def prep_score(self):
        rounded_score = round(self.stats.score, -1) # Округляем значение счета до десятков
        score_str = 'Счет {:,}'.format(rounded_score) # Ставим запятую при преобразовании числового значения в строку
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Вывод счета в правой верхней части экрана
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    '''Обнавляем рекордный счет, если он побит'''
    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    '''Вывод текущего счета,рекорда и количество кораблей на экран'''
    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    '''Вывод подсказки по управлению на начальный экран'''
    def show_control(self):
        self.screen.blit(self.move_text_image, self.move_text_rect)
        self.screen.blit(self.move_left_keys_image, self.move_left_keys_rect)
        self.screen.blit(self.move_right_keys_image, self.move_right_keys_rect)
        self.screen.blit(self.fire_text_image, self.fire_text_rect)
        self.screen.blit(self.fire_keys_image, self.fire_keys_rect)
        self.screen.blit(self.pause_text_image, self.pause_text_rect)
        self.screen.blit(self.pause_keys_image, self.pause_keys_rect)