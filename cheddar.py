import pygame
import random
import numpy as np
from numba import njit

# Initialize Pygame
pygame.init()

# Constants
SIZE = 4
TILE_SIZE = 100
MARGIN = 10
WIDTH = SIZE * TILE_SIZE + (SIZE + 1) * MARGIN
HEIGHT = WIDTH
FPS = 10  # Lower FPS for faster AI moves
FONT = pygame.font.SysFont("comicsansms", 32)

# Colors
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)

# Game variables
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Infinite AI")
clock = pygame.time.Clock()

frame_skip = 10  # Number of frames to skip for rendering
frame_counter = 0  # Frame counter

# Game Functions
def create_board():
    board = np.zeros((SIZE, SIZE), dtype=int)
    add_new_tile(board)
    add_new_tile(board)
    return board

def add_new_tile(board):
    empty_tiles = [(r, c) for r in range(SIZE) for c in range(SIZE) if board[r][c] == 0]
    if empty_tiles:
        r, c = random.choice(empty_tiles)
        board[r][c] = 2 if random.random() < 0.9 else 4

def draw_board(board):
    screen.fill(BLACK)
    for r in range(SIZE):
        for c in range(SIZE):
            value = board[r][c]
            color = GRAY if value == 0 else WHITE
            pygame.draw.rect(screen, color, 
                             (c * TILE_SIZE + (c + 1) * MARGIN, 
                              r * TILE_SIZE + (r + 1) * MARGIN, 
                              TILE_SIZE, TILE_SIZE))
            if value != 0:
                text = FONT.render(str(value), True, BLACK)
                screen.blit(text, 
                            (c * TILE_SIZE + (c + 1) * MARGIN + TILE_SIZE // 3, 
                             r * TILE_SIZE + (r + 1) * MARGIN + TILE_SIZE // 3))

def is_game_over(board):
    if any(0 in row for row in board):
        return False
    for r in range(SIZE):
        for c in range(SIZE):
            if r + 1 < SIZE and board[r][c] == board[r + 1][c]:
                return False
            if c + 1 < SIZE and board[r][c] == board[r][c + 1]:
                return False
    return True

@njit  # JIT compilation for speedup
def merge_left(board):
    for r in range(SIZE):
        tiles = [tile for tile in board[r] if tile != 0]
        i = 0
        while i < len(tiles) - 1:
            if tiles[i] == tiles[i + 1]:
                tiles[i] *= 2
                del tiles[i + 1]
            i += 1
        board[r, :len(tiles)] = tiles
        board[r, len(tiles):] = 0
    return board

def ai_move(board):
    global current_move
    old_board = board.copy()

    # AI makes moves in left, down, right, up order
    if AI_MOVES[current_move] == 0:  # Left
        board = merge_left(board)
    elif AI_MOVES[current_move] == 1:  # Down
        board = np.transpose(merge_left(np.transpose(board)))
    elif AI_MOVES[current_move] == 2:  # Right
        board = np.fliplr(merge_left(np.fliplr(board)))
    elif AI_MOVES[current_move] == 3:  # Up
        board = np.transpose(np.fliplr(merge_left(np.fliplr(np.transpose(board)))))
    
    if not np.array_equal(board, old_board):
        add_new_tile(board)

    current_move = (current_move + 1) % 4
    return board

# Simple AI: It will just go left, then down, then right, and up in a loop
AI_MOVES = [0, 1, 2, 3]  # left, down, right, up
current_move = 0

def main():
    global frame_counter
    running = True
    board = create_board()
    
    while running:
        for event in pygame.event.get():
            print(event)  # Print events for debugging
            if event.type == pygame.QUIT:
                running = False

        # AI makes a move
        board = ai_move(board)
        
        # Check for game over and restart if necessary
        if is_game_over(board):
            board = create_board()

        # Always render the board
        draw_board(board)
        pygame.display.flip()  # Update the display every frame

        frame_counter += 1

        # Frame rate control
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
