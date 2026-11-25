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

        self.cor = (45, 98, 180)

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
        rect = self.get_rect().move(-camerax, 0)


        pygame.draw.rect(tela, self.cor, (rect.x, rect.y + 20, rect.width, rect.height - 20), border_radius=6)


        pygame.draw.circle(tela, (241, 194, 150), (rect.centerx, rect.y + 11), 11)