import sys
import os
import time
import pygame
from bullet import Bullet
from ino import Ino

def resource_path(relative_path):
    """Получить абсолютный путь к ресурсу, работает для dev и для PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def events(screen, gun, bullets):
    """обработка событий"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # """кнопка зажата"""
        elif event.type == pygame.KEYDOWN:
            # вправо
            if event.key == pygame.K_RIGHT:
                gun.mright = True
            # влево
            elif event.key == pygame.K_LEFT:
                gun.mleft = True
            # пробел
            elif event.key == pygame.K_SPACE:
                new_bullet = Bullet(screen, gun)
                bullets.add(new_bullet)
        # """кнопка отжата"""
        elif event.type == pygame.KEYUP:
            # правая
            if event.key == pygame.K_RIGHT:
                gun.mright = False
            # левая
            elif event.key == pygame.K_LEFT:
                gun.mleft = False

def update(bg_color, screen, stats, sc, gun, ino, bullets):
    """обновление экрана"""
    screen.fill(bg_color)
    sc.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    gun.output()
    ino.draw(screen)
    pygame.display.flip()

def update_bullets(screen, stats, sc, inos, bullets):
    """обновлять позиции пуль"""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    collisions = pygame.sprite.groupcollide(bullets, inos, True, True)
    if collisions:
        for inos in collisions.values():
            stats.score += 10 * len(inos)
        sc.image_score()
        check_high_score(stats, sc)
        sc.image_guns()
    if len(inos) == 0:
        bullets.empty()
        create_army(screen, inos)

def gun_kill(stats, screen, sc, gun, inos, bullets):
    """столкновение пушки и врагов"""
    if stats.guns_left > 0:
        stats.guns_left -= 1
        sc.image_guns()
        inos.empty()
        bullets.empty()
        create_army(screen, inos)
        gun.create_gun()
        time.sleep(4)
    else:
        stats.run_gun = False
        sys.exit()


def update_inos(stats, screen, sc, gun, inos, bullets):
    """обновляет позицию врагов"""
    inos.update()
    if pygame.sprite.spritecollideany(gun, inos):
        gun_kill(stats, screen, sc, gun, inos, bullets)
    inos_chek(stats, screen, sc, gun, inos, bullets)

def inos_chek(stats, screen, sc, gun, inos, bullets):
    """проверка армия край """
    screen_rect = screen.get_rect()
    for ino in inos.sprites():
        if ino.rect.bottom >= screen_rect.bottom:
            gun_kill(stats, screen, sc, gun, inos, bullets)
            break


def create_army(screen, inos):
    """создание армии врагов"""
    ino = Ino(screen)
    ino_width = ino.rect.width
    number_ino_x = int((1200 - 2 * ino_width) / ino_width)
    ino_height = ino.rect.height
    number_ino_y = int((700 - 100 - 2 * ino_height) / ino_height)

    for row_number in range(number_ino_y - 1):
        for ino_number in range(number_ino_x):
            ino = Ino(screen)
            ino.x = ino_width + ino_width * ino_number
            ino.y = ino_height + ino_height * row_number
            ino.rect.x = ino.x
            ino.rect.y = ino.rect.height + ino_height * row_number
            inos.add(ino)

def check_high_score(stats, sc):
    """проверка новых рекордов"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sc.image_high_score()
        stats.save_high_score()
