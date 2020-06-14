import pygame as pg


# Player sprites
class Spritessheets:
    """ Classe responsável por carregar a spritesheet do jogador(bonequinho),
        nela já é ajustado os tamanhos e cor de fundo"""

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


# platform sprites
class Spritessheets_plat:
    """Classe responsável por carregar e chamar as imagens contidas na spritesheet dos titles,
        ou seja, as plataformas, aqui também são ajustados tamanhos"""

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
