import pygame
import time
import random

pygame.init()

width, height = 800, 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

white, black, red = (255, 255, 255), (0, 0, 0), (255, 0, 0)
snake_block, snake_speed = 10, 15
snake_list, snake_length = [], 1

x1, y1 = width / 2, height / 2
x1_change, y1_change = 0, 0

apple_x, apple_y = round(random.randrange(0, width - snake_block) / 10.0) * 10.0, round(random.randrange(0, height - snake_block) / 10.0) * 10.0

game_over = False
clock = pygame.time.Clock()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x1_change, y1_change = -snake_block, 0
            elif event.key == pygame.K_RIGHT:
                x1_change, y1_change = snake_block, 0
            elif event.key == pygame.K_UP:
                y1_change, x1_change = -snake_block, 0
            elif event.key == pygame.K_DOWN:
                y1_change, x1_change = snake_block, 0

    x1 += x1_change
    y1 += y1_change

    if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
        game_over = True

    if x1 == apple_x and y1 == apple_y:
        apple_x, apple_y = round(random.randrange(0, width - snake_block) / 10.0) * 10.0, round(random.randrange(0, height - snake_block) / 10.0) * 10.0
        snake_length += 1

    display.fill(black)
    pygame.draw.rect(display, red, [apple_x, apple_y, snake_block, snake_block])

    snake_head = [x1, y1]
    snake_list.append(snake_head)
    if len(snake_list) > snake_length:
        del snake_list[0]

    for segment in snake_list[:-1]:
        if segment == snake_head:
            game_over = True

    for block in snake_list:
        pygame.draw.rect(display, white, [block[0], block[1], snake_block, snake_block])

    pygame.display.update()
    clock.tick(snake_speed)

pygame.quit()
