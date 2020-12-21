import pygame
from pygame.locals import *
import re
import numpy as np


class Point:
    row = 0
    col = 0
    def __init__(self,row,col):
        self.row = row
        self.col = col
    def copy(self):
        return Point(self.row,self.col)

score_map = {
        "01": 17,#眠1连
        "001": 17,#眠1连
        "0001": 17,#眠1连
        
        "0102":17,#眠1连，15
        "0012":15,#眠1连，15
        "01002":19,#眠1连，15
        "00102":17,#眠1连，15
        "00012":15,#眠1连，15

        "01000":21,#活1连，15
        "00100":19,#活1连，15
        "00010":17,#活1连，15
        "00001":15,#活1连，15

        #被堵住
        "0101":65,#眠2连，40
        "0110":65,#眠2连，40
        "011":65,#眠2连，40
        "0011":65,#眠2连，40
        
        "01012":65,#眠2连，40
        "01102":65,#眠2连，40
        "00112":65,#眠2连，40

        "01010":75,#活2连，40
        "01100":75,#活2连，40
        "00110":75,#活2连，40
        "00011":75,#活2连，40
        
        #被堵住
        "0111":150,#眠3连，100
        
        "01112":150,#眠3连，100
        
        "01101":1000,#活3连，130
        "01011":1000,#活3连，130
        "01110": 1000,#活3连
        
        "01111":3000,#4连，300
        }

def eval(pieces,flag=-1):
    # assert isinstance(pieces,np.ndarray)
    s=""
    # score_map = {
            # "11111":100000, #长连
            # "011110":10000, #活四
            # "011112":10000,     #冲四
            # "0101110":10000,    #冲四
            # "0110110":10000,    #冲四
            # "01110":200,      #活三
            # "010110":200,     #活三
            # "001112" :50, #眠三
            # "010112":50, #眠三
            # "011012":50, #眠三
            # "10011":50, #眠三
            # "10101":50, #眠三
            # "2011102":50, #眠三
            # "00110":5, #活二
            # "01010":5, #活二
            # "010010":5, #活二
            # "000112":3,#眠二
            # "001012":3,#眠二
            # "010012":3,#眠二
            # "10001":3,#眠二
            # "2010102":3,#眠二
            # "2011002":3,#眠二
            # "211112":-5,#死四
            # "21112":-5,#死三
            # "2112":-5 #死二
            # }
    for i in pieces:
        if i == 0:
            s+="0"
        elif i == PLAYER_FLAG:
            s+="2"
        elif i == AI_FLAG:
            s+="1"
    rs = s[::-1]
    max_score = -1
    min_score = 10000000
    for k,v in score_map.items():
        if re.search(k,s) is not None or re.search(k,rs) is not None:
            if v > max_score:
                max_score = v
            if v < min_score:
                min_score = v
    return max_score,min_score

w = 1000
h = 1000
ROW = 40
COL = 40
size = (w,h)
direct = "left"
FOCUS_BOARD_MIN_X = 0
FOCUS_BOARD_MIN_Y = 0
FOCUS_BOARD_MAX_X = COL
FOCUS_BOARD_MAX_Y = ROW


def get_enabled_place(board):
    ay,ax = np.where(board!=0)
    search_min_x = max(min(ax) - 1,0)
    search_max_x = min(max(ax) + 1,COL-1)
    search_min_y = max(min(ay) - 1,0)
    search_max_y = min(max(ay) + 1,ROW-1)
    enabled_place = []
    for i in range(search_min_y,search_max_y):
        for j in range(search_min_x,search_max_x):
            if board[i][j] == 0 :
                enabled_place.push((i,j))
    return enabled_place
def neflag(flag):
    if flag==AI_FLAG:
        return PLAYER_FLAG
    elif flag==PLAYER_FLAG:
        return AI_FLAG
def get_eval(board,row,col,flag):
    #TODO: config how to eval
    row_pieces = board[row][(col-4 if col-4>=0 else 0):(col+5)]
    eval(row_pieces)
    col_pieces = [i[col] for i in board[(row-4 if row-4>=0 else 0):(row+5)]]
    lu2rb_pieces = [board[row+i][col+i] for i in range(-min(min(row,col),4),min(min(ROW-row-1,COL-col-1),4)+1)]
    ru2lb_pieces = [board[row+i][col-i] for i in range(-min(min(row,COL-col-1),4),min(min(ROW-row-1,col),4)+1)]
    print(eval(row_pieces))
    return check_win_piece_list(row_pieces,flag) or check_win_piece_list(col_pieces,flag) or check_win_piece_list(lu2rb_pieces,flag) or check_win_piece_list(ru2lb_pieces,flag)
