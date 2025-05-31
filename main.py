

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
GREEN = (0, 255, 0)

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
win_sound = pygame.mixer.Sound(os.path.join("Assets", "win.mp3"))
lose_sound = pygame.mixer.Sound(os.path.join("Assets", "lose.wav"))
explosion_sound = pygame.mixer.Sound(os.path.join(
    "Assets", "explosion_sound.wav"))  # فرض کردم این فایل هست

# بارگذاری مدل‌های گلوله
bullet_kind_1 = pygame.image.load(os.path.join("Assets", "bullet1.png"))
bullet_kind_2 = pygame.image.load(os.path.join("Assets", "bullet2.png"))

bullet_kind_1 = pygame.transform.scale(bullet_kind_1, (15, 5))
bullet_kind_2 = pygame.transform.scale(bullet_kind_2, (15, 5))


def get_bullet_kind():
    return random.choice([bullet_kind_1, bullet_kind_2])


def draw_window(blue, red, blue_bullets, red_bullets, blue_health, red_health):
    WIN.blit(BACKGROUND_IMAGE, (0, 0))
    pygame.draw.line(WIN, BLACK, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)

    # نمایش جان‌ها به صورت HUD بالا
    font = pygame.font.SysFont("Arial", 28, bold=True)
    blue_health_text = font.render(f"Blue Health: {blue_health}", True, BLUE)
    red_health_text = font.render(f"Red Health: {red_health}", True, RED)
    WIN.blit(blue_health_text, (10, 10))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

    # کشیدن سفینه‌ها
    WIN.blit(BLUE_SPACESHIP, (blue.x, blue.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    # کشیدن گلوله‌ها همراه مدل گلوله
    for bullet, kind in blue_bullets:
        WIN.blit(kind, (bullet.x, bullet.y))

    for bullet, kind in red_bullets:
        WIN.blit(kind, (bullet.x, bullet.y))

    pygame.display.update()


def draw_explosion(x, y):
    WIN.blit(EXPLOSION, (x, y))
    explosion_sound.play()
    pygame.display.update()
    pygame.time.delay(100)


def blue_movement(keys, blue):
    if keys[pygame.K_a] and blue.x - VEL > 0:
        blue.x -= VEL
    if keys[pygame.K_d] and blue.x + VEL + blue.width < WIDTH // 2:
        blue.x += VEL
    if keys[pygame.K_w] and blue.y - VEL > 0:
        blue.y -= VEL
    if keys[pygame.K_s] and blue.y + VEL + blue.height < HEIGHT:
        blue.y += VEL


def red_movement(red, blue):
    if red.y < blue.y and red.y + VEL + red.height < HEIGHT:
        red.y += VEL
    elif red.y > blue.y and red.y - VEL > 0:
        red.y -= VEL


def handle_bullets(blue_bullets, red_bullets, blue, red):
    for bullet, kind in blue_bullets[:]:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            draw_explosion(red.x, red.y)
            pygame.event.post(pygame.event.Event(RED_HIT))
            blue_bullets.remove((bullet, kind))
        elif bullet.x > WIDTH:
            blue_bullets.remove((bullet, kind))

    for bullet, kind in red_bullets[:]:
        bullet.x -= BULLET_VEL
        if blue.colliderect(bullet):
            draw_explosion(blue.x, blue.y)
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            red_bullets.remove((bullet, kind))
        elif bullet.x < 0:
            red_bullets.remove((bullet, kind))


def draw_winner(text, blue, red, blue_bullets, red_bullets, blue_health, red_health):
    draw_window(blue, red, blue_bullets, red_bullets,
                blue_health, red_health)  # بک‌گراند کامل بازی
    font = pygame.font.Font(None, 60)
    rendered_text = font.render(text, True, WHITE)
    instruction_font = pygame.font.Font(None, 30)
    restart_text = instruction_font.render(
        "Press R to Restart or Q to Quit", True, WHITE)

    WIN.blit(rendered_text, (WIDTH // 2 -
             rendered_text.get_width() // 2, HEIGHT // 2 - 50))
    WIN.blit(restart_text, (WIDTH // 2 -
             restart_text.get_width() // 2, HEIGHT // 2 + 20))
    pygame.display.update()


def main():
    blue = pygame.Rect(100, 200, 70, 50)  # اندازه سفینه درست شده
    red = pygame.Rect(700, 200, 70, 50)

    blue_bullets = []
    red_bullets = []

    blue_health = 15
    red_health = 15

    clock = pygame.time.Clock()
    run = True
    game_over = False
    winner_text = ""

    winner_shown = False

    while run:
        clock.tick(FPS)

        if game_over:
            if not winner_shown:
                draw_winner(winner_text, blue, red, blue_bullets,
                            red_bullets, blue_health, red_health)
                winner_shown = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main()
                        return
                    elif event.key == pygame.K_q:
                        run = False
                        break
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(blue_bullets) < MAX_BULLETS:
                    bullet_rect = pygame.Rect(
                        blue.x + blue.width, blue.y + blue.height // 2 - 2, 15, 5
                    )
                    bullet_image = get_bullet_kind()
                    blue_bullets.append((bullet_rect, bullet_image))
                    laser_sound.play()

            if event.type == BLUE_HIT:
                blue_health -= 1

            if event.type == RED_HIT:
                red_health -= 1

        keys = pygame.key.get_pressed()
        blue_movement(keys, blue)
        red_movement(red, blue)

        if len(red_bullets) < MAX_BULLETS and random.randint(1, 60) == 1:
            bullet_rect = pygame.Rect(
                red.x, red.y + red.height // 2 - 2, 15, 5
            )
            bullet_image = get_bullet_kind()
            red_bullets.append((bullet_rect, bullet_image))

        handle_bullets(blue_bullets, red_bullets, blue, red)
        draw_window(blue, red, blue_bullets,
                    red_bullets, blue_health, red_health)

        if blue_health <= 0:
            winner_text = "Red Wins!"
            lose_sound.play()
            game_over = True

        if red_health <= 0:
            winner_text = "Blue Wins!"
            win_sound.play()
            game_over = True

    pygame.quit()


if __name__ == "__main__":
    main()
