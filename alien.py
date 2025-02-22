import pygame
from pygame.sprite import Sprite

class Alien(Sprite):

    # Задаем начальную позицию пришельца
    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load('images/alien.bmp')
        self.image = pygame.transform.scale(self.image, (50, 50)) # Устанавливаем размер картинки
        self.rect = self.image.get_rect()
    # Новый пришелец появляется в верхнем левом углу
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    '''Возвращает, True если пришелец находится у края экрана'''
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    '''Перемещение пришельцев'''
    def update(self):
        # Перемещение вправо
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x