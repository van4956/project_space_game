import pygame
import sys
import os

def resource_path(relative_path):
    """Получить абсолютный путь к ресурсу, работает для dev и для PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class Ino(pygame.sprite.Sprite):
    """класс одного врага"""
    def __init__(self, screen):
        """инициализируем и задаем начальную позицию"""
        super(Ino, self).__init__()
        self.screen = screen
        self.image = pygame.image.load(resource_path('images/ino.png'))
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width - 1000
        self.rect.y = self.rect.height - 1000
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def draw(self):
        """вывод врага на экран"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """перемещает врагов"""
        self.y += 0.05
        self.rect.y = self.y
