"""Pygame template - skeleton for a pygame project"""

import pygame
import sys 
import random

#======medidas de formatação  

WIDTH = 800
HEIGHT = 600
FPS = 30

    # cores 
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)

# ======= Classes 

class Player(pygame.sprite.Sprite):
    #sprite for the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)

    #serve para fazer uploodds de como vai se mover 
    def update(self):  
        self.rect.x +=5
        if self.rect.left > WIDTH:
            self.rect.right = 0 




#=====Iniciações 
pygame.init()
pygame.mixer.init()

#======tela 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Testando")
clock = pygame.time.Clock()

#===== Chamando classes 
player = Player() 
#==== Grupo de sprits (imagens)

all_sprites = pygame.sprite.pygame.sprite.Group()
all_sprites.add(player)
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
