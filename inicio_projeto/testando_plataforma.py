import pygame as pg
import sys 
import random
vec =pg.math.Vector2  #numeros com x e y } para poder ter variáveis pros dois 
#from formatação_geral import *

WIDTH = 500
HEIGHT = 620
FPS = 30
NOME = "EU TESTANDO :)"

#player properies 
FAMOSO_ACEL = 0.5
FAMOSO_ATRI = -0.12 #atrito, força contrária ao movimento reduzindo a aceleração


#colocar fração? e aceleração?

    # cores 
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)

    #assets
#backgrond = pg.image.load("imagem.fundo.png").convert()

# ==== Classes 

class Famoso(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30,40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect() #gera a posição e tamanho da imagem 

        self.rect.center = (WIDTH / 2, HEIGHT/2)

        #quantos pixels mexer/velocidade 
        self.pos = vec(WIDTH /2, HEIGHT/2) #gera posições x e y pro jogador  
        self.velo = vec(0,0) #velocidade 
        self.acel = vec(0,0) #aceleração 

    def update(self):
           
        #aplica o atrito 
        self.acel.x += self.velo.x * FAMOSO_ATRI
        
        #equações do movimento 
        self.velo += self.acel
        self.pos += self.velo + 0.5 * self.acel  

        #limitando com a tela
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        #centro da imagem na posição calculada 
        self.rect.center = self.pos 

    def trata_eventos(self, event):

        
        #=====Eventos para o jogador 
        
        self.acel =  vec(0,0.5) #quando nada é apertado /vy= gravidade 
        if event.type == pg.KEYDOWN:

            if event.key == pg.K_LEFT:
                self.acel.x = -FAMOSO_ACEL
            if event.key == pg.K_RIGHT:
                self.acel.x = FAMOSO_ACEL

        if event.type == pg.KEYUP:

            if event.key == pg.K_LEFT :
                self.acel.x = 0
            if event.key == pg.K_RIGHT:
                self.acel.x = 0




class Notas(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill((GREEN))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        




class Game:
    def __init__(self): 

        #=====Iniciações 
        pg.init()
        pg.mixer.init() #musica
        self.rodando = True


        #======tela 
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        #self.backgrond = pg.image.load("imagem.fundo.png").convert()
        pg.display.set_caption(NOME)
        self.clock = pg.time.Clock()  #tempo
         

    def refresh(self):
        #renicia o jogo quando morre, vai rodar um novo jogo // atualizações 

        #==== Grupo de sprits (personagens)
        self.all_sprites = pg.sprite.pygame.sprite.Group()
        self.jogador = Famoso()
        self.all_sprites.add(self.jogador)

        self.platforms = pg.sprite.Group() #para as plataformas 
        p1 = Notas( 0, HEIGHT-40, WIDTH, 40 )
        self.platforms.add(p1)
        self.run()

    def run(self):
        #game Loop 
        self.clock.tick(FPS)

        #==== Chamando events e as tres funções básicas do game loop que se conversam 
        self.events()
        self.updates()
        self.draw()

    
    def updates (self):
        #faz updates
        self.all_sprites.update()

    def events(self):
        # Process input (events)
        events = pg.event.get()
        for event in events:
            #checando para sair do jogo
            if event.type == pg.QUIT:
                self.rodando = False
            self.jogador.trata_eventos(event)

    def draw(self):
        self.screen.fill(BLACK)
        #self.screen.blit(backgrond,(0,0))
        self.all_sprites.draw(self.screen)
        pg.display.flip() #uma desenhada e outra em construção #*after* drawuing everything 

    def tela_inicial(self):
        pass
    
    def tela_final(self):
        pass

g = Game()
g.tela_inicial()
g.refresh() #reniciar apenas no novo jogo 
while g.rodando:
    
    g.run()
    g.tela_final()

pg.quit()

