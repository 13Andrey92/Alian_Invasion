import json
from pathlib import Path
'''Отслеживание статистики игры'''
class GameStats():
    '''Инициализируем статистику'''
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        # Игра запускается в активном состоянии
        self.game_active = False

        # Сохранение рекорда при перезапуске игры
        self.high_score = self.get_saved_high_score()

    '''Получаем рекорд из существующего файла'''
    def get_saved_high_score(self):
        path = Path('high_score.json')
        try:
            contents = path.read_text()
            high_score = json.loads(contents)
            return high_score
        except FileNotFoundError:
            return 0

    '''Инициализирует статистику, заменяющуюся в ходе игры'''
    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1