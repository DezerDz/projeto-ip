import sys
import pygame


class Cenario:

  def __init__(self, largura, altura):
    self.largura = largura
    self.altura = altura

    # o cenário é maior que a tela para permitir a movimentação
    self.larguradomundo = largura * 3

    # cores usadas no céu
    self.corceu = (91, 170, 225)
    self.corhorizonte = (211, 235, 245)

    # cores do chão e da vegetação
    self.corgrama = (55, 160, 55)
    self.corgramaclara = (91, 190, 65)
    self.corgramaescura = (35, 110, 45)
    self.corterra = (125, 72, 42)
    self.corterraescura = (90, 48, 30)

    # configurações do chão
    self.alturadochao = 100

    self.chao = pygame.Rect(
        0, altura - self.alturadochao, self.larguradomundo, self.alturadochao
    )

    # posições das plataformas
    self.plataformas = [
        pygame.Rect(300, altura - 280, 220, 25),
        pygame.Rect(600, altura - 360, 220, 25),
        pygame.Rect(950, altura - 310, 220, 25),
        pygame.Rect(1250, altura - 430, 220, 25),
        pygame.Rect(1600, altura - 350, 220, 25),
        pygame.Rect(1950, altura - 480, 220, 25),
        pygame.Rect(2350, altura - 290, 220, 25),
    ]

    # essas superfícies também são usadas na colisão com o personagem
    self.superficies = [self.chao] + self.plataformas

    # posição horizontal da câmera
    self.camerax = 0

    # posições das nuvens ao longo do cenário
    self.nuvens = []

    for indice in range(self.larguradomundo // 480 + 2):
      posicaox = 100 + indice * 480
      posicaoy = 70 + (indice % 3) * 65
      tamanho = 0.8 + (indice % 3) * 0.15

      self.nuvens.append((posicaox, posicaoy, tamanho))

    # árvores espalhadas pelo cenário
    self.arvores = []

    for indice in range(self.larguradomundo // 720 + 1):
      posicaox = 200 + indice * 720
      tamanho = 0.8 + (indice % 3) * 0.2

      self.arvores.append((posicaox, tamanho))

  # posição horizontal da câmera
  def atualizarcamera(self, personagem):
    self.camerax = personagem.centerx - self.largura // 2

    self.camerax = max(
        0, min(self.camerax, self.larguradomundo - self.largura)
    )

  # desenha o céu e o sol
  def desenharceu(self, tela):
    for indice in range(24):
      proporcao = indice / 23

      cor = (
          int(
              self.corceu[0] + (self.corhorizonte[0] - self.corceu[0]) * proporcao
          ),
          int(
              self.corceu[1] + (self.corhorizonte[1] - self.corceu[1]) * proporcao
          ),
          int(
              self.corceu[2] + (self.corhorizonte[2] - self.corceu[2]) * proporcao
          ),
      )

      alturafaixa = self.altura // 24 + 1

      pygame.draw.rect(
          tela, cor, (0, indice * alturafaixa, self.largura, alturafaixa)
      )

    # o sol acompanha a câmera mais devagar que o cenário
    posicaosol = int(self.largura * 0.78 - self.camerax * 0.08)
    posicaoy = int(self.altura * 0.18)

    pygame.draw.circle(tela, (255, 220, 100), (posicaosol, posicaoy), 55)

    pygame.draw.circle(tela, (255, 240, 160), (posicaosol, posicaoy), 43)

  # posições das nuvens ao longo do cenário
  def desenharnuvem(self, tela, x, y, tamanho):
    cor = (255, 255, 255)

    pygame.draw.ellipse(
        tela,
        cor,
        (
            int(x),
            int(y + 20 * tamanho),
            int(130 * tamanho),
            int(45 * tamanho),
        ),
    )

    pygame.draw.circle(
        tela,
        cor,
        (int(x + 35 * tamanho), int(y + 25 * tamanho)),
        int(28 * tamanho),
    )

    pygame.draw.circle(
        tela,
        cor,
        (int(x + 70 * tamanho), int(y + 10 * tamanho)),
        int(35 * tamanho),
    )

    pygame.draw.circle(
        tela,
        cor,
        (int(x + 105 * tamanho), int(y + 28 * tamanho)),
        int(25 * tamanho),
    )

  def desenharnuvens(self, tela):
    for x, y, tamanho in self.nuvens:
      posicaox = int(x - self.camerax * 0.45)

      if -180 < posicaox < self.largura + 180:
        self.desenharnuvem(tela, posicaox, y, tamanho)

  # desenha as montanhas ao fundo
  def desenharmontanhas(self, tela):
    base = int(self.altura * 0.78)

    for indice in range(-1, self.larguradomundo // 500 + 2):
      x = indice * 500 - int(self.camerax * 0.22)

      alturapico = int(self.altura * (0.18 + (indice % 3) * 0.04))

      pygame.draw.polygon(
          tela,
          (105, 145, 160),
          [(x, base), (x + 250, base - alturapico), (x + 500, base)],
      )

      # parte branca no alto das montanhas
      pygame.draw.polygon(
          tela,
          (235, 245, 240),
          [
              (x + 205, base - alturapico + 55),
              (x + 250, base - alturapico),
              (x + 295, base - alturapico + 55),
              (x + 265, base - alturapico + 42),
              (x + 250, base - alturapico + 60),
              (x + 235, base - alturapico + 42),
          ],
      )

  # as colinas ficam entre as montanhas e o chão
  def desenharcolinas(self, tela):
    base = int(self.altura * 0.88)

    for indice in range(-1, self.larguradomundo // 650 + 2):
      x = indice * 650 - int(self.camerax * 0.42)

      pygame.draw.ellipse(tela, (100, 175, 95), (x, base - 150, 750, 300))

      pygame.draw.ellipse(tela, (75, 155, 75), (x + 300, base - 115, 650, 250))

  # árvores espalhadas pelo cenário
  def desenhararvore(self, tela, x, escala):
    base = self.chao.top

    larguradotronco = int(22 * escala)
    alturadotronco = int(90 * escala)

    # tronco da árvore
    pygame.draw.rect(
        tela,
        (105, 60, 35),
        (
            int(x - larguradotronco // 2),
            int(base - alturadotronco),
            larguradotronco,
            alturadotronco,
        ),
    )

    # folhas da árvore
    posicaoy = int(base - alturadotronco)

    pygame.draw.circle(tela, (30, 110, 45), (int(x), posicaoy), int(48 * escala))

    pygame.draw.circle(
        tela,
        (45, 145, 55),
        (int(x - 30 * escala), int(posicaoy + 10 * escala)),
        int(35 * escala),
    )

    pygame.draw.circle(
        tela,
        (55, 160, 65),
        (int(x + 30 * escala), int(posicaoy + 10 * escala)),
        int(35 * escala),
    )

    pygame.draw.circle(
        tela,
        (65, 175, 65),
        (int(x), int(posicaoy - 27 * escala)),
        int(34 * escala),
    )

  # desenha as árvores, a grama e algumas flores
  def desenharvegetacao(self, tela):

    # árvores espalhadas pelo cenário
    for x, escala in self.arvores:
      posicaox = int(x - self.camerax)

      if -100 < posicaox < self.largura + 100:
        self.desenhararvore(tela, posicaox, escala)

    # pequenos traços para representar a grama
    for x in range(25, self.larguradomundo, 65):
      posicaox = x - self.camerax

      if -20 < posicaox < self.largura + 20:
        base = self.chao.top
        tamanho = 8 + (x // 65 % 5) * 2

        pygame.draw.line(
            tela,
            (25, 120, 35),
            (posicaox, base),
            (posicaox - 4, base - tamanho),
            2,
        )

        pygame.draw.line(
            tela,
            (30, 135, 40),
            (posicaox, base),
            (posicaox + 5, base - tamanho - 3),
            2,
        )

    # algumas flores para deixar o chão menos vazio
    for x in range(100, self.larguradomundo, 240):
      posicaox = x - self.camerax

      if -20 < posicaox < self.largura + 20:
        base = self.chao.top

        pygame.draw.line(
            tela,
            (30, 120, 35),
            (posicaox, base),
            (posicaox, base - 13),
            2,
        )

        pygame.draw.circle(tela, (255, 220, 50), (posicaox, base - 16), 5)

        pygame.draw.circle(tela, (255, 120, 150), (posicaox + 5, base - 13), 3)

  # configurações do chão
  def desenharchao(self, tela):
    chao = self.chao.move(-self.camerax, 0)

    # base de terra da plataforma
    pygame.draw.rect(tela, self.corterra, chao)

    # pequenos pontos para dar textura à terra
    for x in range(0, self.larguradomundo, 100):
      posicaox = x - self.camerax

      if -20 < posicaox < self.largura + 20:
        y = self.chao.top + 35 + (x // 100 % 4) * 12

        pygame.draw.circle(tela, (100, 55, 35), (posicaox, y), 4)

        pygame.draw.circle(tela, (150, 90, 50), (posicaox + 20, y + 20), 3)

    # camada de grama na parte de cima do chão
    pygame.draw.rect(tela, self.corgrama, (chao.x, chao.y, chao.width, 17))

    pygame.draw.rect(tela, self.corgramaclara, (chao.x, chao.y, chao.width, 5))

    pygame.draw.line(
        tela,
        self.corgramaescura,
        (chao.left, chao.top + 17),
        (chao.right, chao.top + 17),
        2,
    )

  # posições das plataformas
  def desenharplataformas(self, tela):
    for plataforma in self.plataformas:
      posicao = plataforma.move(-self.camerax, 0)

      if posicao.right < 0 or posicao.left > self.largura:
        continue

      # sombra logo abaixo da plataforma
      pygame.draw.rect(
          tela,
          (65, 45, 35),
          (posicao.x + 5, posicao.y + 5, posicao.width, posicao.height),
      )

      # base de terra da plataforma
      pygame.draw.rect(tela, self.corterra, posicao)

      # alguns pontos para quebrar a aparência lisa
      pygame.draw.circle(tela, (160, 95, 55), (posicao.x + 40, posicao.y + 17), 3)

      pygame.draw.circle(tela, (90, 50, 30), (posicao.x + 120, posicao.y + 17), 3)

      pygame.draw.circle(tela, (160, 95, 55), (posicao.x + 185, posicao.y + 17), 3)

      # grama na parte de cima da plataforma
      pygame.draw.rect(tela, self.corgrama, (posicao.x, posicao.y, posicao.width, 8))

      pygame.draw.rect(
          tela, self.corgramaclara, (posicao.x, posicao.y, posicao.width, 3)
      )

      # contorno para destacar a plataforma
      pygame.draw.rect(tela, (75, 45, 30), posicao, 2)

      # pequenos detalhes nas bordas
      for x in range(posicao.x + 15, posicao.right, 45):
        pygame.draw.line(
            tela, (35, 120, 40), (x, posicao.y + 2), (x - 3, posicao.y - 5), 2
        )

  # reúne as partes do cenário na ordem em que aparecem na tela
  def desenhar(self, tela):
    self.desenharceu(tela)
    self.desenharnuvens(tela)
    self.desenharmontanhas(tela)
    self.desenharcolinas(tela)
    self.desenharchao(tela)
    self.desenharvegetacao(tela)
    self.desenharplataformas(tela)


# 1. ABRIR E INICIALIZAR O JOGO
pygame.init()

LARGURA = 800
ALTURA = 600
FPS = 60

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo do Aluno")
relogio = pygame.time.Clock()

# Cores básicas
BRANCO = (255, 255, 255)
AZUL = (50, 120, 220)
VERDE = (50, 180, 80)

# Retângulo provisório do aluno
aluno_rect = pygame.Rect(100, 300, 40, 50)
velocidade_y = 0


# 2. FUNÇÃO PARA RETORNAR AO INÍCIO
def reiniciar_jogo():
  aluno_rect.x = 100
  aluno_rect.y = 300

  return 0


# --- INÍCIO DO BLOCO DE TESTE (Apagar quando Pessoa 1 e 2 colocarem o código deles) ---
cenario = Cenario(LARGURA, ALTURA)
chao_teste = pygame.Rect(0, ALTURA - 100, 450, 100)  # Chão com um buraco à direita
cenario.chao = chao_teste
cenario.superficies = [cenario.chao] + cenario.plataformas
no_chao = False

# LOOP PRINCIPAL DO JOGO
rodando = True
while rodando:
  relogio.tick(FPS)

  # 3. FECHAR O JOGO CORRETAMENTE
  for evento in pygame.event.get():
    if evento.type == pygame.QUIT:  # Clicou no "X" da janela
      rodando = False
    if evento.type == pygame.KEYDOWN:
      if evento.key == pygame.K_ESCAPE:  # Apertou ESC para sair
        rodando = False
      if (
          evento.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP) and no_chao
      ):
        velocidade_y = -12
        no_chao = False

  # simulação de queda
  teclas = pygame.key.get_pressed()
  if teclas[pygame.K_RIGHT]:
    aluno_rect.x += 5
  if teclas[pygame.K_LEFT]:
    aluno_rect.x -= 5

  velocidade_y += 0.5  # Gravidade teste
  aluno_rect.y += int(velocidade_y)
  no_chao = False

  for superficie in cenario.superficies:
    if aluno_rect.colliderect(superficie) and velocidade_y > 0:
      aluno_rect.bottom = superficie.top
      velocidade_y = 0
      no_chao = True

  cenario.atualizarcamera(aluno_rect)

  # Se o topo do aluno passar da altura da tela, ele caiu no buraco
  if aluno_rect.top > ALTURA:
    velocidade_y = reiniciar_jogo()

  # DESENHO NA TELA
  tela.fill(BRANCO)

  # Desenho provisório do chão
  cenario.desenhar(tela)
  pygame.draw.rect(tela, AZUL, aluno_rect.move(-cenario.camerax, 0))

  pygame.display.flip()

# Encerra o Pygame
pygame.quit()
sys.exit()