MAX_DEPTH = 4
AI_BEST_MOVE = None
def alpha_beta(board,depth,alpha,beta,row,col,flag):
    #TODO: config how to eval
    if check_win(board,row,col,flag) : 
        return 100000000
    if depth == 0:
        return get_eval(board,row,col,flag)
    enabled_place = get_enabled_place(board)
    if flag==AI_FLAG: #AI MAX
        for place in enabled_place:
            r = place[0]
            c = place[1]
            board_next = board.copy()
            board_next[r][c] = PLAYER_FLAG
            value = alpha_beta(board_next,depth-1,alpha,beta,r,c,neflag(flag))
            if value > alpha:
                alpha = value
                if depth == MAX_DEPTH:
                    AI_BEST_MOVE = place
            if beta <= alpha:
                break
        return alpha
    else:#PLAYER MIN
        for place in enabled_place:
            r = place[0]
            c = place[1]
            board_next = board.copy()
            board_next[r][c] = AI_FLAG
            value = alpha_beta(board_next,depth-1,alpha,beta,r,c,neflag(flag))
            if value < beta:
                beta = value
                if depth == MAX_DEPTH:
                    AI_BEST_MOVE = place
            if beta <= alpha:
                break
        return beta
class AI:
    def __init__(self,flag):
        self.path = []
        self.flag = flag
    def expand(self,depth):
        pass

pygame.init()
window = pygame.display.set_mode(size)
bg = pygame.image.load("./bg.jpg").convert_alpha()
bg = pygame.transform.smoothscale(bg,(w,h))
window.blit(bg,(0,0))
pygame.display.set_caption("五子棋")

AI_FLAG = -1
AI_COLOR = (0,0,0)
PLAYER_FLAG = 1
PLAYER_COLOR = (255,255,255)

w_cell = w/COL
h_cell = h/ROW

def rect(point,color):
    left = point.col*w_cell
    top = point.row*h_cell
    pygame.draw.rect(window,color,(left,top,w_cell,h_cell))
def circle(x,y,color):
    c = x//w_cell
    r = y//h_cell
    left = c*w_cell
    top = r*h_cell
    pygame.draw.circle(window,color,(left+w_cell/2,top+h_cell/2),w_cell/2-2)
class Board:
    def __init__(self):
        # self.board = [[0]*COL for i in range(ROW)]
        self.board = np.zeros((ROW,COL))
    def step(self,ct,rt,flag):
        # ct = int(x//w_cell)
        # rt = int(y//h_cell)
        print("place",rt,ct)
        self.board[rt][ct] = flag


quit = True
clock = pygame.time.Clock()

turn = AI_FLAG

BOARD = Board()

def draw_board():
    for i in range(COL):
        pygame.draw.line(window,(255,255,255),(i*w_cell,0),(i*w_cell,w))
    for i in range(ROW):
        pygame.draw.line(window,(255,255,255),(0,i*h_cell),(h,i*h_cell))

def check_win_piece_list(pieces,flag):
    # assert isinstance(pieces,list)
    # assert len(pieces)<=9
    for i in range(len(pieces)-4):
        if sum(pieces[i:i+5]) == flag*5:
            return True
    return False
def check_win(board,row,col,flag):
    row_pieces = board[row][(col-4 if col-4>=0 else 0):(col+5)]
    eval(row_pieces)
    col_pieces = [i[col] for i in board[(row-4 if row-4>=0 else 0):(row+5)]]
    lu2rb_pieces = [board[row+i][col+i] for i in range(-min(min(row,col),4),min(min(ROW-row-1,COL-col-1),4)+1)]
    ru2lb_pieces = [board[row+i][col-i] for i in range(-min(min(row,COL-col-1),4),min(min(ROW-row-1,col),4)+1)]
    return check_win_piece_list(row_pieces,flag) or check_win_piece_list(col_pieces,flag) or check_win_piece_list(lu2rb_pieces,flag) or check_win_piece_list(ru2lb_pieces,flag)

previous_r = -1
previous_c = -1
print("now turn ",("AI " if turn==AI_FLAG else "PLAYER"))
while quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = False
        elif event.type == MOUSEBUTTONDOWN:
            pressed_array = pygame.mouse.get_pressed()
            for index in range(len(pressed_array)):
                if pressed_array[index]:
                    tx , ty = pygame.mouse.get_pos()
                    tc = int(tx//w_cell)
                    tr = int(ty//h_cell)
                    if index==0:
                        if BOARD.board[tr][tc]!=0:
                            print("you can't")
                            continue
                        if turn == AI_FLAG:
                            color_t = AI_COLOR
                            # alpha_beta(BOARD.board,MAX_DEPTH,float("-inf"),float("inf"),)
                        elif turn == PLAYER_FLAG:
                            color_t = PLAYER_COLOR
                        BOARD.step(tc,tr,turn)
                        circle(tx,ty,color_t)
                        if check_win(BOARD.board,tr,tc,turn):
                            print(("AI" if turn==AI_FLAG else "PLAYER"),"win")
                        if turn == AI_FLAG:
                            turn = PLAYER_FLAG
                        elif turn == PLAYER_FLAG:
                            turn = AI_FLAG
                        print("now turn ",("AI " if turn==AI_FLAG else "PLAYER"))
                    elif index==2:
                        if BOARD.board[tr][tc]!=0 and tr==previous_r and tc==previous_c:
                            pass



    # print(pygame.mouse.get_pos())
    # print(pygame.mouse.get_focused())
    draw_board()
    # pygame.draw.rect(window,(255,255,255),(5,5,80,80))

    pygame.display.update()
