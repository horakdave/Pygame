import pygame
import random
import time

screen_size = (1920, 1080)
box = pygame.Rect(0,0, screen_size[0], screen_size[1])

#Constants
WIDTH, HEIGHT = 800, 600
MARGIN = 25
BOX_WIDTH, BOX_HEIGHT = 300, 400
RADIUS = 15
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Bouncing Balls')

# Create the box
box = pygame.Rect(WIDTH // 2 - BOX_WIDTH // 2, HEIGHT // 2 - BOX_HEIGHT // 2, BOX_WIDTH, BOX_HEIGHT)
pygame.draw.rect(screen, BLACK, box, 2)

def detect_collision(circle, other_circles):
    for other_circle in other_circles:
        if id(circle) == id(other_circle):
            continue

        distance = (circle.centerx - other_circle.centerx) ** 2 + (circle.centery - other_circle.centery) ** 2
        radius_sum = circle.radius + other_circle.radius

        if distance <= radius_sum ** 2:
            return True

    return False

def out_of_box(circle, box):
    center, radius = circle
    top, left = center
    bottom, right = center
    return (top > box.bottom + radius or
            bottom < box.top - radius or
            left < box.left + radius or
            right > box.right - radius)

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x = random.randint(MARGIN, WIDTH - MARGIN)
            y = MARGIN
            radius = random.randint(RADIUS // 2, RADIUS)
            color = random.choice([RED, GREEN, BLUE, YELLOW])
            circle = pygame.draw.circle(screen, color, (x, y), radius)
            velocity = random.randint(1, 3)
            circles.append((circle, radius, color, velocity))

    return True

def update_screen(circles):
    for circle in circles:
        if out_of_box(circle, box) or detect_collision(circle, circles):
            print("GAME OVER")
            time.sleep(3600)
        
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, box, 2)

    for circle, radius, color, velocity in circles:
        circle.centery += velocity
        if out_of_box(circle) or detect_collision(circle, circles):
            circles.remove((circle, radius, color, velocity))

    for circle, radius, color, velocity in circles:
        pygame.draw.circle(screen, color, circle.center, radius)

    pygame.display.flip()

# Main loop
circles = []
running = True
while running:
    running = handle_events()

    update_screen(circles)

    pygame.time.Clock().tick(FPS)

pygame.quit()