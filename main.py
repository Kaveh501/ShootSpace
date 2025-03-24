

import pygame
import os
import random

# تنظیمات اولیه
pygame.init()

# ابعاد صفحه
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Battle")

# رنگ‌ها
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# FPS و سرعت
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 5

# رویدادهای برخورد
BLUE_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# بارگذاری تصاویر
BACKGROUND_IMAGE = pygame.image.load(os.path.join("Assets", "background.jpg"))
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))

BLUE_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "space_blue.png"))
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "space_blue2.png"))
EXPLOSION_IMAGE = pygame.image.load(os.path.join("Assets", "explosion.png"))

BLUE_SPACESHIP = pygame.transform.scale(BLUE_SPACESHIP_IMAGE, (70, 50))
RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP_IMAGE, (70, 50))
EXPLOSION = pygame.transform.scale(EXPLOSION_IMAGE, (50, 50))

# بارگذاری صدا
pygame.mixer.init()
laser_sound = pygame.mixer.Sound(os.path.join("Assets", "laser_gun.mp3"))

# تابع برای رسم عناصر در صفحه


def draw_window(blue, red, blue_bullets, red_bullets, blue_health, red_health):
    WIN.fill(WHITE)
    WIN.blit(BACKGROUND_IMAGE, (0, 0))

    pygame.draw.line(WIN, BLACK, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)

    # نمایش سلامت
    font = pygame.font.Font(None, 30)
    blue_health_text = font.render(f"Health: {blue_health}", True, BLUE)
    red_health_text = font.render(f"Health: {red_health}", True, RED)
    WIN.blit(blue_health_text, (10, 10))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

    WIN.blit(BLUE_SPACESHIP, (blue.x, blue.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in blue_bullets:
        pygame.draw.rect(WIN, BLUE, bullet)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()

# تابع نمایش انفجار


def draw_explosion(x, y):
    WIN.blit(EXPLOSION, (x, y))
    pygame.display.update()
    pygame.time.delay(100)

# کنترل حرکت سفینه آبی


def blue_movement(keys, blue):
    if keys[pygame.K_a] and blue.x - VEL > 0:
        blue.x -= VEL
    if keys[pygame.K_d] and blue.x + VEL + blue.width < WIDTH // 2:
        blue.x += VEL
    if keys[pygame.K_w] and blue.y - VEL > 0:
        blue.y -= VEL
    if keys[pygame.K_s] and blue.y + VEL + blue.height < HEIGHT:
        blue.y += VEL

# کنترل حرکت سفینه قرمز


def red_movement(red, blue):
    if red.y < blue.y and red.y + VEL + red.height < HEIGHT:
        red.y += VEL
    elif red.y > blue.y and red.y - VEL > 0:
        red.y -= VEL

# مدیریت گلوله‌ها


def handle_bullets(blue_bullets, red_bullets, blue, red):
    for bullet in blue_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            draw_explosion(red.x, red.y)
            pygame.event.post(pygame.event.Event(RED_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            blue_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if blue.colliderect(bullet):
            draw_explosion(blue.x, blue.y)
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

# حلقه اصلی بازی


def main():
    blue = pygame.Rect(100, 200, 50, 40)
    red = pygame.Rect(700, 200, 50, 40)

    blue_bullets = []
    red_bullets = []

    blue_health = 15
    red_health = 15

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(blue_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        blue.x + blue.width, blue.y + blue.height // 2 - 2, 10, 5
                    )
                    blue_bullets.append(bullet)
                    laser_sound.play()

            if event.type == BLUE_HIT:
                blue_health -= 1

            if event.type == RED_HIT:
                red_health -= 1

        keys = pygame.key.get_pressed()
        blue_movement(keys, blue)

        red_movement(red, blue)
        if len(red_bullets) < MAX_BULLETS and random.randint(1, 60) == 1:
            bullet = pygame.Rect(
                red.x, red.y + red.height // 2 - 2, 10, 5
            )
            red_bullets.append(bullet)

        handle_bullets(blue_bullets, red_bullets, blue, red)
        draw_window(blue, red, blue_bullets,
                    red_bullets, blue_health, red_health)

        if blue_health <= 0:
            winner_text = "Red Wins!"
            break

        if red_health <= 0:
            winner_text = "Blue Wins!"
            break

    font = pygame.font.Font(None, 60)
    text = font.render(winner_text, True, WHITE)
    WIN.blit(text, (WIDTH // 2 - text.get_width() //
             2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(3000)

    pygame.quit()


if __name__ == "__main__":
    main()
