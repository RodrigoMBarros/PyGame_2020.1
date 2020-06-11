import pygame as pg
import random
from os import path  # para criarar meios de se encontrar um arquivo

WIDTH = 500
HEIGHT = 600
FPS = 30
NOME = "Space Jump!"
FONTE = 'arial'
HS_FILE = "highscore.txt"
SPRITESHEET = "p1_spritesheet.png"
SPRITESHEET_PLAT = "tiles_spritesheet.png"
# NAVE_LAYER = 0
# == Player properies
JOGADOR_ACEL = 8
GRAVIDADE = 1
PULO_JOGADOR = 22

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

# === Formatando plataformas

LISTA_plataformas_iniciais = [(0, HEIGHT - 60),
                              (200, 440),
                              (125, 320),
                              (350, 200),
                              (175, 80),
                              (100, -30),
                              (300, -140),
                              (400, -250),
                              (350, -360),
                              (175, -470)]

LISTA_aleatorias_inciais = [(60, 180),
                            (375, 40),
                            (400, 350),
                            (30, -250),
                            (370, -450)]


# ==== Classes

# Player sprites #
class Spritessheets:
    # carregando e lendo as sprites na imagem geral
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height):
        # pega uma imagem do spritesheet
        image = pg.Surface((width, height), pg.SRCALPHA)
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))

        # defininndo tamanho
        largura = int(width / 1.4)
        altura = int(height / 1.4)
        image = pg.transform.scale(image, (largura, altura))

        return image


