class Settings():

    # Инициализируем настройки игры
    def __init__(self):
        # Параметры экрана
        self.screen_width = 850
        self.screen_height = 600
        # Цвет экрана
        self.bg_color = (0, 150, 250)
        # Настройка корабля
        self.ship_limit = 3
        # Параметры снарядов
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (111, 255, 111)
        self.bullets_allowed = 10
        # Настройка пришельцев
        self.fleet_drop_speed = 10

        # Ускорение игры
        self.speedup_scale = 1.1
        # Темп увеличения очков за пришельцев
        self.score_scale = 1.5

        # Определяем начальный уровень сложности
        self.difficult_level = 'medium'

        self.initialize_dynamic_settings()

    '''Инициализируем настройки, изменяющиеся в ходе игры'''
    def initialize_dynamic_settings(self):
        if self.difficult_level == 'easy':
            self.ship_limit = 5
            self.bullets_allowed = 15
            self.ship_speed = 1.0
            self.bullet_speed = 1.75
            self.alien_speed = 0.75
            self.alien_points = 10 # Подсчет очков
        elif self.difficult_level == 'medium':
            self.ship_limit = 3
            self.bullets_allowed = 10
            self.ship_speed = 1.5
            self.bullet_speed = 2.5
            self.alien_speed = 1.0
            self.alien_points = 20 # Подсчет очков
        elif self.difficult_level == 'difficult':
            self.ship_limit = 1
            self.bullets_allowed = 5
            self.ship_speed = 3.0
            self.bullet_speed = 5.0
            self.alien_speed = 1.8
            self.alien_points = 30 # Подсчет очков

        self.fleet_direction = 1  # Движение вправо


    '''Увеличиваем настройки скорости игры'''
    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale) # Увеличения очков за пришельцев
        # print(self.alien_points) # Проверяем увеличение очков за пришельцев(увеличивается со второго уровня)

    def set_difficulty(self, diff_setting):
        if diff_setting == 'easy':
            print('easy')
        elif diff_setting == 'medium':
            pass
        elif diff_setting == 'difficult':
            pass
