import pygame as pg
import random
from os import path  #para criarar meios de se encontrar um arquivo 

WIDTH = 500
HEIGHT = 620
FPS = 30
NOME = "Juppy"
FONTE = 'arial'
HS_FILE = "highscore.txt"
SPRITESHEET = "p1_spritesheet.png"

# == Player properies
FAMOSO_ACEL = 8
GRAVIDADE = 1
PULO_FAMOSO = 22

# == Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 97, 3)
LIGHTBLUE = (10, 155, 155)

# assets
# backgrond = pg.image.load("imagem.fundo.png").convert()

# === Formatando plataformas

LISTA_plataformas_iniciais = [(0, HEIGHT - 40, WIDTH, 40),
                              (200, 440, 100, 20),
                              (125, 320, 100, 20),
                              (350, 200, 100, 20),
                              (175, 80, 50, 20),
                              (100, -30, 100, 20),
                              (300, -140, 100, 20),
                              (400, -250, 50, 20),
                              (350, -360, 100, 20),
                              (175, -470, 70, 20)]

LISTA_aleatorias_inciais = [(60, 180, 100, 20),
                            (375, 40, 100, 20),
                            (400, 350, 50, 20),
                            (30, -250, 50, 20),
                            (370, -450, 100, 20)]


# ==== Classes

# Player sprites #
class Spritessheets:
    #carregando e lendo as sprites na imagem geral 
    def __init__(self, filename) : 
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        #pega uma imagem do spritesheet 
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height) )
        return image

