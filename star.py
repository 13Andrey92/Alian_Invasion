import pygame

from pygame.sprite import Sprite

class Star(Sprite):
    def __init__(self, sky):
        super().__init__()
        self.screen = sky.screen

        self.image = pygame.image.load('images/zvezda 20x20.bmp')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)