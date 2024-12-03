import pygame
import random
import sqlite3
import time

# Inicializar Pygame
pygame.init()

# Configurações da tela e cores
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Cobrinha")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Conexão com o banco de dados SQLite
conn = sqlite3.connect("ranking.db")
cursor = conn.cursor()

# Recriar a tabela 'ranking' com estrutura correta
cursor.execute("DROP TABLE IF EXISTS ranking")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS ranking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        score INTEGER NOT NULL
    )
""")
conn.commit()

# Função para salvar pontuação no ranking
def save_score(name, score):
    cursor.execute("INSERT INTO ranking (name, score) VALUES (?, ?)", (name, score))
    conn.commit()

# Função para obter os 5 melhores do ranking
def get_top_scores():
    cursor.execute("SELECT name, score FROM ranking ORDER BY score DESC LIMIT 5")
    return cursor.fetchall()

# Função para exibir o ranking na tela
def draw_ranking():
    scores = get_top_scores()
    screen.fill(BLACK)
    font = pygame.font.Font(None, 50)
    title = font.render("Ranking - Top 5", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
    for i, (name, score) in enumerate(scores, start=1):
        text = font.render(f"{i}. {name}: {score}", True, WHITE)
        screen.blit(text, (WIDTH // 4, 100 + i * 50))
    pygame.display.flip()
    pygame.time.wait(5000)

# Loop principal do jogo
def game_loop(player_name):
    clock = pygame.time.Clock()
    snake = [(WIDTH // 2, HEIGHT // 2)]
    direction = (0, -CELL_SIZE)
    food = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
            random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
    score = 0
    level = 1
    start_time = time.time()
    running = True

    while running:
        screen.fill(BLACK)

        # Checar tempo para passar de fase
        elapsed_time = time.time() - start_time
        if level == 1 and score >= 40 and elapsed_time <= 25:
            level = 2  # Passar para a próxima fase
            start_time = time.time()  # Reiniciar o tempo para a próxima fase
        elif level == 2 and score >= 80 and elapsed_time <= 20:
            level = 3
            start_time = time.time()
        elif level == 3 and score >= 150 and elapsed_time <= 15:
            level = 4  # Passar para a fase bônus
            start_time = time.time()
        elif elapsed_time > (25 if level == 1 else 20 if level == 2 else 15):  # Se exceder o tempo, perde o jogo
            return score

        # Eventos do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Movimentação
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and direction != (0, CELL_SIZE):
            direction = (0, -CELL_SIZE)
        if keys[pygame.K_DOWN] and direction != (0, -CELL_SIZE):
            direction = (0, CELL_SIZE)
        if keys[pygame.K_LEFT] and direction != (CELL_SIZE, 0):
            direction = (-CELL_SIZE, 0)
        if keys[pygame.K_RIGHT] and direction != (-CELL_SIZE, 0):
            direction = (CELL_SIZE, 0)

        # Atualizar posição da cobra
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        if new_head in snake or not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
            return score  # Fim do jogo
        snake.insert(0, new_head)

        # Verificar se comeu comida
        if new_head == food:
            score += 10
            food = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                    random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)

        else:
            snake.pop()

        # Desenhar comida e cobra
        pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

        # Mostrar pontuação e nível
        font = pygame.font.Font(None, 35)
        score_text = font.render(f"Score: {score} Level: {level}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Mostrar tempo restante para passar de fase
        time_remaining = 0
        if level == 1:
            time_remaining = max(0, 25 - int(elapsed_time))
        elif level == 2:
            time_remaining = max(0, 20 - int(elapsed_time))
        elif level == 3:
            time_remaining = max(0, 15 - int(elapsed_time))

        time_text = font.render(f"Time Left: {time_remaining}s", True, WHITE)
        screen.blit(time_text, (WIDTH - 200, 10))

        pygame.display.flip()

        if level == 4:  # Fase bônus
            clock.tick(15 + int(score / 50))  # Fase bônus: aumenta muito a velocidade conforme o score
        else:
            clock.tick(7 + level * 2)  # Aumentar gradualmente a velocidade

    return score

# Menu de Game Over
def game_over_menu(score, player_name):
    save_score(player_name, score)

    while True:
        screen.fill(BLACK)

        # Renderizar textos
        font = pygame.font.Font(None, 50)
        game_over_text = font.render("Game Over", True, RED)
        score_text = font.render(f"Your Score: {score}", True, WHITE)
        play_again_text = font.render("Press R to Play Again", True, GREEN)
        ranking_text = font.render("Press T to View Ranking", True, BLUE)
        quit_text = font.render("Press Q to Quit", True, WHITE)

        # Exibir textos na tela
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 50))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 150))
        screen.blit(play_again_text, (WIDTH // 2 - play_again_text.get_width() // 2, 250))
        screen.blit(ranking_text, (WIDTH // 2 - ranking_text.get_width() // 2, 350))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 450))

        pygame.display.flip()

        # Gerenciar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Jogar novamente
                    return True
                if event.key == pygame.K_t:  # Ver ranking
                    draw_ranking()
                if event.key == pygame.K_q:  # Sair
                    pygame.quit()
                    exit()

# Solicitar nome do jogador
def get_player_name():
    font = pygame.font.Font(None, 50)
    name = ""
    input_box = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50)
    active = True

    while active:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name:
                        return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        pygame.draw.rect(screen, WHITE, input_box, 2)
        text_surface = font.render(name, True, WHITE)
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
        pygame.display.flip()

# Função principal
def main():
    player_name = get_player_name()
    while True:
        score = game_loop(player_name)
        if not game_over_menu(score, player_name):
            break

if __name__ == "__main__":
    main()
