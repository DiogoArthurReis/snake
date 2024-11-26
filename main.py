import pygame
import time
import random
import os

# Inicializando o pygame
pygame.init()

# Definindo as cores
branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (213, 50, 80)
verde = (0, 255, 0)  # Cor para a maçã
azul = (0, 0, 255)  # Azul para a cobrinha
amarelo = (255, 255, 0)  # Cor para os olhos da cobrinha
marrom = (139, 69, 19)  # Cor para o cabinho da maçã

# Definindo o tamanho da tela
largura = 600
altura = 400

# Criando a tela
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo da Cobrinha')

# Carregar a imagem de fundo
imagem_fundo = pygame.image.load('assets/imagens/fundo.png')
imagem_fundo = pygame.transform.scale(imagem_fundo, (largura, altura))

# Definindo o relógio
relogio = pygame.time.Clock()

# Definindo o tamanho do bloco
tamanho_bloco = 20
velocidade_inicial = 10
velocidade = velocidade_inicial

# Fonte para o texto
fonte_comum = pygame.font.SysFont("bahnschrift", 25)
fonte_score = pygame.font.SysFont("comicsansms", 35)
fonte_game_over = pygame.font.SysFont("comicsansms", 60)
fonte_pontuacao_final = pygame.font.SysFont("comicsansms", 50)

# Função para exibir a pontuação
def nossa_pontuacao(pontos):
    valor = fonte_score.render("Pontuação: " + str(pontos), True, branco)
    tela.blit(valor, [10, 10])  # Colocando a pontuação no topo da tela, fora do jogo

