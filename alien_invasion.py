import sys, pygame
from time import sleep
from random import randint

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import  Button
from star import Star
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion():
    '''Инициализирует игру и создает игровые ресурсы'''
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock() # Делаем плавное и равномерное движение пришельцев
        self.settings = Settings()# Применяем настройки из модуля settings

        # Полноэкранный режим
        self.screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        # Оконный режим
        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')

        self.stats = GameStats(self) # Создаем экземпляр для хранения статистики
        self.sb = Scoreboard(self) # Создаем экземпляр для хранения панели результатов

        self.ship = Ship(self) # Создаем экземпляр класса Ship
        self.bullets = pygame.sprite.Group() # Создаем группу для хранения всех летящих снарядов
        # Создаем группу для хранения всех пришельцев
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        # Создаем группу для хранения звезд
        self.stars = pygame.sprite.Group()
        self._create_stars()

        # Создание кнопки Play
        self.play_button = Button(self, 'Play')

        # Создание кнопки уровня сложности
        self._make_difficulty_buttons()

        self.game_active = False #???

    '''Создание кнопки для выбора уровня сложности'''
    def _make_difficulty_buttons(self):
        self.easy_button = Button(self, 'Easy')
        self.medium_button = Button(self, 'Medium')
        self.difficult_button = Button(self, 'Difficult')
        # Размещаем кнопки, чтобы они не перекрывали друг друга
        self.easy_button.rect.top = (self.play_button.rect.top + 1.5*self.play_button.rect.height)
        self.easy_button._update_msg_position()

        self.medium_button.rect.top = (self.easy_button.rect.top + 1.5*self.easy_button.rect.height)
        self.medium_button._update_msg_position()

        self.difficult_button.rect.top = (self.medium_button.rect.top + 1.5*self.medium_button.rect.height)
        self.difficult_button._update_msg_position()
        # Инициализируем среднюю кнопку выделенным цветом
        self.medium_button.set_highlighted_color()

    '''Запуск основного цикла'''
    def run_game(self):

        while True:
            # Методы, начинающиеся с "_" - вспомогательные методы
            self._check_events() # События клавиатуры и мыши
            if self.stats.game_active:
                self.ship.update() # Экземпляр класса Ship
                self._update_bullets() # Обновление позиций снарядов и уничтожение старых снарядов
                self._update_alience() # Обновление позиции каждого пришельца
            self._update_screen() # Обновление экрана при каждом проходе цикла
            self.clock.tick(300) # В настройках проверить скорость движения пришельцев!!!

    '''Отслеживание событий клавиатуры и мыши'''
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN: # Обнаруживаем события мышки при нажатии на кнопку
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_difficulty_buttons(mouse_pos)

    '''Запускаем игру при нажатии на Play'''
    def _check_play_button(self,mouse_pos):
        # Запускаем игру при нажатии кнопки Play
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

    '''Выбираем подходящий уровень сложности'''
    def _check_difficulty_buttons(self, mouse_pos):
        easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        medium_button_clicked = self.medium_button.rect.collidepoint(mouse_pos)
        diff_button_clicked = self.difficult_button.rect.collidepoint(mouse_pos)

        if easy_button_clicked:
            self.settings.difficult_level = 'easy'
            self.easy_button.set_highlighted_color()
            self.medium_button.set_base_color()
            self.difficult_button.set_base_color()
        elif medium_button_clicked:
            self.settings.difficult_level = 'medium'
            self.easy_button.set_base_color()
            self.medium_button.set_highlighted_color()
            self.difficult_button.set_base_color()
        elif diff_button_clicked:
            self.settings.difficult_level = 'difficult'
            self.easy_button.set_base_color()
            self.medium_button.set_base_color()
            self.difficult_button.set_highlighted_color()

    '''Запускаем новую игру'''
    def _start_game(self):
        # Сброс игровых настроек
        self.settings.initialize_dynamic_settings()
        # Сброс игровой статистики
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score() # Обнуляем количество очков

        # Очистка списков пришельцев и снарядов
        self.aliens.empty()
        self.bullets.empty()

        # Создание нового флота и размещение корабля в центре
        self._create_fleet()
        self.ship.center_ship()

        # Скрываем указатель мыши
        pygame.mouse.set_visible(False)

    # Нажатие клавиши
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        # Клавиша выхода
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        # Клавиша стрельбы
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        # Запуск игры клавишей P
        elif (event.key == pygame.K_p) and (not self.game_active):
            self._start_game()


    # Отпускание клавиши
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False

    ''' Создание нового снаряда и включение его в группу bullets'''
    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    # Обновление позиций снарядов и уничтожение старых снарядов
    def _update_bullets(self):
        # Обновление позиции снарядов
        self.bullets.update()
        # Удаление снарядов, вышедших за верхний край экрана
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # Удаление снарядов, вышедших за правый край экрана
        # for bullet in self.bullets.copy():
        #     if bullet.rect.left >= self.screen.get_rect().right:
        #         self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

        '''Проверка попадания в пришельца'''
    def _check_bullet_alien_collisions(self):
        # При попадании удаляется снаряд и пришелец
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()

        if not self.aliens:
            # Уничтожение существующих снарядов
            self.bullets.empty()
            # Создание нового флота
            self._create_fleet()
            # Повышение скорости игры
            self.settings.increase_speed()


    '''Проверяет, достиг ли флот края экрана, с последующим изменением позиций всех пришельцев во флоте'''
    def _update_alience(self):
        self._check_fleet_edges()
        self.aliens.update()
        # Проверка коллизии "пришелец - корабль
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Проверяем, добрались ли пришельцы до нижнего края экрана
        self._check_aliens_bottom()

    '''Обрабатывает столкновение корабля с пришельцем'''
    def _ship_hit(self):
        if self.stats.ships_left > 0:
            # Уменьшение ship_left
            self.stats.ships_left -= 1

            # Очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()

            # Пауза
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

        '''Проверяем, добрались ли пришельцы до нижнего края экрана'''
    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Уменьшение ship_left, Очистка списков пришельцев и снарядов, Создание нового флота и
                # размещение корабля в центре
                self._ship_hit()
                break

    '''Создание флота пришельцев'''
    def _create_fleet(self):
        alien = Alien(self)
        # Определяем высоту и ширину корабля пришельца
        alien_width, alien_height = alien.rect.size
        # Вычисляем доступное горизонтальное пространство и количество кораблей пришельцев в ряде
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        # Определяем количество рядов, помещающихся на экране
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (4 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        # Создание флота кораблей пришельцев
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

        # Создание пришельца и размещение его в ряду
    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    '''Реагирует на достижение пришельцем края экрана'''
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    '''Опускает флот и меняет направление движения'''
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    """Создаем звездное небо"""
    def _create_stars(self):
        # Создаем звезду
        star = Star(self)
        star_width, star_height = star.rect.size

        x_max = self.settings.screen_width - star_width
        y_max = self.settings.screen_height - star_height
        # Размещаем звезды по всему полю в случайном порядке
        for _ in range(50, 300):
            x_position = randint(star_width, x_max)
            y_position = randint(star_height, y_max)
            self._create_star(x_position, y_position)

    def _create_star(self, x_position, y_position):
        # Создаем звезду и помещаем ее в сетку (_create_stars)
        new_star = Star(self)
        new_star.rect.x = x_position
        new_star.rect.y = y_position

        self.stars.add(new_star)

    '''Обновление экрана при каждом проходе цикла'''
    def _update_screen(self):

        self.screen.fill(self.settings.bg_color)
        # Отображаем звездное небо
        self.stars.draw(self.screen)
        self.ship.blitme()
        # Отображаем все выпущенные снаряды
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # Отображаем корабль пришельца
        self.aliens.draw(self.screen)
        # Вывод информации о счете
        self.sb.show_score()
        # Отображение кнопки Play, если игра не активна
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.difficult_button.draw_button()

        # Отображение последнего прорисованного экрана
        pygame.display.flip()

if __name__ == '__main__':
    # Создаем экземпляр
    ai = AlienInvasion()
    # Запуск игры
    ai.run_game()