from pathlib import Path

import pygame

PASTA_ANOTACOES = Path(__file__).resolve().parent / "assets" / "sprites" / "anotacoes"
ANOTACOES = {
    "condicionais": ("Condicionais", "condicionais.png"),
    "loops": ("Laços", "loops.png"),
    "funcoes": ("Funções", "funcoes.png"),
}


class Colecao:
    def __init__(self):
        self.quantidades = {}
        self.icones = {}
        self.fonte = pygame.font.Font(None, 24)

        for tipo, (_, arquivo) in ANOTACOES.items():
            self.quantidades[tipo] = 0
            imagem = pygame.image.load(str(PASTA_ANOTACOES / arquivo)).convert_alpha()
            proporcao = 30 / imagem.get_height()
            largura = round(imagem.get_width() * proporcao)
            self.icones[tipo] = pygame.transform.smoothscale(imagem, (largura, 30))

    def adicionar(self, tipo):
        self.quantidades[tipo] += 1

    def desenhar(self, tela):
        x = 16

        for tipo, (nome, _) in ANOTACOES.items():
            icone = self.icones[tipo]
            texto = self.fonte.render(f"{nome}: {self.quantidades[tipo]}", True, (255, 255, 255))
            largura = icone.get_width() + texto.get_width() + 28
            fundo = pygame.Rect(x, 16, largura, 44)

            pygame.draw.rect(tela, (36, 32, 55), fundo, border_radius=8)
            tela.blit(icone, (x + 8, fundo.centery - icone.get_height() // 2))
            texto_rect = texto.get_rect(midleft=(x + 16 + icone.get_width(), fundo.centery))
            tela.blit(texto, texto_rect)
            x = fundo.right + 8