# Função para desenhar a maçã mais realista
def desenhar_comida(comida_x, comida_y):
    # Desenhando a maçã como um círculo vermelho
    pygame.draw.circle(tela, vermelho, (comida_x + tamanho_bloco // 2, comida_y + tamanho_bloco // 2), tamanho_bloco // 2)
    # Desenhando o cabinho da maçã
    pygame.draw.rect(tela, marrom, [comida_x + tamanho_bloco // 2 - 2, comida_y - 5, 4, 10])  # Cabinho
    # Desenhando um sombreamento para dar efeito 3D
    pygame.draw.circle(tela, (255, 100, 100), (comida_x + 5, comida_y + 5), 6)  # Efeito de brilho

# Função que desenha a cobrinha com rosto voltado para a frente
def nossa_cobrinha(lista_cobrinha, direcao):
    for i, x in enumerate(lista_cobrinha):
        if i == len(lista_cobrinha) - 1:  # Cabeça da cobrinha (agora no final da lista)
            # Desenhando a cabeça com a "cara" voltada para a direção
            pygame.draw.rect(tela, azul, [x[0], x[1], tamanho_bloco, tamanho_bloco])  # Cabeça

            # Olhos da cobrinha (dois círculos brancos com pupilas pretas)
            olho_esquerdo_x = x[0] + 5
            olho_esquerdo_y = x[1] + 5
            olho_direito_x = x[0] + 12
            olho_direito_y = x[1] + 5
            pygame.draw.circle(tela, branco, (olho_esquerdo_x, olho_esquerdo_y), 4)  # Olho esquerdo branco
            pygame.draw.circle(tela, branco, (olho_direito_x, olho_direito_y), 4)  # Olho direito branco
            pygame.draw.circle(tela, preto, (olho_esquerdo_x, olho_esquerdo_y), 2)  # Pupila esquerda
            pygame.draw.circle(tela, preto, (olho_direito_x, olho_direito_y), 2)  # Pupila direita
            
            # Boca (um sorriso)
            pygame.draw.arc(tela, preto, [x[0] + 4, x[1] + 10, 12, 6], 3.14159, 0, 2)  # Boca sorridente

            # Desenhando o rosto com a direção correta
            if direcao == "esquerda":
                pygame.draw.polygon(tela, preto, [(x[0], x[1] + 5), (x[0] + 5, x[1] + 10), (x[0], x[1] + 15)])  # Direção esquerda
            elif direcao == "direita":
                pygame.draw.polygon(tela, preto, [(x[0] + tamanho_bloco, x[1] + 5), (x[0] + tamanho_bloco - 5, x[1] + 10), (x[0] + tamanho_bloco, x[1] + 15)])  # Direção direita
            elif direcao == "cima":
                pygame.draw.polygon(tela, preto, [(x[0] + 5, x[1]), (x[0] + 10, x[1] + 5), (x[0] + 15, x[1])])  # Direção cima
            elif direcao == "baixo":
                pygame.draw.polygon(tela, preto, [(x[0] + 5, x[1] + tamanho_bloco), (x[0] + 10, x[1] + tamanho_bloco - 5), (x[0] + 15, x[1] + tamanho_bloco)])  # Direção baixo

        else:
            # Corpo da cobrinha
            pygame.draw.rect(tela, azul, [x[0], x[1], tamanho_bloco, tamanho_bloco])  # Corpo

# Função para salvar e carregar o ranking
def carregar_ranking():
    if not os.path.exists("ranking.txt"):
        with open("ranking.txt", "w") as f:
            f.write("0")  # Se não houver ranking, cria o arquivo com a pontuação 0
    with open("ranking.txt", "r") as f:
        return int(f.read())

def salvar_ranking(pontos):
    ranking = carregar_ranking()
    if pontos > ranking:
        with open("ranking.txt", "w") as f:
            f.write(str(pontos))

# Função para exibir a mensagem de "Game Over"
def mostrar_game_over(pontos):
    tela.fill(preto)

    # Mensagem "Game Over"
    texto_game_over = fonte_game_over.render("GAME OVER", True, vermelho)
    tela.blit(texto_game_over, [largura / 2 - texto_game_over.get_width() / 2, altura / 3])

    # Pontuação final
    texto_pontuacao = fonte_pontuacao_final.render(f"Sua Pontuação: {pontos}", True, branco)
    tela.blit(texto_pontuacao, [largura / 2 - texto_pontuacao.get_width() / 2, altura / 2])

    # Instruções para reiniciar ou sair
    texto_reiniciar = fonte_comum.render("Pressione C para jogar novamente ou Q para sair", True, amarelo)
    tela.blit(texto_reiniciar, [largura / 2 - texto_reiniciar.get_width() / 2, altura * 3 / 4])

    pygame.display.update()

# Função principal do jogo
def jogo():
    global velocidade

    fim_de_jogo = False
    game_over = False

    # Coordenadas iniciais da cobrinha
    x1 = largura / 2
    y1 = altura / 2

    x1_mudanca = 0
    y1_mudanca = 0

    direcao = "direita"  # Direção inicial da cobrinha

    # Lista que armazena os segmentos da cobrinha
    cobrinha_lista = []
    comprimento_cobrinha = 1

    # Coordenadas da comida
    comida_x = round(random.randrange(0, largura - tamanho_bloco) / tamanho_bloco) * tamanho_bloco
    comida_y = round(random.randrange(0, altura - tamanho_bloco) / tamanho_bloco) * tamanho_bloco

    while not fim_de_jogo:

        while game_over:
            pontos = comprimento_cobrinha - 1
            mostrar_game_over(pontos)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    fim_de_jogo = True
                    game_over = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_q:
                        fim_de_jogo = True
                        game_over = False
                    if evento.key == pygame.K_c:
                        jogo()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_de_jogo = True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    x1_mudanca = -tamanho_bloco
                    y1_mudanca = 0
                    direcao = "esquerda"
                elif evento.key == pygame.K_RIGHT:
                    x1_mudanca = tamanho_bloco
                    y1_mudanca = 0
                    direcao = "direita"
                elif evento.key == pygame.K_UP:
                    y1_mudanca = -tamanho_bloco
                    x1_mudanca = 0
                    direcao = "cima"
                elif evento.key == pygame.K_DOWN:
                    y1_mudanca = tamanho_bloco
                    x1_mudanca = 0
                    direcao = "baixo"

        # Movimentação e teletransporte
        x1 += x1_mudanca
        y1 += y1_mudanca

        # Teletransportando a cobrinha para o lado oposto ao colidir com a tela
        if x1 >= largura:
            x1 = 0
        elif x1 < 0:
            x1 = largura - tamanho_bloco
        if y1 >= altura:
            y1 = 0
        elif y1 < 0:
            y1 = altura - tamanho_bloco

        # Exibindo o fundo com a imagem carregada
        tela.blit(imagem_fundo, (0, 0))

        # Desenhando a comida (maçã mais realista)
        desenhar_comida(comida_x, comida_y)

        # Desenhando a cobrinha (com rosto voltado para a frente)
        nossa_cobrinha(cobrinha_lista, direcao)

        nossa_pontuacao(comprimento_cobrinha - 1)

        pygame.display.update()

        # Verificando se a cabeça da cobrinha encostou na comida
        if x1 == comida_x and y1 == comida_y:  # Se a cabeça da cobrinha encostou na comida
            comida_x = round(random.randrange(0, largura - tamanho_bloco) / tamanho_bloco) * tamanho_bloco
            comida_y = round(random.randrange(0, altura - tamanho_bloco) / tamanho_bloco) * tamanho_bloco
            comprimento_cobrinha += 1  # A cobrinha cresce

            # Aumento de velocidade controlado
            if (comprimento_cobrinha - 1) % 10 == 0:  # A cada 10 pontos, aumenta a velocidade
                if velocidade < 30:  # Limite máximo de velocidade
                    velocidade += 1

        # Adicionando a nova posição da cabeça da cobrinha no final da lista (invertendo a ordem)
        cabeça_cobrinha = []
        cabeça_cobrinha.append(x1)
        cabeça_cobrinha.append(y1)
        cobrinha_lista.append(cabeça_cobrinha)

        # Verificando se a cobrinha bateu em si mesma
        if len(cobrinha_lista) > comprimento_cobrinha:
            del cobrinha_lista[0]

        for x in cobrinha_lista[:-1]:
            if x == cabeça_cobrinha:
                game_over = True

        relogio.tick(velocidade)

    salvar_ranking(comprimento_cobrinha - 1)
    pygame.quit()
    quit()

# Iniciar o jogo
jogo()
