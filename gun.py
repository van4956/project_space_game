import sys
import os
import pygame
from pygame.sprite import Sprite

def resource_path(relative_path):
    """Получить абсолютный путь к ресурсу, работает для dev и для PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class Gun(Sprite):
    def __init__(self, screen):
        """инициальзация пушки/танка"""
        super(Gun, self).__init__()
        self.screen = screen
        self.image = pygame.image.load(resource_path('images/gun.png'))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.center = float(self.rect.centerx)
        self.rect.bottom = self.screen_rect.bottom - 15
        self.mright = False
        self.mleft = False
        self.speed = 0
        self.max_speed = 3
        self.acceleration = 0.2
        self.deceleration = 0.1

    def output(self):
        """отрисовка пушки/танка"""
        self.screen.blit(self.image, self.rect)

    def update_gun(self):
        """обновления позиции пушки/танка"""
        # Ускорение при движении
        if self.mright and self.rect.right < self.screen_rect.right:
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        elif self.mleft and self.rect.left > 0:
            self.speed = max(self.speed - self.acceleration, -self.max_speed)
        # Замедление при отсутствии движения
        else:
            if self.speed > 0:
                self.speed = max(0, self.speed - self.deceleration)
            elif self.speed < 0:
                self.speed = min(0, self.speed + self.deceleration)

        # Применяем скорость к позиции
        self.center += self.speed
        self.rect.centerx = self.center

    def create_gun(self):
        """размещает танк в центре внизу"""
        self.center = self.screen_rect.centerx
        self.speed = 0
