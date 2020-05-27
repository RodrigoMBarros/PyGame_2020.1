import pygame as pg
import sys
import random

WIDTH = 500
HEIGHT = 620
FPS = 30
NOME = "EU TESTANDO :)"

# player properies
FAMOSO_ACEL = 5
FAMOSO_ATRI = -0.12  # atrito, força contrária ao movimento reduzindo a aceleração

# colocar fração? e aceleração?

# cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 127, 0)


# assets
# backgrond = pg.image.load("imagem.fundo.png").convert()

# ==== Classes 

# jogador#
class Famoso(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        #  exemplo de como puxar a imagem do sprite:
        #  self.image = pygame.image.load('assets/img/meteorBrown_med1.png').convert_alpha()
        #  self.image = pygame.transform.scale(self.image, (METEOR_WIDTH, METEOR_HEIGHT))
        self.image = pg.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()  # gera a posição e tamanho da imagem

        # quantos pixels mexer/velocidade
        self.rect.x = WIDTH / 2
        self.rect.y = HEIGHT / 2  # gera posições x e y pro jogador
        self.Vy = 0
        self.Vx = 0
        self.grav = 1

    def update(self):
        # equações do movimento

        # pulo
        self.Vy += self.grav
        self.rect.y += self.Vy
        self.rect.x += self.Vx

        # limitando com a tela nos lados
        if self.rect.right > WIDTH:
            self.Vx = 0
        if self.rect.left < 0:
            self.Vx = 0

    def trata_eventos(self, event):  # açoes do jogador: controlar o movimento lateral (eixo x)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                self.Vx = -FAMOSO_ACEL
            if event.key == pg.K_RIGHT:
                self.Vx = FAMOSO_ACEL

        elif event.type == pg.KEYUP:  # garante que pare de ir pro lado quando solta as teclas

            if event.key == pg.K_LEFT:

                if self.Vx < 0:
                    self.Vx = 0

            if event.key == pg.K_RIGHT:

                if self.Vx > 0:
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

        # ======tela
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        # self.backgrond = pg.image.load("imagem.fundo.png").convert()
        pg.display.set_caption(NOME)
        self.clock = pg.time.Clock()  # tempo

    def refresh(self):
        # renicia o jogo quando morre, vai rodar um novo jogo // atualizações

        # ==== Grupo de sprits (personagens)
        self.all_sprites = pg.sprite.pygame.sprite.Group()
        self.jogador = Famoso()
        self.all_sprites.add(self.jogador)

        self.platforms = pg.sprite.Group()  # grupo para as plataformas
        p1 = Notas(0, (HEIGHT - 40), WIDTH, 40)
        p2 = Notas(WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20)
        self.all_sprites.add(p1)
        self.platforms.add(p1)
        self.all_sprites.add(p2)
        self.platforms.add(p2)
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

        if hits:  # verifica impacto entre o jogador e a plataforma para realizar o pulo
            if self.jogador.Vy > 0 and self.jogador.rect.bottom > hits[0].rect.top and self.jogador.rect.bottom < hits[
                0].rect.bottom:
                self.jogador.rect.bottom = hits[0].rect.top
                self.jogador.Vy = -15

    def events(self):
        # Process input (events)
        events = pg.event.get()
        for event in events:
            # checando para sair do jogo
            if event.type == pg.QUIT:
                self.rodando = False
            self.jogador.trata_eventos(event)

    def draw(self):
        self.screen.fill(ORANGE)
        # self.screen.blit(backgrond,(0,0))
        self.all_sprites.draw(self.screen)
        pg.display.flip()  # uma desenhada e outra em construção #*after* drawuing everything

    def tela_inicial(self):
        pass

    def tela_final(self):
        pass


g = Game()
g.tela_inicial()
g.refresh()  # reniciar apenas no novo jogo
while g.rodando:
    g.run()
    g.tela_final()

pg.quit()
