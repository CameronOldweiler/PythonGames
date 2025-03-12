import pygame
from sys import exit

screen_size = (800, 400)
pygame.init()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('Fonts/Pixeltype.ttf', 50)

sky_surface = pygame.image.load('Graphics/Runner Game/Sky.png').convert()
ground_surface = pygame.image.load('Graphics/Runner Game/ground.png').convert()
text_surface = test_font.render('My Game', False, 'Black')

player_surface = pygame.image.load('Graphics/Runner Game/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80, 300))

snail_surface = pygame.image.load('Graphics/Runner Game/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom = (600, 300))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))
    screen.blit(text_surface, (325, 40))

    snail_rect.left -= 4
    if snail_rect.right <= 0:
        snail_rect.left = 800

    screen.blit(snail_surface, snail_rect)
    screen.blit(player_surface, player_rect)

    # if player_rect.collidepoint(snail_rect):
    #     print('Collision')

    # mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint((mouse_pos)):
    #     print('Collision')

    pygame.display.update()
    clock.tick(60)