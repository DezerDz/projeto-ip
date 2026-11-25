import pygame

from aluno import Aluno
from colecao import Colecao
from professor import Professor

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


    chao = pygame.Rect(0, ALTURA_TELA - 100, LARGURA_TELA, 100)
    superficies = [chao]

    aluno = Aluno(150, chao.top)
    professor = Professor(850, chao.top, "condicionais")
    colecao = Colecao()
    fonte = pygame.font.Font(None, 25)
    aviso_resgate = fonte.render("Pressione E para resgatar", True, (255, 255, 255))

    rodando = True
    while rodando:

        dt = relogio.tick(FPS) / 1000


        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                if evento.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    aluno.pular()
                if evento.key == pygame.K_e:
                    professor.resgatar(aluno.get_rect(), colecao)


        aluno.update(dt, superficies, LARGURA_TELA)


        tela.fill(COR_CEU)
        pygame.draw.rect(tela, COR_CHAO, chao)
        professor.desenhar(tela, 0, aluno.get_rect(), aviso_resgate)
        aluno.draw(tela, 0)
        colecao.desenhar(tela)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()