"""importando bibliotecas necessarias para o jogo"""
import pygame as pg
import random
from os import path  # para criarar meios de se encontrar um arquivo

'''importando variaveis e funções de outros arquivos'''
# "settings" importa as variaveis mais gerais do jogo.
from settings import WIDTH, HEIGHT, FPS, NOME, FONTE, HS_FILE, SPRITESHEET, SPRITESHEET_PLAT, MUSICA, PULO_SND, \
    SUPER_PULO_SND, QUEBRA_SND, GAME_OVER_SND, JOGADOR_ACEL, GRAVIDADE, PULO_JOGADOR, SUPER_PULO, WHITE, BLACK, RED, \
    BLUE, GREEN, YELLOW, ORANGE, BLUEM

# "Plataformas_iniciais" importa as listas de posição das plataformas iniciais de cada tipo de plataforma,
# (elas começam sempre no mesmo lugar).
from Plataformas_iniciais import LISTA_plataformas_iniciais, LISTA_aleatorias_inciais, LISTA_super_pulo_incial, \
    LISTA_quebradicas_inciais

# "spitessheets" importa as funções de importação de sprites para o jogador e plataformas.
from spritessheets import Spritessheets, Spritessheets_plat

# "Classes_Plataformas" importa as classes que criam cada tipo de plataforma e suas funções.
from Classes_Plataformas import Plataformas_regulares, Plataformas_aleatorias, Plataformas_super_pulo, \
    Plataformas_quebradicas

# "Classe_Jogador" importa a clsse que cria o jogador e todas as suas funções.
from Classe_Jogador import Jogador


