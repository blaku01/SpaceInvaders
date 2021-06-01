import pygame
import random

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders!")
YELLOW_SHIP = pygame.image.load("assets/pixel_ship_yellow.png")
BLUE_SHIP = pygame.image.load("assets/pixel_ship_blue_small.png")
GREEN_SHIP = pygame.image.load("assets/pixel_ship_green_small.png")
RED_SHIP = pygame.image.load("assets/pixel_ship_red_small.png")
BACKGROUND = pygame.transform.scale((pygame.image.load("assets/background-black.png")), (900, 500))


class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 25
        self.shot_cooldown = 60
        self.rect = YELLOW_SHIP.get_rect()

    def draw(self):
        WIN.blit(YELLOW_SHIP, (self.x, self.y))

    def shoot_bullet(self):
        player_bullets.append(Bullet(self.x + self.width/2, self.y + self.height, 4, (0, 255, 0)))


class Bullet(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y-100
        self.radius = radius
        self.color = color
        self.vel = 10

    def draw(self):
        pygame.draw.circle(WIN, self.color, (self.x, self.y), self.radius)

class Enemy(object):
    def __init__(self, x, y, width, height, vel, shoot_speed, typ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.shoot_speed = shoot_speed
        self.typ = typ


    def draw(self):
        if self.typ == 0:
            WIN.blit(BLUE_SHIP, (self.x, self.y))
        elif self.typ == 1:
            WIN.blit(GREEN_SHIP, (self.x, self.y))
        elif self.typ == 2:
            WIN.blit(RED_SHIP, (self.x, self.y))
clock = pygame.time.Clock()
FPS = 30


def redrawGameWindow():
    WIN.blit(BACKGROUND, (0, 0))
    player_ship.draw()
    for bullet in player_bullets:
        bullet.draw()
    for enemy in enemies:
        enemy.draw()
    pygame.display.update()


# MAIN LOOP
lives = 3
enemies = []
player_ship = Player(300, 410, 100, 90)
player_bullets = []
enemy_bullets = []
new_enemy_cooldown = 119
run = True
while run:
    new_enemy_cooldown += 1
    player_ship.shot_cooldown += 1
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()

    # PLAYER WINDOW COLLISION
    if keys[pygame.K_w] and player_ship.y >= player_ship.vel:
        player_ship.y -= player_ship.vel
    if keys[pygame.K_s] and player_ship.y <= (HEIGHT - player_ship.height - player_ship.vel - 10):
        player_ship.y += player_ship.vel
    if keys[pygame.K_a] and player_ship.x >= player_ship.vel - 30:
        player_ship.x -= player_ship.vel
    if keys[pygame.K_d] and player_ship.x <= (WIDTH - player_ship.width - player_ship.vel + 40):
        player_ship.x += player_ship.vel

    # CHECK IF PLAYER SHOT
    if keys[pygame.K_SPACE]:
        if player_ship.shot_cooldown > 20:
            player_ship.shot_cooldown = 0
            player_ship.shoot_bullet()

    # ENEMY MOVE
    if new_enemy_cooldown % 30 == 0:
        typ = random.randint(0, 3)
        if typ == 0:
            enemies.append(Enemy(random.randint(0, WIDTH-50), 0, 50, 50, random.randint(3, 5), random.randint(0, 5), typ))
        elif typ == 1:
            enemies.append(Enemy(random.randint(0, WIDTH-50), 0, 70, 50, random.randint(3, 5), random.randint(0, 5), typ))
        elif typ == 2:
            enemies.append(Enemy(random.randint(0, WIDTH-50), 0, 70, 50, random.randint(3, 5), random.randint(0, 5), typ))
    for enemy in enemies:
        if enemy.y > HEIGHT:
            lives -= 1
            enemies.pop(enemies.index(enemy))
        else:
            enemy.y += enemy.vel

    # BULLET COLLISION

    # ENEMY BULLET COLLISION

    # PLAYER BULLET COLLISION
    for bullet in player_bullets:
        for enemy in enemies:
            if (enemy.y + 10 + enemy.height) > bullet.y > (enemy.y + 10) and (enemy.x + 10) < bullet.x < (
                    enemy.x + 10 + enemy.width):
                enemies.pop(enemies.index(enemy))
                player_bullets.pop(player_bullets.index(bullet))
        if bullet.y > 0:
            bullet.y -= bullet.vel
        else:
            player_bullets.pop(player_bullets.index(bullet))
    redrawGameWindow()



pygame.quit()