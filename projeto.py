import pygame

pygame.init()

window = pygame.display.set_mode((900, 800))
pygame.display.set_caption('Musicando')

game = True

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    window.fill((255, 110, 0))

    pygame.display.update()

pygame.quit()
