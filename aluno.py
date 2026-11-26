from pathlib import Path

import pygame


GRAVIDADE = 2200
VELOCIDADE = 340
FORCA_PULO = 1000
VELOCIDADE_MAX_QUEDA = 1400


class Aluno:
    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.largura = 36
        self.altura = 64

        self.velocidade_x = 0
        self.velocidade_y = 0
        self.no_chao = False

        caminho_sprite = (
            Path(__file__).resolve().parent
            / "assets" / "sprites" / "aluno" / "parado.png"
        )
        imagem = pygame.image.load(str(caminho_sprite)).convert_alpha()
        # Remove a margem transparente antes de ajustar o tamanho.
        imagem = imagem.subsurface(imagem.get_bounding_rect()).copy()
        largura_sprite = round(imagem.get_width() * self.altura / imagem.get_height())
        self.imagem_direita = pygame.transform.smoothscale(
            imagem, (largura_sprite, self.altura)
        )
        self.imagem_esquerda = pygame.transform.flip(self.imagem_direita, True, False)
        self.olhando_direita = True

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.largura / 2),
            int(self.y - self.altura),
            self.largura,
            self.altura
        )


    def mover(self):
        teclas = pygame.key.get_pressed()

        self.velocidade_x = 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.velocidade_x -= VELOCIDADE
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.velocidade_x += VELOCIDADE

        if self.velocidade_x > 0:
            self.olhando_direita = True
        elif self.velocidade_x < 0:
            self.olhando_direita = False


    def pular(self):
        if self.no_chao:
            self.velocidade_y = -FORCA_PULO
            self.no_chao = False


    def aplicar_gravidade(self, dt):
        self.velocidade_y += GRAVIDADE * dt
        if self.velocidade_y > VELOCIDADE_MAX_QUEDA:
            self.velocidade_y = VELOCIDADE_MAX_QUEDA


    def checar_colisao(self, y_antes, superficies):
        self.no_chao = False


        if self.velocidade_y < 0:
            return

        esquerda = self.x - self.largura / 2
        direita = self.x + self.largura / 2

        for superficie in superficies:
            em_cima = direita > superficie.left and esquerda < superficie.right
            passou_do_topo = y_antes <= superficie.top <= self.y

            if em_cima and passou_do_topo:
                self.y = superficie.top
                self.velocidade_y = 0
                self.no_chao = True
                return


    def limitar_bordas(self, largura_mundo):
        metade = self.largura / 2
        if self.x < metade:
            self.x = metade
        if self.x > largura_mundo - metade:
            self.x = largura_mundo - metade

    def update(self, dt, superficies, largura_mundo):
        self.mover()
        self.aplicar_gravidade(dt)

        y_antes = self.y
        self.x += self.velocidade_x * dt
        self.y += self.velocidade_y * dt

        self.checar_colisao(y_antes, superficies)
        self.limitar_bordas(largura_mundo)


    def draw(self, tela, camerax):
        imagem = self.imagem_direita if self.olhando_direita else self.imagem_esquerda
        rect = imagem.get_rect(
            midbottom=(round(self.x - camerax), round(self.y))
        )
        tela.blit(imagem, rect)
