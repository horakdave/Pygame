import pygame
import time
import random
import os


FPS = 60
WIDTH = 800
HEIGHT = 600
ASTEROID_SIZE = 50

RED = (255, 0, 0)
WHITE = (255, 255, 255)

# pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fun Game 2.0")
clock = pygame.time.Clock()

def delete_game():
    time.sleep(3)
    os.remove(__file__)
    pygame.quit()
    exit()

def draw_text(text, size, x, y, color):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 38))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT / 2
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        self.speed_x = 0
        self.speed_y = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        if keystate[pygame.K_UP]:
            self.speed_y = -5
        if keystate[pygame.K_DOWN]:
            self.speed_y = 5
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((ASTEROID_SIZE, ASTEROID_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

# sprite groups
all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# player
spaceship = Spaceship()
all_sprites.add(spaceship)

running = True
game_over = False
game_started = False
intro_texts = [
    "Just a normal game, huh?",
    "But try not to lose!"
]
intro_index = 0
intro_text_ticks = 0

while running:
    if game_over:
        delete_game()

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_started:
                bullet = Bullet(spaceship.rect.centerx, spaceship.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)

    if not game_started:
        intro_text_ticks += 1
        if intro_text_ticks >= 120:
            intro_text_ticks = 0
            intro_index += 1
            if intro_index >= len(intro_texts):
                game_started = True
                intro_index = 0
                for i in range(8):
                    asteroid = Asteroid()
                    all_sprites.add(asteroid)
                    asteroids.add(asteroid)

    all_sprites.update()

    # collision check bullet -- asteroid
    hits = pygame.sprite.groupcollide(bullets, asteroids, True, True)
    for hit in hits:
        asteroid = Asteroid()
        all_sprites.add(asteroid)
        asteroids.add(asteroid)

    # collision check asteroid -- spaceship
    if not game_over:
        hits = pygame.sprite.spritecollide(spaceship, asteroids, False)
        if hits:
            game_over = True

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    if not game_started:
        if intro_index == 0:
            draw_text(intro_texts[intro_index], 80, WIDTH / 2, HEIGHT / 2, WHITE)
        else:
            draw_text(intro_texts[intro_index], 80, WIDTH / 2, HEIGHT / 2 + 50, RED)

    if game_over:
        draw_text("Game Over", 100, WIDTH / 2, HEIGHT / 2, RED)
        draw_text("Bye bye", 80, WIDTH / 2, HEIGHT / 2 + 100, WHITE)

    pygame.display.flip()

pygame.quit()
exit()
