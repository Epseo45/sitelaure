import pygame
import random
import sys

# --- Configuration ---
WIDTH, HEIGHT = 500, 600
GRID_SIZE = 10
CELL_SIZE = 40
MARGIN = 50
FPS = 60

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
RED = (220, 20, 60)
GREEN = (34, 139, 34)
ORANGE = (255, 165, 0)

SHAPES = [
    [(0, 0)],  # 1 bloc
    [(0, 0), (1, 0)],  # 2 horizontaux
    [(0, 0), (0, 1)],  # 2 verticaux
    [(0, 0), (1, 0), (2, 0)],  # 3 horizontaux
    [(0, 0), (0, 1), (0, 2)],  # 3 verticaux
    [(0, 0), (1, 0), (0, 1), (1, 1)],  # carré
    [(0, 0), (1, 0), (2, 0), (3, 0)],  # ligne 4
    [(0, 0), (0, 1), (1, 1)],  # L
    [(1, 0), (0, 1), (1, 1), (2, 1)],  # T
]

COLORS = [BLUE, RED, GREEN, ORANGE]

# --- Initialisation ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Block Blast")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
current_shape = random.choice(SHAPES)
current_color = random.choice(COLORS)
score = 0

def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(MARGIN + x * CELL_SIZE,
                               MARGIN + y * CELL_SIZE,
                               CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)
            if grid[y][x]:
                pygame.draw.rect(screen, grid[y][x], rect)

def draw_shape(shape, color, mouse_pos):
    mx, my = mouse_pos
    gx = (mx - MARGIN) // CELL_SIZE
    gy = (my - MARGIN) // CELL_SIZE
    for dx, dy in shape:
        rect = pygame.Rect(MARGIN + (gx + dx) * CELL_SIZE,
                           MARGIN + (gy + dy) * CELL_SIZE,
                           CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, color, rect)

def can_place(shape, gx, gy):
    for dx, dy in shape:
        x, y = gx + dx, gy + dy
        if x < 0 or x >= GRID_SIZE or y < 0 or y >= GRID_SIZE:
            return False
        if grid[y][x] is not None:
            return False
    return True

def place_shape(shape, gx, gy, color):
    for dx, dy in shape:
        grid[gy + dy][gx + dx] = color

def clear_lines():
    global score
    cleared = 0

    # Lignes
    for y in range(GRID_SIZE):
        if all(grid[y][x] is not None for x in range(GRID_SIZE)):
            for x in range(GRID_SIZE):
                grid[y][x] = None
            cleared += 1

    # Colonnes
    for x in range(GRID_SIZE):
        if all(grid[y][x] is not None for y in range(GRID_SIZE)):
            for y in range(GRID_SIZE):
                grid[y][x] = None
            cleared += 1

    if cleared:
        score += cleared * 10

def draw_score():
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (MARGIN, 10))

def game_over():
    text = font.render("Game Over", True, RED)
    screen.blit(text, (WIDTH // 2 - 80, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

def has_moves():
    for shape in SHAPES:
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if can_place(shape, x, y):
                    return True
    return False

# --- Boucle principale ---
running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    draw_grid()
    draw_score()

    mouse_pos = pygame.mouse.get_pos()
    draw_shape(current_shape, current_color, mouse_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = mouse_pos
            gx = (mx - MARGIN) // CELL_SIZE
            gy = (my - MARGIN) // CELL_SIZE
            if can_place(current_shape, gx, gy):
                place_shape(current_shape, gx, gy, current_color)
                clear_lines()
                current_shape = random.choice(SHAPES)
                current_color = random.choice(COLORS)
                if not has_moves():
                    game_over()

    pygame.display.flip()

pygame.quit()
