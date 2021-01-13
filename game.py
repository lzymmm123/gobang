import pygame
from pygame.locals import *
import re
import numpy as np
from scipy.signal import convolve2d


class Point:
    row = 0
    col = 0
    def __init__(self,row,col):
        self.row = row
        self.col = col
    def copy(self):
        return Point(self.row,self.col)
w = 1000
h = 1000
ROW = 20
COL = 20
size = (w,h)
direct = "left"
FOCUS_BOARD_MIN_X = 0
FOCUS_BOARD_MIN_Y = 0
FOCUS_BOARD_MAX_X = COL
FOCUS_BOARD_MAX_Y = ROW

def check_has_neibor(board,i,j):
    h,w = board.shape[0],board.shape[1]
    try:
        if board[i-1][j-1] == 0 and board[i-1][j]==0 and board[i-1][j+1]==0 and board[i][j-1] == 0 and board[i][j]==0 and board[i][j+1]==0 and board[i+1][j-1] == 0 and board[i+1][j]==0 and board[i+1][j+1]==0 :
            return False
    except:
        return True
    return True
def get_enabled_place(board):
    ay,ax = np.where(board!=0)
    search_min_x = max(min(ax) - 2,0)
    search_max_x = min(max(ax) + 2,COL-1)
    search_min_y = max(min(ay) - 2,0)
    search_max_y = min(max(ay) + 2,ROW-1)
    enabled_place = []
    for i in range(search_min_y,search_max_y):
        for j in range(search_min_x,search_max_x):
            if board[i][j] == 0 :
                if check_has_neibor(board,i,j):
                    enabled_place.append((i,j))
    return enabled_place
def neflag(flag):
    if flag==AI_FLAG:
        return PLAYER_FLAG
    elif flag==PLAYER_FLAG:
        return AI_FLAG
def get_eval(board,row,col,flag):
    #TODO: config how to eval
    row_pieces = board[row][(col-4 if col-4>=0 else 0):(col+5)]
    col_pieces = [i[col] for i in board[(row-4 if row-4>=0 else 0):(row+5)]]
    lu2rb_pieces = [board[row+i][col+i] for i in range(-min(min(row,col),4),min(min(ROW-row-1,COL-col-1),4)+1)]
    ru2lb_pieces = [board[row+i][col-i] for i in range(-min(min(row,COL-col-1),4),min(min(ROW-row-1,col),4)+1)]
    # print("AI eval " if flag==AI_FLAG else "Player Eval")
    # print("row ",eval(row_pieces))
    # print("col ",eval(col_pieces))
    # print("lu2rb ",eval(lu2rb_pieces))
    # print("ru2lb ",eval(ru2lb_pieces))
    return max(eval(row_pieces,flag)[0] ,eval(col_pieces,flag)[0],eval(lu2rb_pieces,flag)[0],eval(ru2lb_pieces,flag)[0])

def get_eval1(board,flag):
    value = 0
    for i in fliter5_maps:
        value += 10000*np.sum(convolve2d(board,i,mode='valid')==-5)
        value += -8000*np.sum(convolve2d(board,i,mode='valid')==5)
    for i in fliter4_maps:
        value += 1000*np.sum(convolve2d(board,i,mode='valid')==-4)
        value += -800*np.sum(convolve2d(board,i,mode='valid')==4)
    for i in fliter3_maps:
        value += 100*np.sum(convolve2d(board,i,mode='valid')==-3)
        value += -80*np.sum(convolve2d(board,i,mode='valid')==3)
    for i in fliter2_maps:
        value += 10*np.sum(convolve2d(board,i,mode='valid')==-2)
        value += -8*np.sum(convolve2d(board,i,mode='valid')==2)
    # print("value   ",value)
    return value


eval_map  ={
        "11111":100000000, "22222":-100000000, "011110":10000000, "022220":-10000000, "011112":1000000, "211110":1000000, "10111":1000000, "11011":1000000, "11101":1000000, "022221":-1000000, "122220":-1000000, "20222":-1000000, "22022":-1000000, "22202":-1000000, "001110":100000, "011100":100000, "010110":100000, "011010":100000, "002220":-100000, "022200":-100000, "020220":-100000, "022020":-100000, "001112":10000, "010112":10000, "011012":10000, "011102":10000, "211100":10000, "211010":10000, "210110":10000, "201110":10000, "00111":10000, "10011":10000, "10101":10000, "10110":10000, "01011":10000, "10011":10000, "11001":10000, "11010":10000, "01101":10000, "10101":10000, "11001":10000, "11100":10000, "002221":-10000, "020221":-10000, "022021":-10000, "022201":-10000, "122200":-10000, "122020":-10000, "120220":-10000, "102220":-10000, "00222":-10000, "20022":-10000, "20202":-10000, "20220":-10000, "02022":-10000, "20022":-10000, "22002":-10000, "22020":-10000, "02202":-10000, "20202":-10000, "22002":-10000, "22200":-10000, "000110":1000, "001010":1000, "001100":1000, "001100":1000, "010100":1000, "011000":1000, "000110":1000, "010010":1000, "010100":1000, "001010":1000, "010010":1000, "011000":1000, "000220":-1000, "002020":-1000, "002200":-1000, "002200":-1000, "020200":-1000, "022000":-1000, "000220":-1000, "020020":-1000, "020200":-1000, "002020":-1000, "020020":-1000, "022000":-1000, "000112":100, "001012":100, "010012":100, "10001":100, "2010102":100, "2011002":100, "211000":100, "210100":100, "210010":100, "2001102":100, "000221":-100, "002021":-100, "020021":-100, "20002":-100, "1020201":-100, "1022001":-100, "122000":-100, "120200":-100, "120020":-100, "1002201":-100,
        }
