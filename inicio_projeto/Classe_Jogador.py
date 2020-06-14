import pygame as pg
from settings import WIDTH, HEIGHT, GRAVIDADE, JOGADOR_ACEL


class Jogador(pg.sprite.Sprite):
    """Classe do jogador"""

    def __init__(self, spritesheet):

        """Inicia suas imagens, modos de animação, e defini variáveis como velocidade, tamanhos e gravidade """
        pg.sprite.Sprite.__init__(self)
        self.spritesheet = spritesheet

        # controlando frames
        self.walking = False
        self.jumpping = False
        self.current_frame = 0
        self.last_update = 0

        """Pega as imagens da spritesheet com as cordenadas de posição (x, y) e também o tamanho de recorte (largura, 
        altura). Cada sequência de imagem seria uma determinada animação """

        # ____pulo
        self.jump = [self.spritesheet.get_image(438, 93, 67, 94), self.spritesheet.get_image(219, 0, 72, 97)]

        # ____frente/parado
        self.front = [self.spritesheet.get_image(0, 196, 66, 92),
                      self.spritesheet.get_image(67, 196, 66, 92)]

        # ____andando
        self.walk_r = [self.spritesheet.get_image(0, 98, 72, 97),
                       self.spritesheet.get_image(73, 98, 72, 97)]

        self.walk_l = []
        for frame in self.walk_r:
            self.walk_l.append(pg.transform.flip(frame, True, False))  # vira horizontalmente mas não verticalmente

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

    def update(self):

        """responsável por fazer o update dos movimentos de animação do jogador. Definir limites de tela e movimento
        por ela. Controle da altura máxima do jogador para o controle de toques. e também updates e controles de como
        o boneco se comporta com as equações de movimento """

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

        """Recebe os eventos registrados no loop principal do jogo, e assim analisa quais movimentos são possíveis
        para o jogador garantindo o movimento horixontal """

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

        """Trabalha com um relógio de funcionamento, e assim controla a partir de ifs, o movimento do jogador nas
        animações sendo verticalmente, as pernas nas andadas ou entao parado """

        agora = pg.time.get_ticks()

        # __ ajustando andada
        if self.Vx != 0:
            self.walking = True
        else:
            self.walking = False

        if self.walking:
            if agora - self.last_update > 200:  # checa se está na hora de mudar os frames
                self.last_update = agora  # se estiver o tempo do último update de imagem se tona o momento
                self.current_frame = (self.current_frame + 1) % len(self.walk_r)  # pra trocar a frame

        if self.Vx > 0:
            self.image = self.walk_r[self.current_frame]
        elif self.Vx < 0:
            self.image = self.walk_l[self.current_frame]

        # __ ajustando o pulo

        if self.Vy != 0:
            self.jumpping = True

        if self.jumpping:
            if agora - self.last_update > 200:  # checa se está na hora de mudar os frames
                if self.Vy < 0:
                    self.last_update = agora
                    self.image = self.jump[0]
                elif self.Vy > 0:
                    self.last_update = agora
                    self.image = self.jump[1]

        # __ ajustando posição de frente

        if not self.jumpping and not self.walking:
            self.image = self.front[0]  # troca a imagem para o frame correto
            if agora - self.last_update > 450:  # checa se está na hora de mudar os frames
                self.last_update = agora  # se estiver o tempo do último update de imagem se tona o momento
                self.current_frame = (self.current_frame + 1) % len(self.front)  # pra trocar a frame
