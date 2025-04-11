import numpy as np
import pygame
import sys
import math

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Board dimensions
row_count = 6
col_count = 7

# Initialize board
def create_board():
    board = np.zeros((row_count, col_count))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[row_count - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(row_count):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Horizontal
    for c in range(col_count - 3):
        for r in range(row_count):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    # Vertical
    for c in range(col_count):
        for r in range(row_count - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    # Positive diagonal
    for c in range(col_count - 3):
        for r in range(row_count - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    # Negative diagonal
    for c in range(col_count - 3):
        for r in range(3, row_count):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True

# Initialize pygame
pygame.init()

# Define screen size
SQUARESIZE = 100
width = col_count * SQUARESIZE
height = (row_count + 1) * SQUARESIZE
size = (width, height)
radius = int(SQUARESIZE / 2 - 5)

# Set up display
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect Four - Jatin Singh Solanki")
myfont = pygame.font.SysFont("monospace", 75)

def draw_board(board):
    for c in range(col_count):
        for r in range(row_count):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), radius)

    for c in range(col_count):
        for r in range(row_count):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE + SQUARESIZE/2), height - int(r*SQUARESIZE + SQUARESIZE/2)), radius)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE + SQUARESIZE/2), height - int(r*SQUARESIZE + SQUARESIZE/2)), radius)

    pygame.display.update()

# Game setup
board = create_board()
print_board(board)
game_over = False
turn = 0

draw_board(board)

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), radius)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), radius)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            col = int(math.floor(posx / SQUARESIZE))

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1 if turn == 0 else 2)

                if winning_move(board, 1 if turn == 0 else 2):
                    label = myfont.render(f"Player {turn + 1} wins!", 1, RED if turn == 0 else YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

                print_board(board)
                draw_board(board)

                turn = (turn + 1) % 2

                if game_over:
                    pygame.time.wait(3000)
