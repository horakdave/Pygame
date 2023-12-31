import pygame
import random
import time

pygame.init()

WINDOW_WIDTH = 1920 #sirska
WINDOW_HEIGHT = 1080 #vyska
WINDOW_TITLE = "Flappy Bird"
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

bg_image = pygame.image.load("background.png").convert()

#                                                                                   Background
bg_image = pygame.transform.scale(bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

bird_image = pygame.image.load("bird.png").convert_alpha()

pipe_image = pygame.image.load("pipe.png").convert_alpha()
pipe_image = pygame.transform.scale(pipe_image, (200, 600)) #                       Pipe


FPS = 60
clock = pygame.time.Clock()
bird_rect = bird_image.get_rect(center=(50, WINDOW_HEIGHT / 2))
gravity = 0.35
bird_movement = 0
pipe_gap = 400 #                                                                    gap
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
 
def handle_input():
    global bird_movement

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 8

def update_game():
    global bird_movement

    bird_movement += gravity
    bird_rect.centery += bird_movement

    for pipe in pipe_list:
        pipe.centerx -= 2

    if len(pipe_list) > 0 and pipe_list[0].centerx < -50:
        pipe_list.pop(0)

    #                                                                               overlapping
    if len(pipe_list) < 4:
        pipe_height = random.choice([500, 600, 700, 800, 900])
        bottom_pipe = pipe_image.get_rect(midtop=(1920, pipe_height))
        top_pipe = pipe_image.get_rect(midbottom=(1920, pipe_height - pipe_gap))
        if not any(pipe.colliderect(other_pipe) for other_pipe in pipe_list):
            pipe_list.append(bottom_pipe)
            pipe_list.append(top_pipe)

def draw_game():
    window.blit(bg_image, (0, 0))

    window.blit(bird_image, bird_rect)

    #                                                                                   pipe
    for pipe in pipe_list:
        if pipe.bottom >= WINDOW_HEIGHT:
            window.blit(pipe_image, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_image, False, True)
            window.blit(flip_pipe, pipe)

    pygame.display.update()

while True:
    handle_input()

    update_game()

    draw_game()

    clock.tick(FPS)
