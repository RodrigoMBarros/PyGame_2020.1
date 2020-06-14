import pygame as pg

class Plataformas_regulares(pg.sprite.Sprite):
    """Defini as plataformas que serão geradas de forma regular com o passar do jogo e a necessidade de novas
    plataformas """

    def __init__(self, spritesheet_p, x, y):
        pg.sprite.Sprite.__init__(self)

        self.image = spritesheet_p.get_image_plat(144, 648, 70, 70)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Plataformas_aleatorias(pg.sprite.Sprite):
    """Defini as plataformas que serão geradas de forma aleatórias em quantidade ao passar do jogo"""

    def __init__(self, spritesheet_p, x, y):
        pg.sprite.Sprite.__init__(self)

        self.image = spritesheet_p.get_image_plat2(144, 648, 70, 70)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Plataformas_super_pulo(pg.sprite.Sprite):
    """Plataformas geradas em um intervalo maior, e que quando tocadas irão gerar pulos maiores"""

    def __init__(self, spritesheet_p, x, y):
        pg.sprite.Sprite.__init__(self)

        self.image = spritesheet_p.get_image_plat2(504, 0, 70, 70)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Plataformas_quebradicas(pg.sprite.Sprite):
    """Plataformas também geradas de forma aleatória em quantidade e menos, desaparecem quando tocadas pelo jogador"""

    def __init__(self, spritesheet_p, x, y):
        pg.sprite.Sprite.__init__(self)

        self.image = spritesheet_p.get_image_plat2(0, 792, 70, 70)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
