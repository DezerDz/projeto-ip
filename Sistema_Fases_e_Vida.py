import pygame

# Inicialização do Pygame
pygame.init()

LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Fases - Teste")
relogio = pygame.time.Clock()

# Fontes para avisos e vidas
fonte_hud = pygame.font.SysFont("arial", 26, bold=True)
fonte_aviso = pygame.font.SysFont("arial", 24, bold=True)
fonte_fim = pygame.font.SysFont("arial", 40, bold=True)

# Cores
BRANCO = (255, 255, 255)
PRETO = (15, 15, 15)
VERDE = (0, 220, 80)
VERMELHO = (220, 50, 50)
AMARELO = (255, 220, 50)

# cores de fundo de cada fase
FASES = {
    1: {
        "cor_fundo": (30, 50, 90),      # Azul 
        "inicio": (60, 275),
        "buraco": pygame.Rect(350, 250, 90, 90),
        "objetivo": pygame.Rect(680, 270, 50, 50),
    },
    2: {
        "cor_fundo": (75, 35, 95),      # Roxo escuro
        "inicio": (60, 100),
        "buraco": pygame.Rect(360, 200, 110, 110),
        "objetivo": pygame.Rect(680, 450, 50, 50),
    },
    3: {
        "cor_fundo": (25, 75, 70),      # Verde
        "inicio": (60, 480),
        "buraco": pygame.Rect(340, 230, 130, 130),
        "objetivo": pygame.Rect(680, 100, 50, 50),
    },
}

def iniciar_jogo():
    fase = 1
    vidas = 3
    ix, iy = FASES[fase]["inicio"]
    jogador = pygame.Rect(ix, iy, 40, 40)
    return fase, vidas, jogador, "playing", "Fase 1 iniciada!", 120

fase_atual, vidas, jogador, estado, texto_aviso, tempo_aviso = iniciar_jogo()
velocidade = 5
rodando = True

while rodando:
    relogio.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            if estado in ("vitoria", "derrota"):
                if evento.key == pygame.K_r:
                    fase_atual, vidas, jogador, estado, texto_aviso, tempo_aviso = iniciar_jogo()
                elif evento.key == pygame.K_ESCAPE:
                    rodando = False

    # Lógica enquanto está jogando (é só pra testar)
    if estado == "playing":
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            jogador.x = jogador.x - velocidade
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            jogador.x = jogador.x + velocidade
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            jogador.y = jogador.y - velocidade
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            jogador.y = jogador.y + velocidade

        # Impede sair da tela
        if jogador.left < 0:
            jogador.left = 0
        if jogador.right > LARGURA:
            jogador.right = LARGURA
        if jogador.top < 60:
            jogador.top = 60
        if jogador.bottom > ALTURA:
            jogador.bottom = ALTURA

        buraco_atual = FASES[fase_atual]["buraco"]
        objetivo_atual = FASES[fase_atual]["objetivo"]

        # verifica se caiu no buraco (perdeu vida)
        if jogador.colliderect(buraco_atual):
            vidas = vidas - 1
            if vidas <= 0:
                vidas = 0
                estado = "derrota"
            else:
                ix, iy = FASES[fase_atual]["inicio"]
                jogador.topleft = (ix, iy)
                texto_aviso = f"Caiu no buraco! Restam {vidas} vida(s)!"
                tempo_aviso = 120

        # verifica se passou de fase
        elif jogador.colliderect(objetivo_atual):
            if fase_atual < 3:
                fase_atual = fase_atual + 1
                ix, iy = FASES[fase_atual]["inicio"]
                jogador.topleft = (ix, iy)
                texto_aviso = f"Passou para a Fase {fase_atual}!"
                tempo_aviso = 120
            else:
                estado = "vitoria"

    # Desenho na tela
    cor_fundo = FASES[fase_atual]["cor_fundo"]
    tela.fill(cor_fundo)

    # Barra superior
    pygame.draw.rect(tela, (20, 20, 20), (0, 0, LARGURA, 60))

    # Texto da Fase e Vidas
    txt_fase = fonte_hud.render(f"Fase: {fase_atual}/3", True, BRANCO)
    tela.blit(txt_fase, (20, 15))

    txt_vidas = fonte_hud.render(f"Vidas: {vidas}", True, BRANCO)
    tela.blit(txt_vidas, (180, 15))

    # sistema de vidas
    for i in range(vidas):
        pygame.draw.rect(tela, VERMELHO, (300 + i * 32, 18, 22, 22))

    # Aviso temporario das vidas
    if tempo_aviso > 0 and estado == "playing":
        txt_av = fonte_aviso.render(texto_aviso, True, AMARELO)
        tela.blit(txt_av, (420, 17))
        tempo_aviso = tempo_aviso - 1

    # desenha um buraco imaginario e um local que serve pra mudar de fase
    pygame.draw.rect(tela, PRETO, FASES[fase_atual]["buraco"])
    pygame.draw.rect(tela, VERDE, FASES[fase_atual]["objetivo"])
    pygame.draw.rect(tela, BRANCO, jogador)

    # Tela final 
    if estado in ("vitoria", "derrota"):
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(190)
        overlay.fill((0, 0, 0))
        tela.blit(overlay, (0, 0))

        if estado == "vitoria":
            msg_titulo = fonte_fim.render("VOCÊ VENCEU TODAS AS FASES!", True, VERDE)
        else:
            msg_titulo = fonte_fim.render("VOCÊ PERDEU! (3 QUEDAS)", True, VERMELHO)

        msg_sub = fonte_hud.render("Pressione [R] para jogar de novo ou [ESC] para sair", True, BRANCO)

        tela.blit(msg_titulo, msg_titulo.get_rect(center=(LARGURA // 2, ALTURA // 2 - 30)))
        tela.blit(msg_sub, msg_sub.get_rect(center=(LARGURA // 2, ALTURA // 2 + 30)))

    pygame.display.flip()

pygame.quit()
