'''Отслеживание статистики игры'''
class GameStats():
    '''Инициализируем статистику'''
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        # Игра запускается в активном состоянии
        self.game_active = False

    '''Инициализирует статистику, зменяющуюся в ходе игры'''
    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0