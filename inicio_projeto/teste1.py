"""Pygame template - skeleton for a pygame project"""

import pygame
import sys 
import random

#======medidas de formatação  

WIDTH = 360
HEIGHT = 480
FPS = 30

    # cores 
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)


#=====Iniciações 
pygame.init()
pygame.mixer.init()

#======tela 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Testando")
clock = pygame.time.Clock()

#==== Grupo de sprits (imagens)

all_sprites = pygame.sprite.pygame.sprite.Group()
#====Game loop 
funcionando = True 

while funcionando : 
    #keep running at the right speed
    clock.tick(FPS)
    # Process input (events)
    events = pygame.event.get()
    for event in events:
        #checando para sair do jogo
        if event.type == pygame.QUIT:
            funcionando = False 

    # Updates 
    all_sprites.update()

    # Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip() #uma desenhada e outra em construção #*after* drawuing everything 

#=== Saindo do jogo 
pygame.quit() 
