import pygame
import sys
import copy
from pygame import mixer
from pygame.locals import *

# グローバル変数
WIDTH, HEIGHT = 700, 700
WIDTH_FIELD = 1320
ROWS, COLS = 9, 9
SQUARE_SIZE = WIDTH // COLS
WIDTH1 = 30 ##横外側の幅
WIDTH2 = 30 ##横持ち駒置き場と将棋盤の間の幅

HEIGHT1 = 50 ##縦外側の幅1


ROWS_HAVE, COLS_HAVE = 5, 4
SQUARE_SIZE_HAVE = 63
WIDTH_HAVE, HEIGHT_HAVE = SQUARE_SIZE_HAVE * COLS_HAVE, SQUARE_SIZE_HAVE * ROWS_HAVE


COL_SETUP = -145 #将棋盤上の駒の位置ズレを調整する
ROW_SETUP = -35

BROWN = (244, 164, 96)
BLACK = (0, 0, 0)
DARK_RED = (20, 5, 5)
WHITE = (255, 255, 255)
BEIJE = (210, 160, 130)
RED = (250, 5, 0)
BLUE = (80, 80, 170)
# pressed_keys = pygame.key.get_pressed()

# 初期化
pygame.init()
WIN = pygame.display.set_mode((WIDTH_FIELD, 800))
pygame.display.set_caption("将棋しよう！")
FONT = pygame.font.SysFont("こころ明朝体", 60)
FONT1 = pygame.font.SysFont("こころ明朝体", 50)

class Button:
    def __init__(self, pos, size, pad, color, txtcolor, text="Button"):
        self.x = pos[0]
        self.y = pos[1]
        self.pad = pad
        self.color = color
        self.font = pygame.font.SysFont("こころ明朝体", size)
        self.yes_text = self.font.render(text[0], True, txtcolor)
        self.no_text = self.font.render(text[1], True, txtcolor)
        self.button = pygame.Rect(pos, (self.yes_text.get_width() + pad, self.yes_text.get_height() + pad))
        # self.button_bottom = pygame.Rect(pos, (self.button.width, self.button.height + 5))
        self.yes_button = pygame.Rect(pos, (self.button.width, self.button.height + 5))
        self.no_button = pygame.Rect((pos[0]+200,pos[1]), (self.button.width+100, self.button.height + 5))
    
        self.clicked_function = None

    def update(self):
        self.button.top = self.y

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.yes_button.collidepoint(event.pos):
                    self.yes_button.top += 2
                    print(u"ボタンが押されました")
                    return 1
                if self.no_button.collidepoint(event.pos):
                    self.no_button.top += 2
                    print(u"ボタンが押されました")
                    return 2

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.yes_button)
        pygame.draw.rect(screen, self.color, self.no_button)
        screen.blit(self.yes_text, (self.x + self.pad / 2, self.y + self.pad / 2))
        screen.blit(self.no_text, (self.x + self.pad / 2+200, self.y + self.pad / 2))
# 盤面の初期化
def initialize_board():
    board = [["香2","桂2","銀2","金2","玉2","金2","銀2","桂2","香2"],
             ["　","飛2","　","　","　","　","　","角2","　"],
             ["歩2","歩2","歩2","歩2","歩2","歩2","歩2","歩2","歩2"],
             ["　","　","　","　","　","　","　","　","　"],
             ["　","  ","　","　","　","　","　","　","　"],
             ["　","　","　","　","　","　","　","　","　"],
             ["歩1","歩1","歩1","歩1","歩1","歩1","歩1","歩1","歩1"],
             ["　","角1","　","　","　","　","　","飛1","　"],
             ["香1","桂1","銀1","金1","王1","金1","銀1","桂1","香1"]]
    return board

