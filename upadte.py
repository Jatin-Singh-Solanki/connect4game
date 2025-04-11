import numpy as np
import pygame
import sys
import math

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

row_count = 6
col_count = 7

SQUARESIZE = 100
width = col_count * SQUARESIZE
height = (row_count + 1) * SQUARESIZE
size = (width, height)
radius = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect Four - Jatin Singh Solanki")

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
    for c in range(col_count - 3):
        for r in range(row_count):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    for c in range(col_count):
        for r in range(row_count - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    for c in range(col_count - 3):
        for r in range(row_count - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    for c in range(col_count - 3):
        for r in range(3, row_count):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def draw_board(board):
    for c in range(col_count):
        for r in range(row_count):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE/2)+SQUARESIZE), radius)

    for c in range(col_count):
        for r in range(row_count):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), radius)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), radius)

    pygame.display.update()

pygame.init()
myfont = pygame.font.SysFont("monospace", 75)

board = create_board()
print_board(board)
game_over = False
turn = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                board = create_board()
                print_board(board)
                draw_board(board)
                game_over = False
                turn = 0
            continue

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
            col = int(math.floor(posx/SQUARESIZE))

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1 if turn == 0 else 2)

                if winning_move(board, 1 if turn == 0 else 2):
                    winner = "Player 1" if turn == 0 else "Player 2"
                    label = myfont.render(f"{winner} wins!", 1, RED if turn == 0 else YELLOW)
                    screen.blit(label, (40, 10))
                    pygame.display.update()
                    game_over = True
                    label2 = myfont.render("Press ENTER to restart", 1, BLUE)
                    screen.blit(label2, (40, 80))
                    pygame.display.update()

                turn += 1
                turn = turn % 2
                print_board(board)
                draw_board(board)