# jogador#
class Famoso(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.spritesheet.get_image(0, 196, 66, 92)
        #self.image.fill(ORANGE)
        self.rect = self.image.get_rect()  # gera a posição e tamanho da imagem
        self.maior_altura = self.rect.bottom

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

        # Se subindo, atualiza a maior altura atingida
        if self.Vy < 0:
            self.maior_altura = self.rect.bottom

        # atravessando a tela de um lado pro outro
        if self.rect.right > WIDTH:
            self.rect.left = 0
        if self.rect.left < 0:
            self.rect.right = WIDTH

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

    # Plataformas - Notas


class Notas_regulares(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Notas_aleatorias(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# ===Classe do jogo
class Game:
    def __init__(self):

        # =====Iniciações
        pg.init()
        self.jogador = Famoso()
        self.all_sprites = pg.sprite.pygame.sprite.Group()
        
        pg.mixer.init()  # musica
        self.rodando = True  # define o looping do gameplay
        self.jogo = True  # define o looping do programa
        self.nome_fonte = pg.font.match_font(FONTE)
        self.load_data()

        # ======tela
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        # self.backgrond = pg.image.load("imagem.fundo.png").convert()
        pg.display.set_caption(NOME)
        self.clock = pg.time.Clock()  # tempo

    def load_data(self):
        #carrega o high sore
        self.dir = path.dirname(__file__)  #usado para encontrar o folder do arquivo 
        img_dir = path.join(self.dir, 'img')

        with open(path.join(self.dir, HS_FILE), 'w') as ah:#abre o file para escrevermos, olhar, ou criar
            try:
                self.highscore = int(ah.read())
            except:
                self.highscore = 0
        
        #carrega imagens das sprites
        self.spritesheet = Spritessheets(path.join(img_dir, SPRITESHEET))
    def refresh(self):  # renicia o jogo quando morre, vai rodar um novo jogo // atualizações
        self.score = 0

        # ==== Grupo de sprits (personagens)
        self.all_sprites.add(self.jogador)
        self.jogador.rect.x = WIDTH / 2  # devolve o jogador para a posicao original
        self.jogador.rect.y = HEIGHT / 2
        self.jogador.Vy = 0  # devolve jogador para a velocidade original

        #=== Grupo de spreites plataformas
        self.platforms_R = pg.sprite.Group()  # grupo para as plataformas regulares
        self.platforms_A = pg.sprite.Group()  # grupo para as plataformas aleatorias
        
        for plat in LISTA_plataformas_iniciais:
            p = Notas_regulares(*plat)  # explora todas a lista de forma quebrada
            self.all_sprites.add(p)
            self.platforms_R.add(p)

        for plat in LISTA_aleatorias_inciais:
            p = Notas_aleatorias(*plat)  # explora todas a lista de forma quebrada
            self.all_sprites.add(p)
            self.platforms_A.add(p)

    def run(self):
        # game Loop
        self.clock.tick(FPS)

        # ==== Chamando events e as tres funções básicas do game loop que se conversam
        self.events()  # recebe comandos do taclado e mouse (controle do jogador)
        self.updates()
        self.draw()

    def updates(self):
        # faz updates
        self.all_sprites.update()
        # checando colisões
        hits = pg.sprite.spritecollide(self.jogador, self.platforms_R, False)  # contato com as plataformas regulares
        hits2 = pg.sprite.spritecollide(self.jogador, self.platforms_A, False)  # contato com as plataformas aleatorias

        if hits:  # verifica impacto entre jogador e as plataformas regulares para realizar o pulo
            
            if (self.jogador.Vy > 0) and (self.jogador.rect.bottom > hits[0].rect.top) and (self.jogador.maior_altura < hits[0].rect.top):
                self.jogador.rect.bottom = hits[0].rect.top
                self.jogador.Vy = -PULO_FAMOSO

        if hits2:  # verifica impacto entre jogador e as plataformas aleatorias para realizar o pulo

            if (self.jogador.Vy > 0) and (self.jogador.rect.bottom > hits2[0].rect.top) and (self.jogador.maior_altura < hits2[0].rect.top):
                self.jogador.rect.bottom = hits2[0].rect.top
                self.jogador.Vy = -PULO_FAMOSO

        # Fazer a tela rodar quando o jogador chegar a 1/4 da tela
        if self.jogador.rect.top <= HEIGHT / 4:
            self.jogador.rect.y += abs(self.jogador.Vy)
            for plat in self.platforms_R:
                plat.rect.y += abs(self.jogador.Vy)
                if plat.rect.y >= HEIGHT:   # recolocando as plataformas regulares
                    width = random.randrange(50, 100)
                    p = Notas_regulares(random.randrange(0, WIDTH - width), plat.rect.y - HEIGHT*2, width, 20)
                    while pg.sprite.spritecollide(p, self.platforms_R, False) or \
                            pg.sprite.spritecollide(p, self.platforms_A, False):
                        p = Notas_regulares(random.randrange(0, WIDTH - width), plat.rect.y - HEIGHT*2, width, 20)
                    self.platforms_R.add(p)
                    self.all_sprites.add(p)
                    plat.kill()
                    self.score += 10

            for plat in self.platforms_A:
                plat.rect.y += abs(self.jogador.Vy)
                if plat.rect.y >= HEIGHT:   # recolocando as plataformas aleatorias
                    width = random.randrange(50, 100)
                    p = Notas_aleatorias(random.randrange(0, WIDTH - width),
                                         (random.randrange(-HEIGHT, -20)), width, 20)
                    while pg.sprite.spritecollide(p, self.platforms_A, False) or \
                            pg.sprite.spritecollide(p, self.platforms_R, False):
                        p = Notas_aleatorias(random.randrange(0, WIDTH - width),
                                             (random.randrange(-HEIGHT, -20)), width, 20)
                    self.platforms_A.add(p)
                    self.all_sprites.add(p)
                    plat.kill()
                    self.score += 10

        # Die

        if self.jogador.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.jogador.Vy, 10)

                if sprite.rect.bottom < 0:
                    sprite.kill()

        if len(self.platforms_R) == 0:
            self.rodando = False

    def events(self):
        # Process input (events)
        events = pg.event.get()
        for event in events:
            # checando para sair do jogo
            if event.type == pg.QUIT:
                self.rodando = False
                self.jogo = False
            self.jogador.trata_eventos(event)

    def draw(self):

        # Função para desenvolver imagens

        self.screen.fill(LIGHTBLUE)
        # self.screen.blit(backgrond,(0,0))
        self.all_sprites.draw(self.screen)
        self.draw_textos(str(self.score), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()  # uma desenhada e outra em construção #*after* drawuing everything

    def draw_textos(self, text, size, color, x, y):

        # Função pra desenvolver os textos nas telas

        font = pg.font.Font(self.nome_fonte, size)  # fonte
        texto_surface = font.render(text, True, color)  # onde
        texto_rect = texto_surface.get_rect()  # o que
        texto_rect.midtop = (x, y)  # onde do onde
        self.screen.blit(texto_surface, texto_rect)  # taraw

    def tela_inicial(self):

        self.screen.fill(LIGHTBLUE)
        self.draw_textos("Juppy!", 48, WHITE, WIDTH / 2, HEIGHT / 4)

        # == Instruções
        self.draw_textos("Use as setas para se mover", 22, GREEN, WIDTH / 2, HEIGHT / 2)
        self.draw_textos("Precione espaço para jogar", 22, GREEN, WIDTH / 2, (HEIGHT * 3 / 4))
        self.draw_textos(("High Score :" + str(self.highscore)), 22, WHITE, (WIDTH/2), 15)
        pg.display.flip()
        self.espera_acao()

    def tela_final(self):

        # Função para definir a tela final de gameover#

        if self.rodando:  # se quiser sair não tem que mostrar a tela final
            return
        self.screen.fill(LIGHTBLUE)
        # resultados
        self.draw_textos("GAME OVER", 48, BLACK, WIDTH / 2, HEIGHT / 4)
        self.draw_textos("Score = " + str(self.score), 22, GREEN, WIDTH / 2, HEIGHT / 2)
        self.draw_textos("Precione espaço para jogar novamente", 22, GREEN, WIDTH / 2, (HEIGHT * 3 / 4))
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_textos("NOVO HIGH SCORE!", 22, WHITE, WIDTH/2, (HEIGHT/2 + 40))
            with open(path.join(self.dir, HS_FILE), 'w') as ah:
                ah.write(str(self.score))
        else :
            self.draw_textos("NOVO HIGH SCORE!", 22, WHITE, WIDTH/2, (HEIGHT/2 + 40))
        pg.display.flip()
        self.espera_acao()

    def espera_acao(self):

        # Função para não bagunçar os eventos, e controlar o tempo e espera das telas iniciais e finais

        esperando = True
        while esperando:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    esperando = False
                    self.jogo = False
                    self.rodando = False

                if event.type == pg.KEYUP:
                    if event.key == pg.K_SPACE:
                        esperando = False
                        self.rodando = True


g = Game()  # o jogo de fato
while g.jogo:
    g.tela_inicial()  # gera menu inicial e opcoes
    g.refresh()  # reniciar apenas no novo jogo
    while g.rodando:
        g.run()  # gera a gameplay de fato

    if g.jogo:  # garante que da pra fechar o jogo no meio do run
        g.tela_final()  # tela do game over
    continue
pg.quit()