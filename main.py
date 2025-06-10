import pygame
import random
from sys import exit

pygame.init()
pygame.display.set_caption("Game RPG with Falling Objects")

width = 1280
height = 720
screen = pygame.display.set_mode((width, height))

fps = 60
clock = pygame.time.Clock()

GRAVITY = 0.8
JUMP_STRENGTH = -20
PLAYER_SPEED = 12
OBJECT_SPEED = 10

w_ts = 1280
h_ts = 100
t_surface = pygame.Surface((w_ts, h_ts))
t_surface.fill('darkgreen')

sky = pygame.image.load('sky.png')
dern = pygame.image.load('dern.png')
player_image = pygame.image.load('player.png')
object_image = pygame.Surface((30, 30))
object_image.fill('red')
object_image = pygame.image.load('fireball.png')

player_x = 100
player_y = 465
player_width = player_image.get_width()
player_height = player_image.get_height()
player_velocity_y = 0
on_ground = False

falling_objects = []
object_spawn_timer = 0
game_over = False


font = pygame.font.SysFont(None, 72)

def spawn_object():
    obj_x = random.randint(0, width - object_image.get_width())
    obj_y = -object_image.get_height()
    falling_objects.append(pygame.Rect(obj_x, obj_y, object_image.get_width(), object_image.get_height()))

def check_collision():
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for obj in falling_objects:
        if player_rect.colliderect(obj):
            return True
    return False

running = True
while running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground and not game_over:
                player_velocity_y = JUMP_STRENGTH
                on_ground = False
            if event.key == pygame.K_r and game_over:
                game_over = False
                player_x = 100
                player_y = 465
                player_velocity_y = 0
                falling_objects = []
                object_spawn_timer = 0

    if not game_over:

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_x -= PLAYER_SPEED
        if keys[pygame.K_d]:
            player_x += PLAYER_SPEED

        player_velocity_y += GRAVITY
        player_y += player_velocity_y

        ground_level = height - player_height - h_ts
        if player_y >= ground_level:
            player_y = ground_level
            player_velocity_y = 0
            on_ground = True
        else:
            on_ground = False

        player_x = max(0, min(player_x, width - player_width))
        if player_y < 0:
            player_y = 0
            player_velocity_y = 0

        object_spawn_timer += 3
        if object_spawn_timer >= fps:
            spawn_object()
            object_spawn_timer = 0

            if random.random() < 0.3:
                spawn_object()

        for obj in falling_objects[:]:
            obj.y += OBJECT_SPEED
            if obj.y > height:
                falling_objects.remove(obj)

        if check_collision():
            game_over = True

    screen.blit(sky, (0, 0))
    screen.blit(t_surface, (0, height - h_ts))
    screen.blit(dern, (0, height - h_ts - 20))
    screen.blit(player_image, (player_x, player_y))

    for obj in falling_objects:
        screen.blit(object_image, obj)

    if game_over:
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        restart_text = font.render("Press R to restart", True, (255, 255, 255))
        screen.blit(game_over_text, (width//2 - game_over_text.get_width()//2, height//2 - 50))
        screen.blit(restart_text, (width//2 - restart_text.get_width()//2, height//2 + 50))

    pygame.display.update()

pygame.quit()