# ===Classe do jogo
class Game:
    def __init__(self):

        """Inicia o jogo: tela, grupo de sprites, música, looping que mostra que o jogo está rodando, seta clock pro
        jogo coloca tempo e nome """

        # =====Iniciações
        pg.init()

        # ======tela
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))

        self.demonstration_sprites = pg.sprite.Group()

        pg.mixer.init()  # musica
        self.rodando = True  # define o looping do gameplay
        self.jogo = True  # define o looping do programa
        self.nome_fonte = pg.font.match_font(FONTE)

        """carrega os files: de highscore, os de imagens de spritesheet, e de música"""
        # imagens-caminho de diretório
        self.dir = path.dirname(__file__)  # usado para encontrar o folder do arquivo
        img_dir = path.join(self.dir, 'img')

        # carrega o high sore
        with open(path.join(self.dir, HS_FILE), 'w') as ah:  # abre o file para escrevermos o highscore, olhar, ou criar
            try:
                self.highscore = int(ah.read())
            except (FileNotFoundError, IOError):
                self.highscore = 0

        # carrega imagens das sprites
        self.spritesheet = Spritessheets(path.join(img_dir, SPRITESHEET))
        self.spritesheet_p = Spritessheets_plat(path.join(img_dir, SPRITESHEET_PLAT))

        # carrega sons
        self.snd_dir = path.join(self.dir, 'snd')

        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, PULO_SND))
        self.jump_super_sound = pg.mixer.Sound(path.join(self.snd_dir, SUPER_PULO_SND))
        self.jump_quebra_sound = pg.mixer.Sound(path.join(self.snd_dir, QUEBRA_SND))

        self.jogador = Jogador(self.spritesheet)
        self.jumpping = False
        self.walking = False

        self.highscore = 0
        self.score = 0

        pg.display.set_caption(NOME)
        self.clock = pg.time.Clock()  # tempo

    def refresh(self):  # renicia o jogo quando morre, vai rodar um novo jogo // atualizações

        """função responsável por reiniciar e agregar novos fatores no jogo. Reinicia valores e posições do jogador, 
            adiniciona cada grupo de plataformas e cada uma nas lista nos grupos de sprites, puxa o run"""

        self.score = 0

        self.all_sprites = pg.sprite.Group()

        # === Grupo de spreites plataformas
        self.platforms_R = pg.sprite.Group()  # grupo para as plataformas regulares
        self.platforms_A = pg.sprite.Group()  # grupo para as plataformas aleatorias
        self.platforms_P = pg.sprite.Group()  # grupo para as plataformas super pulo
        self.platforms_Q = pg.sprite.Group()  # grupo para as plataformas quebradicas

        # ==== Grupo de sprits (personagens)
        self.all_sprites.add(self.jogador)
        self.jogador.rect.x = WIDTH / 2  # devolve o jogador para a posicao original
        self.jogador.rect.y = HEIGHT / 2
        self.jogador.Vy = 0  # devolve jogador para a velocidade original
        self.jogador.Vx = 0  # devolve jogador para a velocidade original

        # === Pega as plataformas nos grupos inicias e adiciona cada uma nos grupos de sprites

        for plat in LISTA_plataformas_iniciais:
            p = Plataformas_regulares(self.spritesheet_p, *plat)  # explora todas a lista de forma quebrada
            self.all_sprites.add(p)
            self.platforms_R.add(p)

        for plat in LISTA_aleatorias_inciais:
            p = Plataformas_aleatorias(self.spritesheet_p, *plat)  # explora todas a lista de forma quebrada
            self.all_sprites.add(p)
            self.platforms_A.add(p)

        for plat in LISTA_super_pulo_incial:
            p = Plataformas_super_pulo(self.spritesheet_p, *plat)  # explora todas a lista de forma quebrada
            self.all_sprites.add(p)
            self.platforms_P.add(p)

        for plat in LISTA_quebradicas_inciais:
            p = Plataformas_quebradicas(self.spritesheet_p, *plat)  # explora todas a lista de forma quebrada
            self.all_sprites.add(p)
            self.platforms_Q.add(p)

        self.run()

    def run(self):

        """Roda todas as funcionalidades do loop do game, chamanddo todas as funções base"""

        # game Loop
        self.clock.tick(FPS)
        # ==== Chamando events e as tres funções básicas do game loop que se conversam
        self.events()  # recebe comandos do taclado e mouse (controle do jogador)
        self.updates()
        self.draw()
        # pg.mixer.music.fadeout(500)

    def updates(self):

        """ Faz os updates(como o própro nome diz). Primeiramente é a respossável por verificar as colisões entre o
        jogador e plataformas (as dos 4 grupos), e além de verificar ajusta a posição e velocidade do jogador pós
        colisão. vai movendo as plataformas pra baixo até o final na dela e depois as destroi, e conforme vão
        desaparecendo novas são geradas """

        # faz updates
        self.all_sprites.update()

        # __________________________________________________________________________________________________________________________________________________
        # checando colisões
        hits = pg.sprite.spritecollide(self.jogador, self.platforms_R, False)  # contato com as plataformas regulares
        hits2 = pg.sprite.spritecollide(self.jogador, self.platforms_A, False)  # contato com as plataformas aleatorias
        hits3 = pg.sprite.spritecollide(self.jogador, self.platforms_P, False)  # contato com as plataformas super pulo
        hits4 = pg.sprite.spritecollide(self.jogador, self.platforms_Q, False)  # contato com as plataformas quebradicas

        if hits:  # verifica impacto entre jogador e as plataformas regulares para realizar o pulo

            if (self.jogador.Vy > 0) and (self.jogador.rect.bottom > hits[0].rect.top) and (
                    self.jogador.maior_altura < hits[0].rect.top):
                self.jogador.rect.bottom = hits[0].rect.top  # ajusta a posição do jogador
                self.jogador.image = self.jogador.front[0]  # seleciona a anição que vai ser mostrada
                self.jumpping = False  # diz que ta apenas de frente assim que faz o contato
                self.walking = False
                self.jogador.Vy = -PULO_JOGADOR  # ajusta para o pulo assim que tocou

                self.jump_sound.play()  # toca o som do contato

        if hits2:  # verifica impacto entre jogador e as plataformas aleatorias para realizar o pulo

            if (self.jogador.Vy > 0) and (self.jogador.rect.bottom > hits2[0].rect.top) and (
                    self.jogador.maior_altura < hits2[0].rect.top):
                self.jogador.rect.bottom = hits2[0].rect.top
                self.jumpping = False
                self.walking = False
                self.jogador.Vy = -PULO_JOGADOR

                self.jump_sound.play()

        if hits3:  # verifica impacto entre jogador e a plataforma super_pulo para realizar o super pulo

            if (self.jogador.Vy > 0) and (self.jogador.rect.bottom > hits3[0].rect.top) and (
                    self.jogador.maior_altura < hits3[0].rect.top):
                self.jogador.rect.bottom = hits3[0].rect.top
                self.jumpping = False
                self.walking = False
                self.jogador.Vy = -SUPER_PULO

                self.jump_super_sound.play()

        if hits4:  # verifica impacto entre jogador e as plataformas quebradicas para realizar o pulo

            if (self.jogador.Vy > 0) and (self.jogador.rect.bottom > hits4[0].rect.top) and (
                    self.jogador.maior_altura < hits4[0].rect.top):
                hits4 = pg.sprite.spritecollide(self.jogador, self.platforms_Q,
                                                True)  # destroi quebradica se vier de cima
                self.jogador.rect.bottom = hits4[0].rect.top
                self.jumpping = False
                self.walking = False
                self.jogador.Vy = -PULO_JOGADOR

                self.jump_quebra_sound.play()

        '''faz a tela subir conforme o jogador avança. Na verdade, todas plataformas estão descendo, e nao o jogador 
        que está subindo. '''

        if self.jogador.rect.top <= HEIGHT / 4:  # Fazer a tela rodar quando o jogador chegar a 1/4 da tela
            self.jogador.rect.y += max(abs(self.jogador.Vy), 2)
            # __________________________________________________________________________________________________________________________________________________
            for plat in self.platforms_R:  # recolocando as plataformas regulares
                plat.rect.y += max(abs(self.jogador.Vy), 2)  # para ter um valor coerente

                if plat.rect.y >= HEIGHT:
                    width = random.randrange(50, 100)
                    p = Plataformas_regulares(self.spritesheet_p, (random.randrange(0, WIDTH - width)),
                                              (plat.rect.y - HEIGHT * 2))  # sorteando posição das plataformas

                    while pg.sprite.spritecollide(p, self.platforms_R, False) or \
                            pg.sprite.spritecollide(p, self.platforms_A, False) or \
                            pg.sprite.spritecollide(p, self.platforms_P, False) or \
                            pg.sprite.spritecollide(p, self.platforms_Q, False):
                        p = Plataformas_regulares(self.spritesheet_p, (random.randrange(0, WIDTH - width)),
                                                  (plat.rect.y - HEIGHT * 2))

                    self.platforms_R.add(p)  # addicionando as novas plataformas aos grupos
                    self.all_sprites.add(p)
                    plat.kill()
                    self.score += 5  # matou, ganhou plataforma
            # __________________________________________________________________________________________________________________________________________________
            for plat in self.platforms_A:  # recolocando as plataformas aleatorias
                plat.rect.y += max(abs(self.jogador.Vy), 2)

                if plat.rect.y >= HEIGHT:
                    width = random.randrange(50, 100)
                    p = Plataformas_aleatorias(self.spritesheet_p, (random.randrange(0, WIDTH - width)),
                                               (random.randrange(-HEIGHT, -20)))

                    while pg.sprite.spritecollide(p, self.platforms_A, False) or \
                            pg.sprite.spritecollide(p, self.platforms_R, False) or \
                            pg.sprite.spritecollide(p, self.platforms_P, False) or \
                            pg.sprite.spritecollide(p, self.platforms_Q, False):
                        p = Plataformas_aleatorias(self.spritesheet_p, (random.randrange(0, WIDTH - width)),
                                                   (random.randrange(-HEIGHT, -20)))

                    self.platforms_A.add(p)
                    self.all_sprites.add(p)
                    plat.kill()
                    self.score += 5

            for plat in self.platforms_P:  # recolocando a plataforma super pulo
                plat.rect.y += max(abs(self.jogador.Vy), 2)

                if plat.rect.y >= HEIGHT:
                    width = random.randrange(50, 100)
                    p = Plataformas_super_pulo(self.spritesheet_p, (random.randrange(0, WIDTH - width)),
                                               (random.randrange(-2 * HEIGHT, -200)))

                    while pg.sprite.spritecollide(p, self.platforms_A, False) or \
                            pg.sprite.spritecollide(p, self.platforms_R, False) or \
                            pg.sprite.spritecollide(p, self.platforms_P, False) or \
                            pg.sprite.spritecollide(p, self.platforms_Q, False):
                        p = Plataformas_super_pulo(self.spritesheet_p, (random.randrange(0, WIDTH - width)),
                                                   (random.randrange(-2 * HEIGHT, -200)))

                    self.platforms_P.add(p)
                    self.all_sprites.add(p)
                    plat.kill()
                    self.score += 5

            for plat in self.platforms_Q:  # recolocando as plataformas quebradicas
                plat.rect.y += max(abs(self.jogador.Vy), 2)

                if plat.rect.y >= HEIGHT:  # cria mais se sairem fora da tela
                    width = random.randrange(50, 100)
                    p = Plataformas_quebradicas(self.spritesheet_p, (random.randrange(0, WIDTH - width)),
                                                (random.randrange(-HEIGHT, -200)))

                    while pg.sprite.spritecollide(p, self.platforms_A, False) or \
                            pg.sprite.spritecollide(p, self.platforms_R, False) or \
                            pg.sprite.spritecollide(p, self.platforms_P, False) or \
                            pg.sprite.spritecollide(p, self.platforms_Q, False):
                        p = Plataformas_quebradicas(self.spritesheet_p, (random.randrange(0, WIDTH - width)),
                                                    (random.randrange(-HEIGHT, -200)))

                    self.platforms_Q.add(p)
                    self.all_sprites.add(p)
                    plat.kill()
                    self.score += 5

                if len(self.platforms_Q) < 2:  # cria mais quebradicas se as outras forem destruidas
                    width = random.randrange(50, 100)
                    p = Plataformas_quebradicas(self.spritesheet_p, (random.randrange(0, WIDTH - width)),
                                                (random.randrange(-HEIGHT, -200)))

                    while pg.sprite.spritecollide(p, self.platforms_A, False) or \
                            pg.sprite.spritecollide(p, self.platforms_R, False) or \
                            pg.sprite.spritecollide(p, self.platforms_P, False) or \
                            pg.sprite.spritecollide(p, self.platforms_Q, False):
                        p = Plataformas_quebradicas(self.spritesheet_p, (random.randrange(0, WIDTH - width)),
                                                    (random.randrange(-HEIGHT, -200)))

                    self.platforms_Q.add(p)
                    self.all_sprites.add(p)
                    self.score += 5

        # Die

        if self.jogador.rect.bottom > HEIGHT:
            pg.mixer.music.fadeout(500)
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.jogador.Vy, 10)

                if sprite.rect.bottom < 0:
                    sprite.kill()

        if len(self.platforms_R) == 0:
            self.platforms_R.empty()
            self.platforms_A.empty()
            self.platforms_P.empty()
            self.platforms_Q.empty()
            self.rodando = False

    def events(self):

        """Trata ações que o usuário tomou durante o jogo e as coletas para devolver ações. Verifica se o jogador
        deseja desligar """
        # Process input (events)

        events = pg.event.get()
        for event in events:

            # checando para sair do jogo
            if event.type == pg.QUIT:
                self.rodando = False
                self.jogo = False
            self.jogador.trata_eventos(event)

    def draw(self):

        """Função pata desenvolver as sprites que estão no grupo e os textos que aparecerão"""

        # Função para desenvolver imagens

        backgrond = pg.image.load(
            path.join(path.join(self.dir, 'img'), "background.png")).convert()  # pega imagem do fundo
        backgrond_rect = backgrond.get_rect()  # defini o retangulo da imagem
        self.screen.blit(backgrond, backgrond_rect)  # coloca o backgound

        self.all_sprites.draw(self.screen)  # sprites
        self.screen.blit(self.jogador.image, self.jogador.rect)

        self.draw_textos(str(self.score), 22, WHITE, WIDTH / 2, 15)  # textos

        pg.display.flip()  # uma desenhada e outra em construção #*after* drawuing everything

    def draw_textos(self, text, size, color, x, y):

        """Defini textos que aparecerão. Fonte, tamanho e imagem. Desenha eles  """

        # Função pra desenvolver os textos nas telas

        font = pg.font.Font(self.nome_fonte, size)  # fonte
        texto_surface = font.render(text, True, color)  # onde
        texto_rect = texto_surface.get_rect()  # o que
        texto_rect.midtop = (x, y)  # onde do onde
        self.screen.blit(texto_surface, texto_rect)  # taraw!!

    def tela_inicial(self):

        """Carrega as tela inicial que contém o nome e scores e fica até a ação da pessoa"""

        self.screen.fill(BLUEM)

        # pg.mixer.music.load(path.join(self.snd_dir,GAME_OVER_SND ))
        # pg.mixer.music.play(loops = -1)

        self.draw_textos(NOME, 80, WHITE, WIDTH / 2, HEIGHT / 4)  # chama os textos

        # Instruções
        self.draw_textos("Precione espaço para instruções", 30, GREEN, WIDTH / 2, (HEIGHT * 3 / 4))
        self.draw_textos(("High Score :" + str(self.highscore)), 22, WHITE, (WIDTH / 2), 15)

        pg.display.flip()
        self.espera_acao()

    def tela_instrucoes(self):

        """Carrega uma tela de instruções. Com isso tem textos de instruções e as imagens de plataformas a serem
        carregadas espera ação do usuário """

        self.screen.fill(BLUEM)

        # desenha as setinhas
        self.draw_textos("Use as setas para se mover", 22, WHITE, 350, 80)
        self.draw_textos("<=   =>", 60, GREEN, 140, 60)

        # desenha e escreve sobre a plataforma normal
        self.draw_textos("Pule nas plataformas para subir", 22, WHITE, 350, 180)
        self.demonstration_sprites.add(Plataformas_regulares(self.spritesheet_p, 80, 180))

        # desenha e escreve sobre a plataforma quebradiça
        self.draw_textos("Plataformas de madeira", 22, WHITE, 350, 280)
        self.draw_textos("só podem ser usadas uma vez", 22, WHITE, 350, 300)
        self.demonstration_sprites.add(Plataformas_quebradicas(self.spritesheet_p, 100, 290))

        # desenha e escreve sobre a plataforma de super pulo
        self.draw_textos("Plataformas vermelhas te", 22, WHITE, 350, 380)
        self.draw_textos("fazem realizar um super pulo", 22, WHITE, 350, 400)
        self.demonstration_sprites.add(Plataformas_super_pulo(self.spritesheet_p, 100, 390))

        self.draw_textos("Precione espaço para começar", 30, GREEN, WIDTH / 2, (HEIGHT * 5 / 6))  # instrução

        self.demonstration_sprites.draw(self.screen)  # sprites
        pg.display.flip()
        self.espera_acao()

    def tela_final(self):

        """tela final de game over, traz textos de resultados (score + highscore): edita o arquivo de score caso o
        score seja mais alto que o highscore antigo e imagem do personagem triste """

        # Função para definir a tela final de gameover

        if self.rodando:  # se quiser sair não tem que mostrar a tela final
            return

        # ==Músicas de final
        pg.mixer.music.load(path.join(self.snd_dir, GAME_OVER_SND))
        pg.mixer.music.play(loops=-1)

        self.screen.fill(BLUEM)

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

        """Função que controla quando o jogador clica algo pra sair das telas auxílares"""

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


# ---------------------------------------------------------------------------------------------------------------------

"""Loop do jogo que controla por partes e quando mudar telas ou quando está de fato rodando o loop principal"""

g = Game()  # o jogo de fato
while g.jogo:
    g.tela_inicial()  # gera menu inicial e high score

    if g.jogo:  # garante que da pra fechar o jogo no menu inicial
        g.tela_instrucoes()  # gera menu de instruções
        g.refresh()  # reniciar apenas no novo jogo

    pg.mixer.music.load(path.join(g.snd_dir, MUSICA))  # música de fundo principal
    pg.mixer.music.play(loops=-1)
    while g.rodando:
        g.run()  # gera a gameplay de fato

    if g.jogo:  # garante que da pra fechar o jogo no meio do run
        g.tela_final()  # tela do game over
        pg.mixer.music.fadeout(500)
    continue
pg.quit()
