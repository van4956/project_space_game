import os

class Stats():
    """класс отслеживание статистики"""

    def __init__(self):
        """инициализируем статистику"""
        self.reset_stats()
        self.run_game = True
        self.high_score = 0
        self.load_high_score()

    def reset_stats(self):
        """статистика изменений в игре"""
        self.guns_left = 2
        self.score = 0

    def load_high_score(self):
        """загрузка рекорда"""
        try:
            if os.path.exists('score_stats.txt'):
                with open('score_stats.txt', 'r') as file:
                    self.high_score = int(file.readline())
            else:
                self.high_score = 0
        except:
            self.high_score = 0

    def save_high_score(self):
        """сохранение рекорда"""
        try:
            with open('score_stats.txt', 'w') as file:
                file.write(str(self.high_score))
        except:
            pass