def readToDisplay_img(piece):
    if piece[:-1] == "歩":
        img_piece = pygame.image.load("koma_hu.png")
    if piece[:-1] == "角":
        img_piece = pygame.image.load("koma_kaku.png")
    if piece[:-1] == "飛":
        img_piece = pygame.image.load("koma_hisya.png")
    if piece[:-1] == "香":
        img_piece = pygame.image.load("koma_kyosya.png")
    if piece[:-1] == "桂":
        img_piece = pygame.image.load("koma_keima.png")
    if piece[:-1] == "金":
        img_piece = pygame.image.load("koma_kin.png")
    if piece[:-1] == "銀":
        img_piece = pygame.image.load("koma_gin.png")
    if piece[:-1] == "王":
        img_piece = pygame.image.load("koma_ou.png")
    if piece[:-1] == "玉":
        img_piece = pygame.image.load("koma_gyoku.png")
    if piece[:-1] == "と":
        img_piece = pygame.image.load("koma_to.png")
    if piece[:-1] in ["(銀)", "(香)", "(桂)"]:
        img_piece = pygame.image.load("koma_narikin.png")
    if piece[:-1] == "馬":
        img_piece = pygame.image.load("koma_narikaku.png")
    if piece[:-1] == "龍":
        img_piece = pygame.image.load("koma_ryu.png")

    return img_piece


