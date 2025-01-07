import pygame.font

'''Инициализируем атрибуты кнопки'''
class Button():
    def __init__(self, ai_game, msg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Базовый цвет и цвет выделения
        self.base_color = (0, 135, 0)
        self.highlighted_color = (0, 65,0)

        # Сохранение сообщения, чтобы мы могли вызвать _prep_msg(), когда цвет кнопки изменится
        self.msg = msg

        # Назначение размера и свойств кнопок
        self.width, self.height = 200, 50
        self.button_color = self.base_color
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48) # None - шрифт по умолчанию; 48 - размер текста

        # Построение объекта rect кнопки и выравнивание по левому краю экрана по заданной высоте
        self.rect = pygame.Rect(0, 50, self.width, self.height)
        self.rect.left = self.screen_rect.left

        # Сообщение кнопки создается только один раз
        self._prep_msg()

    '''Преобразует msg в прямоугольник и выравнивает текст по центру'''
    def _prep_msg(self):
        self.msg_image = self.font.render(self.msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    '''Если кнопка была перемещена, текст так же переносится'''
    def _update_msg_position(self):
        self.msg_image_rect.center = self.rect.center

    '''Установка цвета выделения для кнопки'''
    def set_highlighted_color(self):
        self.button_color = self.highlighted_color
        self._prep_msg()

    '''Установка базового цвета для кнопки'''
    def set_base_color(self):
        self.button_color = self.base_color
        self._prep_msg()

    '''Отображение пустой кнопки и вывод сообщения'''
    def draw_button(self):
        self.screen.fill(self.button_color, self.rect) # Отображение прямоугольника кнопки
        self.screen.blit(self.msg_image, self.msg_image_rect) # Вывод сообщения