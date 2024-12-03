import pygame
import random
import sqlite3
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Cobrinha")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

conn = sqlite3.connect("ranking.db")
cursor = conn.cursor()

cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS ranking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        score INTEGER NOT NULL
    )
""")
conn.commit()

def save_score(name, score):
    cursor.execute("INSERT INTO ranking (name, score) VALUES (?, ?)", (name, score))
    conn.commit()

def get_top_scores():
    cursor.execute("SELECT name, score FROM ranking ORDER BY score DESC LIMIT 5")
    return cursor.fetchall()

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

        elapsed_time = time.time() - start_time
        if level == 1 and score >= 50 and elapsed_time <= 25:
            level = 2  
            start_time = time.time()  
        elif level == 2 and score >= 100 and elapsed_time <= 20:
            level = 3
            start_time = time.time()
        elif level == 3 and score >= 150 and elapsed_time <= 15:
            level = 4  
            start_time = time.time() 
        elif level != 4 and elapsed_time > (25 if level == 1 else 20 if level == 2 else 15):  
            return score

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and direction != (0, CELL_SIZE):
            direction = (0, -CELL_SIZE)
        if keys[pygame.K_DOWN] and direction != (0, -CELL_SIZE):
            direction = (0, CELL_SIZE)
        if keys[pygame.K_LEFT] and direction != (CELL_SIZE, 0):
            direction = (-CELL_SIZE, 0)
        if keys[pygame.K_RIGHT] and direction != (-CELL_SIZE, 0):
            direction = (CELL_SIZE, 0)

        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        if new_head in snake or not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
            return score 
        snake.insert(0, new_head)

        if new_head == food:
            score += 10
            food = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                    random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)

        else:
            snake.pop()

        pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

        font = pygame.font.Font(None, 35)
        level_text = f"Level: {level}" if level != 4 else "Level: Bônus"  
        score_text = font.render(f"Score: {score} {level_text}", True, WHITE)
        screen.blit(score_text, (10, 10))

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

        if level == 4: 
            clock.tick(12 + int(score / 20))  
        else:
            clock.tick(7 + level * 2)

    return score

def game_over_menu(score, player_name):
    save_score(player_name, score)

    while True:
        screen.fill(BLACK)

        font = pygame.font.Font(None, 50)
        game_over_text = font.render("Game Over", True, RED)
        score_text = font.render(f"Sua Pontuação: {score}", True, WHITE)
        play_again_text = font.render("Pression R para Jogar Novamente", True, GREEN)
        ranking_text = font.render("Pressione T para Ver o Ranking", True, BLUE)
        quit_text = font.render("Pressione Q para sair", True, WHITE)

        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 50))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 150))
        screen.blit(play_again_text, (WIDTH // 2 - play_again_text.get_width() // 2, 250))
        screen.blit(ranking_text, (WIDTH // 2 - ranking_text.get_width() // 2, 350))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 450))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  
                    return True
                if event.key == pygame.K_t: 
                    draw_ranking()
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

def get_player_name():
    font = pygame.font.Font(None, 50)
    name = ""
    input_box = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50)
    active = True

    while active:
        screen.fill(BLACK)

        instruction_text = font.render("Digite seu nome:", True, WHITE)
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 4))

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

def main():
    player_name = get_player_name()
    while True:
        score = game_loop(player_name)
        if not game_over_menu(score, player_name):
            break

if __name__ == "__main__":
    main()
