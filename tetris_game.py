import pygame
import random

pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLOCK_SIZE = 30

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Tetromino shapes
SHAPES = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 1, 1],
     [1, 1, 0]],

    [[1, 1, 0],
     [0, 1, 1]],

    [[1, 1],
     [1, 1]],

    [[1, 1, 1, 1]],

    [[1, 1, 1],
     [0, 0, 1]]
]

SHAPES_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (0, 255, 255)]

# Game variables
board = [[0 for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
current_tetromino = None
current_tetromino_pos = (0, 0)
current_tetromino_color = None

# Functions
def draw_board():
    for y, row in enumerate(board):
        for x, color in enumerate(row):
            pygame.draw.rect(screen, SHAPES_COLORS[color - 1], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
            pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def new_tetromino():
    global current_tetromino, current_tetromino_pos, current_tetromino_color
    current_tetromino = random.choice(SHAPES)
    current_tetromino_pos = (SCREEN_WIDTH // BLOCK_SIZE // 2 - len(current_tetromino[0]) // 2, 0)
    current_tetromino_color = random.randint(1, len(SHAPES_COLORS))

def check_collision():
    for y, row in enumerate(current_tetromino):
        for x, cell in enumerate(row):
            if cell and (board[y + current_tetromino_pos[1]][x + current_tetromino_pos[0]] or x + current_tetromino_pos[0] < 0 or x + current_tetromino_pos[0] >= len(board[0]) or y + current_tetromino_pos[1] >= len(board)):
                return True
    return False

def merge_tetromino():
    for y, row in enumerate(current_tetromino):
        for x, cell in enumerate(row):
            if cell:
                board[y + current_tetromino_pos[1]][x + current_tetromino_pos[0]] = current_tetromino_color

def remove_completed_lines():
    global board
    new_board = [row for row in board if 0 not in row]
    num_removed_lines = len(board) - len(new_board)
    board = [[0 for _ in range(len(board[0]))] for _ in range(num_removed_lines)] + new_board

# Game loop
clock = pygame.time.Clock()
running = True

new_tetromino()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            current_tetromino_pos = (current_tetromino_pos[0] - 1, current_tetromino_pos[1])
            if check_collision():
                current_tetromino_pos = (current_tetromino_pos[0] + 1, current_tetromino_pos[1])
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            current_tetromino_pos = (current_tetromino_pos[0] + 1, current_tetromino_pos[1])
            if check_collision():
                current_tetromino_pos = (current_tetromino_pos[0] - 1, current_tetromino_pos[1])
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            current_tetromino_pos = (current_tetromino_pos[0], current_tetromino_pos[1] + 1)
            if check_collision():
                current_tetromino_pos = (current_tetromino_pos[0], current_tetromino_pos[1] - 1)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            rotated_tetromino = list(zip(*current_tetromino[::-1]))
            if not check_collision(rotated_tetromino=rotated_tetromino):
                current_tetromino = rotated_tetromino

    current_tetromino_pos = (current_tetromino_pos[0], current_tetromino_pos[1] + 1)
    if check_collision():
        current_tetromino_pos = (current_tetromino_pos[0], current_tetromino_pos[1] - 1)
        merge_tetromino()
        remove_completed_lines()
        new_tetromino()

    screen.fill(BLACK)
    draw_board()

    # Draw the current falling tetromino
    for y, row in enumerate(current_tetromino):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, SHAPES_COLORS[current_tetromino_color - 1],
                                 ((x + current_tetromino_pos[0]) * BLOCK_SIZE, (y + current_tetromino_pos[1]) * BLOCK_SIZE,
                                  BLOCK_SIZE, BLOCK_SIZE), 0)

    pygame.display.flip()
    clock.tick(5)

pygame.quit()
