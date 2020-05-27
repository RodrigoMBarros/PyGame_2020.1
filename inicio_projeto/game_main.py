import pygame as pg
import sys
import random
from formatacao_geral import *

WIDTH = 500
HEIGHT = 620
FPS = 30
NOME = "EU TESTANDO :)"
FONTE = 'arial'
#== Player properies
FAMOSO_ACEL = 5
FAMOSO_ATRI = -0.12  # atrito, força contrária ao movimento reduzindo a aceleração
GRAVIDADE = 1 
PULO_FAMOSO = 20


# colocar fração? e aceleração?

#== Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 127, 0)
LIGHTBLUE =(0, 155, 155)


# assets
# backgrond = pg.image.load("imagem.fundo.png").convert()

#=== Formatando plataformas

LISTA_plataformas = [(0, HEIGHT - 40, WIDTH, 40),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20),
                 (125, HEIGHT - 350, 100, 20),
                 (350, 200, 100, 20),
                 (175, 100, 50, 20)]

# ==== Classes 

# jogador#
class Famoso(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()  # gera a posição e tamanho da imagem

        # quantos pixels mexer/velocidade
        self.rect.x = WIDTH / 2
        self.rect.y = HEIGHT / 2  # gera posições x e y pro jogador
        self.Vy = 0
        self.Vx = 0
        self.grav = GRAVIDADE

    def update(self):

        # pulo
        self.Vy += self.grav
        # equações do movimento

        self.rect.y += self.Vy
        self.rect.x += self.Vx

        # limitando com a tela
        if self.rect.right > WIDTH:
            self.Vx = 0
        if self.rect.left < 0:
            self.Vx = 0

    def trata_eventos(self, event):  # Eventos para o jogador

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                self.Vx = -FAMOSO_ACEL
            if event.key == pg.K_RIGHT:
                self.Vx = FAMOSO_ACEL

        elif event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                self.Vx = 0
            if event.key == pg.K_RIGHT:
                self.Vx = 0

    # Plataformas - Notas#


class Notas(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# ===Classe do jogo
class Game:
    def __init__(self):

        # =====Iniciações
        pg.init()
        pg.mixer.init()  # musica
        self.rodando = True
        self.nome_fonte = pg.font.match_font(FONTE)

        # ======tela
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        # self.backgrond = pg.image.load("imagem.fundo.png").convert()
        pg.display.set_caption(NOME)
        self.clock = pg.time.Clock()  # tempo

    def refresh(self):
        # renicia o jogo quando morre, vai rodar um novo jogo // atualizações

        self.score = 0

        # ==== Grupo de sprits (personagens)
        self.all_sprites = pg.sprite.pygame.sprite.Group()
        self.jogador = Famoso()
        self.all_sprites.add(self.jogador)

        self.platforms = pg.sprite.Group()  # grupo para as plataformas
        for plat in LISTA_plataformas:
            p=Notas(*plat)   #explora todas a lista de forma quebrada 
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        # game Loop
        self.clock.tick(FPS)

        # ==== Chamando events e as tres funções básicas do game loop que se conversam
        self.events()
        self.updates()
        self.draw()

    def updates(self):
        # faz updates
        self.all_sprites.update()
        # checando colisões
        hits = pg.sprite.spritecollide(self.jogador, self.platforms, False)

        if hits: #verifica impacto entre jogador e a plataforma para realizar o pulo
           
            if ((self.jogador.Vy > 0 ) and ( self.jogador.rect.bottom > hits[0].rect.top) and ( self.jogador.rect.bottom < hits[0].rect.bottom )):
            
                self.jogador.rect.bottom = hits[0].rect.top
                self.jogador.Vy = -PULO_FAMOSO

        #Fazer a tela rodar quando o jogador chegar a 1/4 da tela 
        if self.jogador.rect.top <= HEIGHT/4:
            self.jogador.rect.y += abs(self.jogador.Vy)
            for plat in self.platforms:
                plat.rect.y += abs(self.jogador.Vy)
                if plat.rect.y >= HEIGHT:
                    plat.kill()
                    self.score += 10

        #Die 

        if self.jogador.rect.bottom > HEIGHT : 
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.jogador.Vy, 10)

                if sprite.rect.bottom < 0:
                    sprite.kill()

        if len(self.platforms) == 0: 
            self.rodando = False 

        #recolocando as plataformas: 
        while len(self.platforms) < 7:
            width = random.randrange(50,100)
            p=Notas(random.randrange(0,WIDTH - width),
                    random.randrange(-55,-30),
                    width, 20)
            self.platforms.add(p)
            self.all_sprites.add(p)


    def events(self):
        # Process input (events)
        events = pg.event.get()
        for event in events:
            # checando para sair do jogo
            if event.type == pg.QUIT:
                self.rodando = False
            self.jogador.trata_eventos(event)

    def draw(self):

        # Função para desenvolver imagens #

        self.screen.fill(LIGHTBLUE)
        # self.screen.blit(backgrond,(0,0))
        self.all_sprites.draw(self.screen)
        self.draw_textos(str(self.score), 22, WHITE, WIDTH/2 , 15)
        pg.display.flip()  # uma desenhada e outra em construção #*after* drawuing everything
        
    def draw_textos(self, text, size, color, x, y) :
        
        #Função pra desenvolver os textos nas telas 

        font = pg.font.Font(self.nome_fonte, size) #fonte
        texto_surface = font.render(text, True, color) #onde
        texto_rect = texto_surface.get_rect() #o que 
        texto_rect.midtop = (x,y) #onde do onde
        self.screen.blit(texto_surface, texto_rect) #taraw 


    def tela_inicial(self):

        # game go screen 
        
        self.screen.fill(LIGHTBLUE)
        self.draw_textos("Juppy!", 48, WHITE, WIDTH / 2, HEIGHT /4)

        #== Instruções
        self.draw_textos("Use as setas para se mover", 22, GREEN, WIDTH/2, HEIGHT / 2)
        self.draw_textos("Precione espaço para jogar", 22, GREEN, WIDTH/2, (HEIGHT* 3/4) )
        pg.display.flip()
        self.espera_acao()

    def tela_final(self):

        #Função para definir a tela final de gameover#

        if not self.rodando:  #se quiser sair não tem que mostrar a tela final 
            return
        self.screen.fill(LIGHTBLUE)
        # resultados 
        self.draw_textos("GAME OVER", 48, BLACK, WIDTH / 2, HEIGHT /4)
        self.draw_textos("Score = " + str(self.score), 22, GREEN, WIDTH/2, HEIGHT / 2)
        self.draw_textos("Precione espaço para jogar novamente", 22, GREEN, WIDTH/2, (HEIGHT* 3/4) )
        pg.display.flip()
        #self.espera_acao()

    def espera_acao(self):

        #Função para não bagunçar os eventos, e controlar o tempo e espera das telas iniciais e finais#

        esperando = True
        while esperando:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    esperando = False
                    self.rodando = False

                if event.type == pg.KEYUP:
                    if event.key == pg.K_SPACE:
                        esperando = False
            
g = Game()
g.tela_inicial()
while g.rodando:
    g.refresh()  # reniciar apenas no novo jogo
    g.run()
    g.tela_final()

pg.quit()