# 盤面の描画
def draw_board(board, text, selected_row, selected_col, having, possible_moves, whosturn, mode): #mode=1は将棋盤をタッチしているとき、mode=2は持ち駒置き場をタッチしているとき。 
    WIN.fill(DARK_RED)
    img = pygame.image.load("syogi_backart.png")
    WIN.blit(img,(0, 0)) 

    img = pygame.image.load("syogiban.png")
    WIN.blit(img,(WIDTH1 + WIDTH2 + SQUARE_SIZE_HAVE + COLS_HAVE + 175, HEIGHT1 - 13)) 

    a, b, a1, b1= 0, 0, 0, 0
    # text = text_surface.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2))
    # WIN.blit(text_surface, text)
    for row in range(ROWS):
        for col in range(COLS):
            if (row + col) % 2 == 0:
                pygame.draw.rect(WIN, BROWN, (WIDTH_HAVE + WIDTH1 + WIDTH2 + (col * SQUARE_SIZE), HEIGHT1 + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            else:
                pygame.draw.rect(WIN, BEIJE, (WIDTH_HAVE + WIDTH1 + WIDTH2 + (col * SQUARE_SIZE), HEIGHT1 + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if mode == 1 and selected_row != 100 and selected_col != 100:
                pygame.draw.rect(WIN, WHITE, (WIDTH_HAVE + WIDTH1 + WIDTH2 + (selected_col * SQUARE_SIZE), HEIGHT1 + selected_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if mode == 1 and possible_moves != "" and a1 != "" and b1 != "":
                for i in range(len(possible_moves)):
                    a1,b1 = possible_moves[i]
                    pygame.draw.rect(WIN, BLUE, (WIDTH_HAVE + WIDTH1 + WIDTH2 + (b1 * SQUARE_SIZE), HEIGHT1 + a1 * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(WIN, BLACK, (WIDTH_HAVE + WIDTH1 + WIDTH2 + (col * SQUARE_SIZE), HEIGHT1 + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
            piece = board[row][col]
            # 自分の駒と相手の駒を区別し、180°回転させる
            if piece != "　":
                if piece[-1] == "1":  # 自分の駒
                    piece_surface = readToDisplay_img(piece)
                    WIN.blit(piece_surface,(WIDTH_HAVE + WIDTH1 + WIDTH2 + col * SQUARE_SIZE + SQUARE_SIZE + COL_SETUP // 2 ,HEIGHT1 + row * SQUARE_SIZE + SQUARE_SIZE // 2 + ROW_SETUP))
                elif piece[-1] == "2":  # 相手の駒
                    piece_surface = readToDisplay_img(piece)
                    piece_surface = pygame.transform.flip(piece_surface, True, True)  
                    WIN.blit(piece_surface,(WIDTH_HAVE + WIDTH1 + WIDTH2 + col * SQUARE_SIZE + SQUARE_SIZE + COL_SETUP // 2 ,HEIGHT1 + row * SQUARE_SIZE + SQUARE_SIZE // 2 + ROW_SETUP)) 
    
    #持ち駒エリアの表示
    field_surface = pygame.image.load("mochigomaoki.png")  
    WIN.blit(field_surface,(WIDTH + WIDTH_HAVE + WIDTH1 + WIDTH2*2 - 17, HEIGHT + HEIGHT1 - (HEIGHT_HAVE) - 10)) 
    field_surface = pygame.transform.flip(field_surface, True, True)
    WIN.blit(field_surface,(WIDTH1-10, HEIGHT1-60))

    for row in range(ROWS_HAVE):
        for col in range(COLS_HAVE):
            #自分の持ち駒置き場
            if (row + col) % 2 == 0:
                pygame.draw.rect(WIN, BROWN, (WIDTH1 + WIDTH2*2 + WIDTH_HAVE + (col * SQUARE_SIZE_HAVE) + COLS * SQUARE_SIZE, HEIGHT1 + HEIGHT - HEIGHT_HAVE + (row * SQUARE_SIZE_HAVE), SQUARE_SIZE_HAVE, SQUARE_SIZE_HAVE))
                pygame.draw.rect(WIN, BROWN, (WIDTH1 + col * SQUARE_SIZE_HAVE, HEIGHT1 + row * SQUARE_SIZE_HAVE, SQUARE_SIZE_HAVE, SQUARE_SIZE_HAVE))#相手
    if mode == 2: 
        pygame.draw.rect(WIN, WHITE, (WIDTH1 + WIDTH2*2 + WIDTH_HAVE + (selected_col * SQUARE_SIZE_HAVE) + COLS * SQUARE_SIZE, HEIGHT1 + HEIGHT - HEIGHT_HAVE + (selected_row * SQUARE_SIZE_HAVE), SQUARE_SIZE_HAVE, SQUARE_SIZE_HAVE))
        pygame.draw.rect(WIN, WHITE, (WIDTH1 + selected_col * SQUARE_SIZE_HAVE, HEIGHT1 + selected_row * SQUARE_SIZE_HAVE, SQUARE_SIZE_HAVE, SQUARE_SIZE_HAVE))#相手
                
    #持ち駒の表示
    for i in range(len(having)):
        if having[i][-1] == "2":##相手がとったとき
            piece_surface = readToDisplay_img(having[i])
            piece_surface = pygame.transform.flip(piece_surface, True, True)
            WIN.blit(piece_surface,(WIDTH1 + SQUARE_SIZE_HAVE * (COLS_HAVE-1) - (a%COLS_HAVE) * SQUARE_SIZE_HAVE, HEIGHT1 - ((b-(b%COLS_HAVE))/COLS_HAVE * SQUARE_SIZE_HAVE) + SQUARE_SIZE_HAVE * (ROWS_HAVE-1)))
            a += 1
        elif having[i][-1] == "1":##自分がとったとき
            piece_surface = readToDisplay_img(having[i])
            WIN.blit(piece_surface, (WIDTH_HAVE + WIDTH1 + WIDTH2*2 + ((b%COLS_HAVE) * SQUARE_SIZE_HAVE) + COLS * SQUARE_SIZE, HEIGHT1 + HEIGHT - HEIGHT_HAVE + ((b-(b%COLS_HAVE))/COLS_HAVE * SQUARE_SIZE_HAVE)))
            b += 1
    
    # ターンを教える表示
    font = pygame.font.SysFont("こころ明朝体",40)
    text = font.render("あなたのターンです", True, BLACK)
    if whosturn == 2:  # 相手側の駒
        text = pygame.transform.flip(text, True, True)  # 上下反転
        WIN.blit(text,(WIDTH_FIELD / 2 - 160, 0))
    else:
        WIN.blit(text,(WIDTH_FIELD / 2 -160, HEIGHT +60))

    pygame.display.update()


# 駒の移動可能な位置を計算する関数
def get_possible_moves(board, row, col, whosturn):
    possible_moves = []
    piece = board[row][col]
    U = 1

    if whosturn == 2:
        U = -1
    
############################↓################################   
    # 歩の移動方向
    if piece[:-1] == "歩":
        if board[row - U][col] == "　":
            possible_moves.append((row - U, col))
        elif board[row - U][col] != "　":
            if board[row - U][col][-1] != piece[-1]:
                possible_moves.append((row - U, col))
    
    # 飛車の移動方向
    if piece[:-1] == "飛":
        # 上方向
        for r in range(row - 1, -1, -1):
            if board[r][col] == "　":
                possible_moves.append((r, col))
            elif board[r][col][-1] == piece[-1]:
                break
            else:
                possible_moves.append((r, col))
                break
        # 下方向
        for r in range(row + 1, ROWS):
            if board[r][col] == "　":
                possible_moves.append((r, col))
            elif board[r][col][-1] == piece[-1]:
                break
            else:
                possible_moves.append((r, col))
                break
        # 左方向
        for c in range(col - 1, -1, -1):
            if board[row][c] == "　":
                possible_moves.append((row, c))
            elif board[row][c][-1] == piece[-1]:
                break
            else:
                possible_moves.append((row, c))
                break
        # 右方向
        for c in range(col + 1, COLS):
            if board[row][c] == "　":
                possible_moves.append((row, c))
            elif board[row][c][-1] == piece[-1]:
                break
            else:
                possible_moves.append((row, c))
                break
    
    # 角の移動方向
    if piece[:-1] == "角":
        # 左上方向
        r, c = row - 1, col - 1
        while r >= 0 and c >= 0:
            if board[r][c] == "　":
                possible_moves.append((r, c))
            elif board[r][c][-1] == piece[-1]:
                break
            else:
                possible_moves.append((r, c))
                break
            r -= 1
            c -= 1
        # 右上方向
        r, c = row - 1, col + 1
        while r >= 0 and c < COLS:
            if board[r][c] == "　":
                possible_moves.append((r, c))
            elif board[r][c][-1] == piece[-1]:
                break
            else:
                possible_moves.append((r, c))
                break
            r -= 1
            c += 1
        # 左下方向
        r, c = row + 1, col - 1
        while r < ROWS and c >= 0:
            if board[r][c] == "　":
                possible_moves.append((r, c))
            elif board[r][c][-1] == piece[-1]:
                break
            else:
                possible_moves.append((r, c))
                break
            r += 1
            c -= 1
        # 右下方向
        r, c = row + 1, col + 1
        while r < ROWS and c < COLS:
            if board[r][c] == "　":
                possible_moves.append((r, c))
            elif board[r][c][-1] == piece[-1]:
                break
            else:
                possible_moves.append((r, c))
                break
            r += 1
            c += 1

    # 桂馬の移動方向
    if piece[:-1] == "桂":
        # 上方向
            if col > 0 and board[row - 2*U][col - 1] == "　" or  col > 0 and board[row - 2*U][col - 1] != "　" and board[row - 2*U][col - 1][-1] != piece[-1]:
                possible_moves.append((row - 2*U, col - 1))
            if col < COLS - 1 and board[row - 2*U][col + 1] == "　" or col < COLS - 1 and board[row - 2*U][col + 1] != "　" and board[row - 2*U][col + 1][-1] != piece[-1]:
                possible_moves.append((row - 2*U, col + 1))

    # 香車の移動方向
    if piece[:-1] == "香":
        # 上方向
        for r in range(row - U, -1, -1):
            if board[r][col] == "　":
                possible_moves.append((r, col))
            elif board[r][col][-1] == piece[-1]:
                break
            else:
                possible_moves.append((r, col))
                break

    # 金の移動方向
    if piece[:-1] in ["金", "と", "(銀)", "(香)", "(桂)"]:
        # 上方向
        if row > 0 and board[row - U][col] == "　":
            possible_moves.append((row - U, col))
        elif row > 0 and board[row - U][col][-1] != piece[-1]:
            possible_moves.append((row - U, col))
        # 左上方向
        if row > 0 and col > 0 and board[row - U][col - 1] == "　":
            possible_moves.append((row - U, col - 1))
        elif row > 0 and col > 0 and board[row - U][col - 1][-1] != piece[-1]:
            possible_moves.append((row - U, col - 1))
        # 右上方向
        if row > 0 and col < COLS - 1 and board[row - U][col + 1] == "　":
            possible_moves.append((row - U, col + 1))
        elif row > 0 and col > 0 and board[row - U][col + 1][-1] != piece[-1]:
            possible_moves.append((row - U, col + 1))
        # 下方向
        if row < ROWS - 1 and board[row + U][col] == "　":
            possible_moves.append((row + U, col))
        elif row < ROWS - 1 and board[row + U][col][-1] != piece[-1]:
            possible_moves.append((row + U, col))
        # 左方向
        if col > 0 and board[row][col - 1] == "　":
            possible_moves.append((row, col - 1))
        elif col > 0 and board[row][col - 1] != piece[-1]:
            possible_moves.append((row, col - 1))
        # 右方向
        if col < COLS - 1 and board[row][col + 1] == "　":
            possible_moves.append((row, col + 1))
        elif col < COLS - 1 and board[row][col + 1] != piece[-1]:
            possible_moves.append((row, col + 1))

    # 銀の移動方向
    if piece[:-1] == "銀":
        # 上方向
        if row > 0 and board[row - U][col] == "　":
            possible_moves.append((row - U, col))
        elif row > 0 and board[row - U][col][-1] != piece[-1]:
            possible_moves.append((row - U, col))
        # 左上方向
        if row > 0 and col > 0 and board[row - U][col - 1] == "　":
            possible_moves.append((row - U, col - 1))
        elif row > 0 and col > 0 and board[row - U][col - 1][-1] != piece[-1]:
            possible_moves.append((row - U, col - 1))
        # 右上方向
        if row > 0 and col < COLS - 1 and board[row - U][col + 1] == "　":
            possible_moves.append((row - U, col + 1))
        elif row > 0 and col > 0 and board[row - U][col + 1][-1] != piece[-1]:
            possible_moves.append((row - U, col + 1))
        # 左下方向
        if row < ROWS - 1 and col > 0 and board[row + U][col - 1] == "　":
            possible_moves.append((row + U, col - 1))
        elif row < ROWS - 1 and col > 0 and board[row + U][col - 1][-1] != piece[-1]:
            possible_moves.append((row + U, col - 1))
        # 右下方向
        if row < ROWS - 1 and col < COLS - 1 and board[row + U][col + 1] == "　":
            possible_moves.append((row + U, col + 1))
        elif row < ROWS - 1 and col < COLS - 1 and board[row + U][col + 1][-1] != piece[-1]:
            possible_moves.append((row + U, col + 1))
    
    # 王（玉）の移動方向
    if piece[:-1] in ["王", "玉"]:
        # 上方向
        if row > 0 and board[row - U][col] == "　":
            possible_moves.append((row - U, col))
        elif row > 0 and board[row - U][col][-1] != piece[-1]:
            possible_moves.append((row - U, col))
        # 左上方向
        if row > 0 and col > 0 and board[row - U][col - 1] == "　":
            possible_moves.append((row - U, col - 1))
        elif row > 0 and col > 0 and board[row - U][col - 1][-1] != piece[-1]:
            possible_moves.append((row - U, col - 1))
        # 右上方向
        if row > 0 and col < COLS - 1 and board[row - U][col + 1] == "　":
            possible_moves.append((row - U, col + 1))
        elif row > 0 and col > 0 and board[row - U][col + 1][-1] != piece[-1]:
            possible_moves.append((row - U, col + 1))
        # 下方向
        if row < ROWS - 1 and board[row + U][col] == "　":
            possible_moves.append((row + U, col))
        elif row < ROWS - 1 and board[row + U][col][-1] != piece[-1]:
            possible_moves.append((row + U, col))
        # 左方向
        if col > 0 and board[row][col - 1] == "　":
            possible_moves.append((row, col - 1))
        elif col > 0 and board[row][col - 1] != piece[-1]:
            possible_moves.append((row, col - 1))
        # 右方向
        if col < COLS - 1 and board[row][col + 1] == "　":
            possible_moves.append((row, col + 1))
        elif col < COLS - 1 and board[row][col + 1] != piece[-1]:
            possible_moves.append((row, col + 1))
        # 左下方向
        if row < ROWS - 1 and col > 0 and board[row + U][col - 1] == "　":
            possible_moves.append((row + U, col - 1))
        elif row < ROWS - 1 and col > 0 and board[row + U][col - 1][-1] != piece[-1]:
            possible_moves.append((row + U, col - 1))
        # 右下方向
        if row < ROWS - 1 and col < COLS - 1 and board[row + U][col + 1] == "　":
            possible_moves.append((row + U, col + 1))
        elif row < ROWS - 1 and col < COLS - 1 and board[row + U][col + 1][-1] != piece[-1]:
            possible_moves.append((row + U, col + 1))

    # 竜の移動方向
    if piece[:-1] == "竜":
        # 上方向
        for r in range(row - 1, -1, -1):
            if board[r][col] == "　":
                possible_moves.append((r, col))
            elif board[r][col][-1] == piece[-1]:
                break
            else:
                possible_moves.append((r, col))
                break
        # 下方向
        for r in range(row + 1, ROWS):
            if board[r][col] == "　":
                possible_moves.append((r, col))
            elif board[r][col][-1] == piece[-1]:
                break
            else:
                possible_moves.append((r, col))
                break
        # 左方向
        for c in range(col - 1, -1, -1):
            if board[row][c] == "　":
                possible_moves.append((row, c))
            elif board[row][c][-1] == piece[-1]:
                break
            else:
                possible_moves.append((row, c))
                break
        # 右方向
        for c in range(col + 1, COLS):
            if board[row][c] == "　":
                possible_moves.append((row, c))
            elif board[row][c][-1] == piece[-1]:
                break
            else:
                possible_moves.append((row, c))
                break
        # 左上方向
        if row > 0 and col > 0 and board[row - U][col - 1] == "　":
            possible_moves.append((row - U, col - 1))
        elif row > 0 and col > 0 and board[row - U][col - 1][-1] != piece[-1]:
            possible_moves.append((row - U, col - 1))
        # 右上方向
        if row > 0 and col < COLS - 1 and board[row - U][col + 1] == "　":
            possible_moves.append((row - U, col + 1))
        elif row > 0 and col > 0 and board[row - U][col + 1][-1] != piece[-1]:
            possible_moves.append((row - U, col + 1))
        # 左下方向
        if row < ROWS - 1 and col > 0 and board[row + U][col - 1] == "　":
            possible_moves.append((row + U, col - 1))
        elif row < ROWS - 1 and col > 0 and board[row + U][col - 1][-1] != piece[-1]:
            possible_moves.append((row + U, col - 1))
        # 右下方向
        if row < ROWS - 1 and col < COLS - 1 and board[row + U][col + 1] == "　":
            possible_moves.append((row + U, col + 1))
        elif row < ROWS - 1 and col < COLS - 1 and board[row + U][col + 1][-1] != piece[-1]:
            possible_moves.append((row + U, col + 1))

    # 馬の移動方向
    if piece[:-1] == "馬":
        # 左上方向
        r, c = row - 1, col - 1
        while r >= 0 and c >= 0:
            if board[r][c] == "　":
                possible_moves.append((r, c))
            elif board[r][c][-1] == piece[-1]:
                break
            else:
                possible_moves.append((r, c))
                break
            r -= 1
            c -= 1
        # 右上方向
        r, c = row - 1, col + 1
        while r >= 0 and c < COLS:
            if board[r][c] == "　":
                possible_moves.append((r, c))
            elif board[r][c][-1] == piece[-1]:
                break
            else:
                possible_moves.append((r, c))
                break
            r -= 1
            c += 1
        # 左下方向
        r, c = row + 1, col - 1
        while r < ROWS and c >= 0:
            if board[r][c] == "　":
                possible_moves.append((r, c))
            elif board[r][c][-1] == piece[-1]:
                break
            else:
                possible_moves.append((r, c))
                break
            r += 1
            c -= 1
        # 右下方向
        r, c = row + 1, col + 1
        while r < ROWS and c < COLS:
            if board[r][c] == "　":
                possible_moves.append((r, c))
            elif board[r][c][-1] == piece[-1]:
                break
            else:
                possible_moves.append((r, c))
                break
            r += 1
            c += 1
        # 上方向
        if row > 0 and board[row - U][col] == "　":
            possible_moves.append((row - U, col))
        elif row > 0 and board[row - U][col][-1] != piece[-1]:
            possible_moves.append((row - U, col))
        # 下方向
        if row < ROWS - 1 and board[row + U][col] == "　":
            possible_moves.append((row + U, col))
        elif row < ROWS - 1 and board[row + U][col][-1] != piece[-1]:
            possible_moves.append((row + U, col))
        # 左方向
        if col > 0 and board[row][col - 1] == "　":
            possible_moves.append((row, col - 1))
        elif col > 0 and board[row][col - 1] != piece[-1]:
            possible_moves.append((row, col - 1))
        # 右方向
        if col < COLS - 1 and board[row][col + 1] == "　":
            possible_moves.append((row, col + 1))
        elif col < COLS - 1 and board[row][col + 1] != piece[-1]:
            possible_moves.append((row, col + 1))

    

    return possible_moves
#############################↑###############################
def yes():
    print("yes")
    return 1
def no():
    print("No")
    return 2
    

def nari(board, row, col):
    if board[row][col][:-1] == "歩":
        narikoma = "と"
        
    if board[row][col][:-1] == "角":
        narikoma = "馬"
    if board[row][col][:-1] == "飛":
        narikoma = "龍"
    if board[row][col][:-1] == "桂":
        narikoma = "(桂)"
    if board[row][col][:-1] == "香":
        narikoma = "(香)"
    return  narikoma + board[row][col][-1]



def get_having(board, row, col, having):
    if board[row][col][-1] == "2":#取られたコマ番号が2の場合#
        having.append(board[row][col][:-1] + "1")
    else:#取られたコマ番号が1の場合#
        having.append(board[row][col][:-1] + "2")
    return having

def search_piece(having):
    for i in range(len(having)):
        if having[i][:-1] == "王":
            print("player2の勝ち")
        elif having[i][:-1] == "玉":
            print("player1の勝ち")

def get_having_sep(having):
    # 4次元のリストを初期化
    having_sep = [[[[], [], []],[[], [], []],[[], [], []]],[[[], [], []],[[], [], []],[[], [], []]],[[[], [], []],[[], [], []],[[], [], []]]]
    a, b = 0, 0
    for i in having:
        if having[-1] == "2":
            having_sep[2][int((a - (a % COLS_HAVE)) / COLS_HAVE)][int(a % COLS_HAVE)].append(i)
            a += 1
        else:
            having_sep[1][int((b - (b % COLS_HAVE)) / COLS_HAVE)][int(b % COLS_HAVE)].append(i)
            b += 1
            
    return having_sep

                

# ゲームのメインループ
def main():
    
    board = initialize_board()
    board_backup = copy.deepcopy(board)
    selected_piece = None
    possible_moves = []
    having = []
    having_backup = copy.deepcopy(having)
    whosturn = 1
    narihantei = 0
    mode = 0
    while True:
        print(whosturn)
        a = 0
        row, col = 100, 100
        while a == 0:#ターン切り替え
            b = 0
            text = ""
            while b == 0:#画面表示のループ
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    pygame.event.pump()
                    pressed_keys = pygame.key.get_pressed()
                    #下キーを押して一手戻る
                    if pressed_keys[pygame.K_DOWN]:
                        b = 1
                        if board != board_backup:
                            board = copy.deepcopy(board_backup)
                            having = copy.deepcopy(having_backup)
                            a = 1
                            print("一手戻しました")
                        

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        b = 1
                        x, y = event.pos
                        if x >= WIDTH_HAVE + WIDTH1 + WIDTH2 and x <= WIDTH_HAVE + WIDTH1 + WIDTH2 + WIDTH and y >= HEIGHT1 and y <= HEIGHT1 + HEIGHT:
                            col = (x - WIDTH_HAVE - WIDTH1 - WIDTH2 ) // SQUARE_SIZE
                            row = (y-HEIGHT1) // SQUARE_SIZE
                            mode = int(1)
                            if possible_moves == []:
                                if board[row][col] != "　":  # 選択したマスに駒がある場合
                                    if str(board[row][col][-1]) != str(whosturn):
                                        print("自分の駒を選んでください")
                                    else:
                                        selected_piece = (row, col)
                                        possible_moves = get_possible_moves(board, row, col, whosturn)
                                        
                                        if possible_moves == []:
                                            text = "この駒は移動できるマスがありません"
                            else:
                                if (row, col) in possible_moves:  # 移動可能なマスをタッチした場合
                                    hit_sound = pygame.mixer.Sound("将棋の駒を打つ.mp3")
                                    hit_sound.play()  # サウンドを再生
                                    # 駒を移動させる処理を追加する
                                    if board[row][col] != "　":
                                        having_backup = copy.deepcopy(having)
                                        having = get_having(board, row, col, having)
                                        print(having)
                                    board_backup = copy.deepcopy(board)
                                    board[selected_piece[0]][selected_piece[1]], board[row][col] = "　", board[selected_piece[0]][selected_piece[1]]
                                    #なり領域にはいったとき、なり領域から動くとき選択
                                    if whosturn == 2 and row >= 6 and board[row][col][:-1] in ["歩", "角", "飛", "香", "桂"] or whosturn == 2 and selected_piece[0] >= 6 and board[row][col][:-1] in ["歩", "角", "飛", "香", "桂"] :
                                            narihantei = 2
                                    elif whosturn == 1 and row <= 2 and  board[row][col][:-1] in ["歩", "角", "飛", "香", "桂"] or whosturn == 1 and selected_piece[0] <= 2 and  board[row][col][:-1] in ["歩", "角", "飛", "香", "桂"]:
                                            narihantei = 1
                                    while narihantei != 0:
                                        img = pygame.image.load("narimasuka.png")
                                        WIN.blit(img,(0, 0))
                                        font = pygame.font.SysFont("こころ明朝体",40)
                                        text = font.render("成りますか？", True, BLACK)
                                        yesno_button = Button((200, 200), 32, 16, (255, 0, 0), (255, 255, 255), text=("はい","いいえ"))#narihantei=1を返すボタン
                                        yesno_button.clicked_function = yes
        
                                        nari_select = yesno_button.update()
                                        
                                        yesno_button.draw(WIN)
                                        pygame.display.flip()
                                        
                                        if nari_select == 1:
                                            if narihantei == 1:
                                                board[row][col] = nari(board, row, col)
                                            if narihantei == 2:
                                                board[row][col] = nari(board, row, col)
                                            narihantei = 0
                                        elif nari_select == 2:
                                            narihantei = 0

                                    selected_piece = None
                                    narihantei = 0
                                    possible_moves = []
                                    a = 1
                                    search_piece(having)

                                elif board[row][col] != "　":
                                    if str(board[row][col][-1]) == str(whosturn):#動かす駒を選択し直した時
                                        selected_piece = (row, col)
                                        possible_moves = get_possible_moves(board, row, col, whosturn)

                        elif whosturn == 1 and x >= WIDTH1 + WIDTH2*2 + WIDTH + WIDTH_HAVE and x <= WIDTH1 + WIDTH2*2 + WIDTH + WIDTH_HAVE*2 and y >= HEIGHT1 + HEIGHT - HEIGHT_HAVE and y <= HEIGHT1 + HEIGHT  or  whosturn == 2 and x >= WIDTH1 and x <= WIDTH_HAVE + WIDTH1 and y >= HEIGHT1 and y <= HEIGHT1 + HEIGHT_HAVE:
                            
                            if whosturn == 1 : #自分持ち駒置き場のタッチ判定
                                col = (x - (WIDTH1 + WIDTH2*2 + WIDTH + WIDTH_HAVE)) // SQUARE_SIZE_HAVE
                                row = (y - (HEIGHT1 + HEIGHT - HEIGHT_HAVE)) // SQUARE_SIZE_HAVE

                            elif whosturn == 2 : #相手持ち駒置き場のタッチ判定
                                col = (x - WIDTH1) // SQUARE_SIZE_HAVE
                                row = (y - HEIGHT1) // SQUARE_SIZE_HAVE
                            selected_piece_have = (row,col)
                            mode = int(2)

                            having_sep = get_having_sep(having)
                            while mode == 2:
                                 print("ppppppp")
                                 if event.type == pygame.MOUSEBUTTONDOWN:
                                    x, y = event.pos
                                    print("jjjjj")

                                    if (x >= WIDTH_HAVE + WIDTH1 + WIDTH2 and y>= HEIGHT1):
                                        col = (x - WIDTH_HAVE - WIDTH1 - WIDTH2 ) // SQUARE_SIZE
                                        row = (y-HEIGHT1) // SQUARE_SIZE
                                        board[row][col] = having_sep[whosturn][selected_piece_have[0]][selected_piece_have[1]].pop()
                                        print("dadadad")
                                        x, y = 0, 0
                                        mode = 0


                                    

                        
                        
                        

                                
                                



                draw_board(board, text, row, col, having, possible_moves, whosturn, mode)
        if whosturn == 1:
            whosturn = 2
        else:
            whosturn = 1

if __name__ == "__main__":
    main()
