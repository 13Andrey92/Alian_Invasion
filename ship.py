import pygame
from pygame import sprite
from pygame.examples.cursors import image
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_game):
        # Инициализируем корабль и задаем начальную позицию
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Загружаем корабль и получаем прямоугольник
        self.image = pygame.image.load('images/cosmoship.bmp')
        self.image = pygame.transform.scale(self.image, (50, 50)) # Устанавливаем размер картинки
        self.rect = self.image.get_rect()

        # Каждый новый корабль появляется у нижнего края экрана
        self.rect.midbottom = self.screen_rect.midbottom

        # Сохранение координаты центра корабля
        self.x = float(self.rect.x)
        # Перемещение
        self.moving_right = False
        self.moving_left = False

        # Обновляем позицию корабля
    def update(self):
        # Обновляем х объекта ship, не rect. Данные берем из файла settings.py
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # Обновление атрибута rect на основании self.x
        self.rect.x = self.x

    # Рисуем корабль в текущей позиции
    def blitme(self):
        self.screen.blit(self.image, self.rect)

    '''Размещаем корабль в центре нижней части экрана'''
    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)