def eval2(pieces):
    s=""
    score = 0
    for i in pieces:
        if i == 0:
            s+="0"
        elif i == PLAYER_FLAG:
            s+="2"
        elif i == AI_FLAG:
            s+="1"
    for k,v in eval_map.items():
        if re.search(k,s) is not None:
            score += v
    return score

def get_eval2(board,row,col,mark):
    score = 0
    if mark[row,col,0]==0:
        row_pieces = board[row]
        mark[row,:,0] = 1
        score += eval2(row_pieces)
    if mark[row,col,1]==0:
        col_pieces = board[:,col]
        mark[:,col,1] = 1
        score += eval2(col_pieces)
    if mark[row,col,2]==0:
        lu2rb_pieces = np.diagonal(board,offset=col-row)
        offset1 = col-row
        index1 = np.array([[i,i+offset1] for i in range(ROW) if i+offset1<COL]).T
        mark[index1[0],index1[1],2] = 1
        score += eval2(lu2rb_pieces)
    if mark[row,col,3]==0:
        offset2 = (COL-1)-col-row
        ru2lb_pieces = np.diagonal(np.flip(board,axis=1),offset=offset2)
        index2 = np.array([[i,COL-1-i-offset2] for i in range(ROW) if COL-1-i-offset2>=0 and COL-1-i-offset2<COL]).T
        mark[index2[0],index2[1],3] = 1
        score += eval2(ru2lb_pieces)
    return score

def get_test_eval(board):
    h,w = board.shape[0],board.shape[1]
    mark = np.zeros((h,w,4)) #0 line; 1 col ; 2 lefttop2rightbottom; 3 righttop2leftbottom
    score = 0
    for i in range(h):
        for j in range(w):
            if board[i][j]!=0:
                score += get_eval2(board,i,j,mark)
                # print(mark)
    return score
MAX_DEPTH = 3
AI_BEST_MOVE = None

def check_win_test(board):
    pass

def alpha_beta(board,depth,alpha,beta,flag):
    global AI_BEST_MOVE

    if depth <= 0:
        # return get_eval(board,row,col,flag)
        return get_test_eval(board)
    enabled_place = get_enabled_place(board)
    # print("ai best ",AI_BEST_MOVE)
    if flag==AI_FLAG: #AI MAX
        for place in enabled_place:
            r = place[0]
            c = place[1]
            board[r][c] = AI_FLAG
            if check_win(board,r,c,AI_FLAG):
                value = 10000000000
            else:
                value = alpha_beta(board,depth-1,alpha,beta,neflag(flag))
            board[r][c] = 0
            if value > alpha:
                alpha = value
                if depth == MAX_DEPTH:
                    AI_BEST_MOVE = place
            if beta <= alpha:
                # print("break max")
                break
        return alpha
    else:#PLAYER MIN
        for place in enabled_place:
            r = place[0]
            c = place[1]
            board[r][c] = PLAYER_FLAG
            if check_win(board,r,c,PLAYER_FLAG):
                value = -1000000000000
            else:
                value = alpha_beta(board,depth-1,alpha,beta,neflag(flag))
            board[r][c] = 0
            if value < beta:
                beta = value
                if depth == MAX_DEPTH:
                    AI_BEST_MOVE = place
            if beta <= alpha:
                # print("break min")
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
def circle(r,c,color):
    left = c*w_cell
    top = r*h_cell
    pygame.draw.circle(window,color,(left+w_cell/2,top+h_cell/2),w_cell/2-2)
class Board:
    def __init__(self):
        # self.board = [[0]*COL for i in range(ROW)]
        self.board = np.zeros((ROW,COL))
    def step(self,rt,ct,flag):
        # ct = int(x//w_cell)
        # rt = int(y//h_cell)
        print("place",rt,ct)
        self.board[rt][ct] = flag

def copy_board(board):
    copy_board = np.zeros((ROW,COL))


quit = True
clock = pygame.time.Clock()

turn = PLAYER_FLAG

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
    # eval(row_pieces)
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
                            enabled_place = get_enabled_place(BOARD.board)
                            # print("enabled_place",len(enabled_place))
                            alpha_beta(BOARD.board.copy(),MAX_DEPTH,float("-inf"),float("inf"),AI_FLAG)
                            tr = AI_BEST_MOVE[0]
                            tc = AI_BEST_MOVE[1]
                        elif turn == PLAYER_FLAG:
                            color_t = PLAYER_COLOR
                        BOARD.step(tr,tc,turn)
                        # get_eval(BOARD.board,tr,tc,turn)
                        circle(tr,tc,color_t)
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

    pygame.display.update()
