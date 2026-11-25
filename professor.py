import pygame

COR_ROUPA = (109, 53, 140)
COR_PELE = (241, 194, 150)


class Professor:
    def __init__(self, x, y, tipo_item):

        self.rect = pygame.Rect(0, 0, 42, 64)
        self.rect.midbottom = (x, y)
        self.area_interacao = self.rect.inflate(96, 24)
        self.tipo_item = tipo_item
        self.resgatado = False

    def pode_resgatar(self, rect_aluno):
        return not self.resgatado and self.area_interacao.colliderect(rect_aluno)

    def resgatar(self, rect_aluno, colecao):
        if not self.pode_resgatar(rect_aluno):
            return

        colecao.adicionar(self.tipo_item)
        self.resgatado = True

    def desenhar(self, tela, camerax, rect_aluno, aviso_resgate):
        if self.resgatado:
            return

        rect = self.rect.move(-camerax, 0)
        corpo = pygame.Rect(rect.x, rect.y + 24, rect.width, rect.height - 24)
        pygame.draw.rect(tela, COR_ROUPA, corpo, border_radius=6)
        pygame.draw.circle(tela, COR_PELE, (rect.centerx, rect.y + 13), 12)

        if self.pode_resgatar(rect_aluno):
            aviso_rect = aviso_resgate.get_rect(midbottom=(rect.centerx, rect.top - 8))
            aviso_rect.clamp_ip(tela.get_rect())
            fundo = aviso_rect.inflate(14, 8)
            fundo.clamp_ip(tela.get_rect())
            pygame.draw.rect(tela, (36, 32, 55), fundo, border_radius=5)
            tela.blit(aviso_resgate, aviso_rect)