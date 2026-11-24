import pygame

from aluno import Aluno

LARGURA_TELA = 1280
ALTURA_TELA = 720
FPS = 60
TITULO = "Projeto IP - Equipe 10"

COR_CEU = (186, 220, 245)
COR_CHAO = (92, 160, 82)


def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO)
    relogio = pygame.time.Clock()

    # chão provisório só pra testar o aluno (depois entra o cenário)
    chao = pygame.Rect(0, ALTURA_TELA - 100, LARGURA_TELA, 100)
    superficies = [chao]

    aluno = Aluno(150, chao.top)

    rodando = True
    while rodando:
        # dt é o tempo (em segundos) desde o último quadro
        dt = relogio.tick(FPS) / 1000

        # 1) eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                if evento.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    aluno.pular()

        # 2) atualizar
        aluno.update(dt, superficies, LARGURA_TELA)

        # 3) desenhar
        tela.fill(COR_CEU)
        pygame.draw.rect(tela, COR_CHAO, chao)
        aluno.draw(tela, 0)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()