class Spritessheets_plat:
    # carregando e lendo as sprites na imagem geral
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert_alpha()

    def get_image_plat(self, x, y, width, height):
        # pega uma imagem do spritesheet
        image = pg.Surface((width, height), pg.SRCALPHA)
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))

        # defininndo tamanho
        largura = int(width / 0.65)
        altura = int(height // 2)
        image = pg.transform.scale(image, (largura, altura))

        return image

    def get_image_plat2(self, x, y, width, height):
        # pega uma imagem do spritesheet
        image = pg.Surface((width, height), pg.SRCALPHA)
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))

        # defininndo tamanho
        largura = int(width)
        altura = int(height // 2)
        image = pg.transform.scale(image, (largura, altura))

        return image


# jogador#
class Jogador(pg.sprite.Sprite):
    def __init__(self, spritesheet):
        pg.sprite.Sprite.__init__(self)
        self.spritesheet = spritesheet

        # controlando frames
        self.walking = False
        self.jumpping = False
        self.current_frame = 0
        self.last_update = 0

        self.carrega_imagens()

        # pegando a imagem
        self.image = self.front[0]
        self.rect = self.image.get_rect()  # gera a posição e tamanho da imagem
        self.maior_altura = self.rect.bottom

        # quantos pixels mexer/velocidade
        self.rect.x = WIDTH / 2
        self.rect.y = HEIGHT / 2  # gera posições x e y pro jogador
        self.Vy = 0
        self.Vx = 0
        self.grav = GRAVIDADE

    def carrega_imagens(self):

        # ____pulo
        self.jump = [self.spritesheet.get_image(438, 93, 67, 94), self.spritesheet.get_image(219, 0, 72,
                                                                                             97)]  # pver se queremos essa ou a outras + se vira para direita ou não

        # ____frente/parado
        self.front = [self.spritesheet.get_image(0, 196, 66, 92),
                      self.spritesheet.get_image(67, 196, 66, 92)]

        # ____andando
        self.walk_r = [self.spritesheet.get_image(0, 98, 72, 97),
                       self.spritesheet.get_image(73, 98, 72, 97)]

        self.walk_l = []
        for frame in self.walk_r:
            self.walk_l.append(pg.transform.flip(frame, True, False))  # vira horizontalmente mas não verticalmente

    def update(self):

        self.animacao()
        # pulo
        self.Vy += self.grav
        # equações do movimento

        self.rect.y += self.Vy
        self.rect.x += self.Vx

        # Se subindo, atualiza a maior altura atingida
        if self.Vy < 0:
            self.maior_altura = self.rect.bottom

        # atravessando a tela de um lado pro outro
        if self.rect.right > WIDTH + self.rect.width / 2:
            self.rect.left = 0 - self.rect.width / 2
        if self.rect.left < 0 - self.rect.width / 2:
            self.rect.right = WIDTH + self.rect.width / 2

    def trata_eventos(self, event):  # Eventos para o jogador

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                self.Vx = -JOGADOR_ACEL
            if event.key == pg.K_RIGHT:
                self.Vx = JOGADOR_ACEL

        elif event.type == pg.KEYUP:
            if event.key == pg.K_LEFT and self.Vx < 0:  # garante que ele nao trave quando muda de direção
                self.Vx = 0
            if event.key == pg.K_RIGHT and self.Vx > 0:  # garante que ele nao trave quando muda de direção
                self.Vx = 0

    def animacao(self):
        agora = pg.time.get_ticks()

        # __ ajustando andada
        if self.Vx != 0:
            self.walking = True
        else:
            self.walking = False

        if self.walking:
            if agora - self.last_update > 200:
                self.last_update = agora
                self.current_frame = (self.current_frame + 1) % len(self.walk_r)

        if self.Vx > 0:
            self.image = self.walk_r[self.current_frame]
        elif self.Vx < 0:
            self.image = self.walk_l[self.current_frame]

        if self.Vy != 0:
            self.jumpping = True

        if self.jumpping:
            if agora - self.last_update > 200:
                if self.Vy < 0:
                    self.last_update = agora
                    self.image = self.jump[0]
                elif self.Vy > 0:
                    self.last_update = agora
                    self.image = self.jump[1]

        if not self.jumpping and not self.walking:
            print("chegou aqui")
            self.image = self.front[0]  # troca a imagem para o frame correto
            if agora - self.last_update > 450:  # checa se está na hora de mudar os frames
                self.last_update = agora  # se estiver o tempo do último update de imagem se tona o momento
                self.current_frame = (self.current_frame + 1) % len(self.front)  # pra trocar a frame

    # Plataformas


class Plataformas_regulares(pg.sprite.Sprite):
    def __init__(self, spritesheet_p, x, y):
        pg.sprite.Sprite.__init__(self)
        self.spritesheet_p = spritesheet_p

        self.image = self.spritesheet_p.get_image_plat(144, 648, 70, 70)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Plataformas_aleatorias(pg.sprite.Sprite):
    def __init__(self, spritesheet_p, x, y):
        pg.sprite.Sprite.__init__(self)

        self.image = spritesheet_p.get_image_plat2(144, 648, 70, 70)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# ===Classe do jogo
class Game:
    def __init__(self):

        # =====Iniciações
        pg.init()

        # ======tela
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))

        self.all_sprites = pg.sprite.Group()

        pg.mixer.init()  # musica
        self.rodando = True  # define o looping do gameplay
        self.jogo = True  # define o looping do programa
        self.nome_fonte = pg.font.match_font(FONTE)
        self.load_data()

        self.jogador = Jogador(self.spritesheet)

        pg.display.set_caption(NOME)
        self.clock = pg.time.Clock()  # tempo

    def load_data(self):
        # carrega o high sore
        self.dir = path.dirname(__file__)  # usado para encontrar o folder do arquivo
        img_dir = path.join(self.dir, 'img')

        with open(path.join(self.dir, HS_FILE), 'w') as ah:  # abre o file para escrevermos, olhar, ou criar
            try:
                self.highscore = int(ah.read())
            except:
                self.highscore = 0

        # carrega imagens das sprites
        self.spritesheet = Spritessheets(path.join(img_dir, SPRITESHEET))
        self.spritesheet_p = Spritessheets_plat(path.join(img_dir, SPRITESHEET_PLAT))

    def refresh(self):  # renicia o jogo quando morre, vai rodar um novo jogo // atualizações
        self.score = 0

        # ==== Grupo de sprits (personagens)
        self.all_sprites.add(self.jogador)
        self.jogador.rect.x = WIDTH / 2  # devolve o jogador para a posicao original
        self.jogador.rect.y = HEIGHT / 2
        self.jogador.Vy = 0  # devolve jogador para a velocidade original
        self.jogador.Vx = 0  # devolve jogador para a velocidade original

        # === Grupo de spreites plataformas
        self.platforms_R = pg.sprite.Group()  # grupo para as plataformas regulares
        self.platforms_A = pg.sprite.Group()  # grupo para as plataformas aleatorias

        for plat in LISTA_plataformas_iniciais:
            p = Plataformas_regulares(self.spritesheet_p, *plat)  # explora todas a lista de forma quebrada
            self.all_sprites.add(p)
            self.platforms_R.add(p)

        for plat in LISTA_aleatorias_inciais:
            p = Plataformas_aleatorias(self.spritesheet_p, *plat)  # explora todas a lista de forma quebrada
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

        # __________________________________________________________________________________________________________________________________________________
        # checando colisões
        hits = pg.sprite.spritecollide(self.jogador, self.platforms_R, False)  # contato com as plataformas regulares
        hits2 = pg.sprite.spritecollide(self.jogador, self.platforms_A, False)  # contato com as plataformas aleatorias

        if hits:  # verifica impacto entre jogador e as plataformas regulares para realizar o pulo

            if (self.jogador.Vy > 0) and (self.jogador.rect.bottom > hits[0].rect.top) and (
                    self.jogador.maior_altura < hits[0].rect.top):
                self.jogador.rect.bottom = hits[0].rect.top
                self.jogador.image = self.jogador.front[0]
                self.jumpping = False
                self.walking = False

                self.jogador.Vy = -PULO_JOGADOR

        if hits2:  # verifica impacto entre jogador e as plataformas aleatorias para realizar o pulo

            if (self.jogador.Vy > 0) and (self.jogador.rect.bottom > hits2[0].rect.top) and (
                    self.jogador.maior_altura < hits2[0].rect.top):
                self.jogador.rect.bottom = hits2[0].rect.top
                self.jumpping = False
                self.walking = False
                self.jogador.Vy = -PULO_JOGADOR

        # ___Fazer a tela rodar quando o jogador chegar a 1/4 da tela___
        if self.jogador.rect.top <= HEIGHT / 4:
            self.jogador.rect.y += max(abs(self.jogador.Vy), 2)
            # __________________________________________________________________________________________________________________________________________________
            for plat in self.platforms_R:
                plat.rect.y += max(abs(self.jogador.Vy), 2)  # para ter um valor coerente

                if plat.rect.y >= HEIGHT:  # recolocando as plataformas regulares
                    width = random.randrange(50, 100)
                    p = Plataformas_regulares(self.spritesheet_p, (random.randrange(0, WIDTH - width)),
                                              (plat.rect.y - HEIGHT * 2))  # sorteando posição das plataformas

                    while pg.sprite.spritecollide(p, self.platforms_R, False) or \
                            pg.sprite.spritecollide(p, self.platforms_A, False):
                        p = Plataformas_regulares(self.spritesheet_p, (random.randrange(0, WIDTH - width)),
                                                  (plat.rect.y - HEIGHT * 2))

                    self.platforms_R.add(p)  # addicionando as novas plataformas aos grupos
                    self.all_sprites.add(p)
                    plat.kill()
                    self.score += 5  # matou, ganhou plataforma
            # __________________________________________________________________________________________________________________________________________________
            for plat in self.platforms_A:
                plat.rect.y += max(abs(self.jogador.Vy), 2)

                if plat.rect.y >= HEIGHT:  # recolocando as plataformas aleatorias
                    width = random.randrange(50, 100)
                    p = Plataformas_aleatorias(self.spritesheet_p, (random.randrange(0, WIDTH - width)),
                                               (random.randrange(-HEIGHT, -20)))

                    while pg.sprite.spritecollide(p, self.platforms_A, False) or \
                            pg.sprite.spritecollide(p, self.platforms_R, False):
                        p = Plataformas_aleatorias(self.spritesheet_p, (random.randrange(0, WIDTH - width)),
                                                   (random.randrange(-HEIGHT, -20)))

                    self.platforms_A.add(p)
                    self.all_sprites.add(p)
                    plat.kill()
                    self.score += 5

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

        backgrond = pg.image.load(
            path.join(path.join(self.dir, 'img'), "background.png")).convert()  # pega imagem do fundo
        backgrond_rect = backgrond.get_rect()
        self.screen.blit(backgrond, backgrond_rect)  # coloca o backgound
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.jogador.image, self.jogador.rect)
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
        self.draw_textos(NOME, 48, WHITE, WIDTH / 2, HEIGHT / 4)

        # == Instruções
        self.draw_textos("Use as setas para se mover", 22, GREEN, WIDTH / 2, HEIGHT / 2)
        self.draw_textos("Precione espaço para jogar", 22, GREEN, WIDTH / 2, (HEIGHT * 3 / 4))
        self.draw_textos(("High Score :" + str(self.highscore)), 22, WHITE, (WIDTH / 2), 15)
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
            self.draw_textos("NOVO HIGH SCORE!", 22, WHITE, WIDTH / 2, (HEIGHT / 2 + 40))
            with open(path.join(self.dir, HS_FILE), 'w') as ah:
                ah.write(str(self.score))
        else:
            self.draw_textos("HIGH SCORE: " + str(self.highscore), 22, WHITE, WIDTH / 2, (HEIGHT / 2 + 40))
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
