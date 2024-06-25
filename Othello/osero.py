import pygame
import sys

# グローバル変数
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)

# 初期化
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello")
FONT = pygame.font.SysFont("comicsans", 60)

# 盤面の初期化
def initialize_board():
    board = [[0] * COLS for _ in range(ROWS)]
    board[3][3] = board[4][4] = 1
    board[3][4] = board[4][3] = -1
    return board

# 盤面の描画
def draw_board(board):
    WIN.fill(GREEN)
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(WIN, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2)
            if board[row][col] == 1:
                pygame.draw.circle(WIN, BLACK, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
            elif board[row][col] == -1:
                pygame.draw.circle(WIN, WHITE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
    pygame.display.update()

# 駒を置ける位置をチェック
def is_valid_move(board, row, col, player):
    if board[row][col] != 0:
        return False
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]
    for d in directions:
        x, y = row + d[0], col + d[1]
        if 0 <= x < ROWS and 0 <= y < COLS and board[x][y] == -player:
            while 0 <= x < ROWS and 0 <= y < COLS and board[x][y] == -player:
                x, y = x + d[0], y + d[1]
            if 0 <= x < ROWS and 0 <= y < COLS and board[x][y] == player:
                return True
    return False

# 駒を置ける場所があるかチェック
def has_valid_moves(board, player):
    for row in range(ROWS):
        for col in range(COLS):
            if is_valid_move(board, row, col, player):
                return True
    return False

# 駒を置く
def place_piece(board, row, col, player):
    if is_valid_move(board, row, col, player):
        board[row][col] = player
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for d in directions:
            x, y = row + d[0], col + d[1]
            if 0 <= x < ROWS and 0 <= y < COLS and board[x][y] == -player:
                to_flip = []
                while 0 <= x < ROWS and 0 <= y < COLS and board[x][y] == -player:
                    to_flip.append((x, y))
                    x, y = x + d[0], y + d[1]
                if 0 <= x < ROWS and 0 <= y < COLS and board[x][y] == player:
                    for r, c in to_flip:
                        board[r][c] = player
        return True
    return False

# ゲームの状態をチェック
def check_game_over(board):
    if all(board[i][j] != 0 for i in range(ROWS) for j in range(COLS)):
        return True
    if not has_valid_moves(board, 1) and not has_valid_moves(board, -1):
        return True
    return False

# ゲームの結果を表示
def display_winner(board):
    black_count = sum(row.count(1) for row in board)
    white_count = sum(row.count(-1) for row in board)
    if black_count > white_count:
        text = FONT.render("Black Wins!", 1, BLACK)
    elif black_count < white_count:
        text = FONT.render("White Wins!", 1, WHITE)
    else:
        text = FONT.render("Draw!", 1, BLACK)
    WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)

# ゲームのメインループ
def main():
    board = initialize_board()
    player = 1
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
                if place_piece(board, row, col, player):
                    player *= -1

            if check_game_over(board):
                game_over = True

        draw_board(board)

        # ターンをスキップするロジック
        if not has_valid_moves(board, player):
            player *= -1
            if not has_valid_moves(board, player):
                game_over = True

    display_winner(board)
    main()  # ゲームの再開

if __name__ == "__main__":
    main()
