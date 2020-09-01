import pygame
import sys
import random


# Pipe creator


def create_pipe():
    random_pipe_pos = random.choice(pipes_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))
    return bottom_pipe, top_pipe

# Move the pipes


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

# Draw the Pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

# Floor "mozgás"


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))

# Check Collision


def check_collision(pipes):
    for pipe in pipes:
        if tiger_rect.colliderect(pipe):
            lose_sound.play()
            return False

    if tiger_rect.top <= -100 or tiger_rect.bottom >= 900:
        lose_sound.play()
        return False

    return True

# Rotate


def rotate_tiger(tiger):
    new_tiger = pygame.transform.rotozoom(tiger, -tiger_speed * 3, 1)
    return new_tiger

# Animation


def tiger_animation():
    new_tiger = tiger_frames[tiger_index]
    new_tiger_rect = new_tiger.get_rect(center=(100, tiger_rect.centery))
    return new_tiger, new_tiger_rect

# Score Displaying


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center=(288,80))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 80))
        screen.blit(score_surface, score_rect)

        # High Score

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 850))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.mixer.pre_init(frequency= 44100, size= 16, channels= 1, buffer=512)
pygame.init()
# Caption
pygame.display.set_caption("Flappy Tiger: Ultimate Knockout")
# Font
game_font = pygame.font.Font('ka1.ttf', 40)

screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()

# Images

bg_surface = pygame.transform.scale2x(pygame.image.load('assets/background.png').convert())

floor_surface = pygame.transform.scale2x(pygame.image.load('assets/base.png').convert())
floor_x_pos = 0

# Tiger

tiger_down = pygame.transform.scale2x(pygame.image.load('assets/Tiger-Down.png').convert_alpha())
tiger_normal = pygame.transform.scale2x(pygame.image.load('assets/Tiger-Normal.png').convert_alpha())
tiger_up = pygame.transform.scale2x(pygame.image.load('assets/Tiger-Up.png').convert_alpha())
tiger_frames = [tiger_down, tiger_normal, tiger_up]
tiger_index = 0
tiger_surface = tiger_frames[tiger_index]
tiger_rect = tiger_surface.get_rect(center=(100, 512))


TIGERJUMP = pygame.USEREVENT + 1
pygame.time.set_timer(TIGERJUMP, 200)

# Game over img

game_over_surface = pygame.image.load('assets/main.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(288,512))

# Sounds

jump_sound = pygame.mixer.Sound('sound/sfx_jump.wav')
lose_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 130

# Pipes

pipe_surface = pygame.image.load('assets/pipe-black.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipes_list = []

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipes_height = [400, 600, 800]


# Game Variables
game_gravity = 0.2
tiger_speed = 0
game_active = False
score = 0
high_score = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                tiger_speed = 0
                tiger_speed -= 12
                jump_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipes_list.clear()
                tiger_rect.center = (100, 512)
                tiger_speed = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipes_list.extend(create_pipe())
            if game_active and score_sound_countdown <= 0:
                score_sound.play()
                score += 1
                score_sound_countdown = 100

        if event.type == TIGERJUMP:
            if tiger_index < 2:
                tiger_index += 1
            else:
                tiger_index = 0

            tiger_surface, tiger_rect = tiger_animation()

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # Bird movement
        tiger_speed += game_gravity
        rotated_tiger = rotate_tiger(tiger_surface)
        tiger_rect.centery += int(tiger_speed)
        screen.blit(rotated_tiger, tiger_rect)
        # Collision
        game_active = check_collision(pipes_list)
        # Pipes
        pipes_list = move_pipes(pipes_list)
        draw_pipes(pipes_list)
        # Score
        score_sound_countdown -= 1
        score_display('main_game')

    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')
        score_sound_countdown = 200

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    # Mindig előtte kell lennie  és felé a rajzokat amit szeretnénk
    pygame.display.update()
    clock.tick(120)
