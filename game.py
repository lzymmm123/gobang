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

fliter5_maps = [
        np.identity(5),
        np.flip(np.identity(5),0),
        np.array([[1,1,1,1,1]]),
        np.array([ [1], [1], [1], [1], [1] ])
        ]
fliter4_maps = [
        np.identity(4),
        np.flip(np.identity(4),0),
        np.array([[1,1,1,1]]),
        np.array([ [1], [1], [1], [1] ])
        ]

fliter3_maps = [
        np.identity(3),
        np.flip(np.identity(3),0),
        np.array([[1,1,1]]),
        np.array([ [1], [1], [1] ])
        ]
fliter2_maps = [
        np.identity(2),
        np.flip(np.identity(2),0),
        np.array([[1,1]]),
        np.array([ [1], [1] ])
        ]
score_map = {
        "11111":10000, #AI连五
        "22222":-10000, #PLAYER 连五
        "022220":-9050,
        "122220":-9040,
        "0222020":-9040,
        "0220220":-9040,
        "011110":9030,
        "211110":9020,
        "0111010":9020,
        "0110110":9020,

        # "01": 17,#眠1连
        # "001": 17,#眠1连
        # "0001": 17,#眠1连
        
        # "0102":16,#眠1连，15
        # "0012":15,#眠1连，15
        # "01002":19,#眠1连，15
        # "00102":17,#眠1连，15
        # "00012":12,#眠1连，15

        # "01000":21,#活1连，15
        # "00100":19,#活1连，15
        # "00010":17,#活1连，15
        # "00001":15,#活1连，15

        # #被堵住
        # "0101":65,#眠2连，40
        # "0110":65,#眠2连，40
        # "011":65,#眠2连，40
        # "0011":65,#眠2连，40
        
        # "01012":65,#眠2连，40
        # "01102":65,#眠2连，40
        # "00112":65,#眠2连，40

        # "01010":75,#活2连，40
        # "01100":75,#活2连，40
        # "00110":75,#活2连，40
        # "00011":75,#活2连，40
        
        # #被堵住
        # "0111":150,#眠3连，100
        
        # "01112":150,#眠3连，100
        
        # "01101":1000,#活3连，130
        # "01011":1000,#活3连，130
        # "01110": 1000,#活3连
        
        # "01111":3000,#4连，300
        # "11111":100000,
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
ROW = 20
COL = 20
size = (w,h)
direct = "left"
FOCUS_BOARD_MIN_X = 0
FOCUS_BOARD_MIN_Y = 0
FOCUS_BOARD_MAX_X = COL
FOCUS_BOARD_MAX_Y = ROW

WIN_AI = ["11111"]
WIN_PLAYER = ["22222"]
HUO4_AI = ["011110"]
HUO4_PLAYER = ["022220"]
CHONG4_AI = ["011112", "211110", "10111", "11011", "11101"]
CHONG4_PLAYER = ["022221", "122220", "20222", "22022", "22202"]
HUO3_AI = ["001110", "011100", "010110", "011010"]
HUO3_PLAYER = ["002220", "022200", "020220", "022020"]
MIAN3_AI = ["001112", "010112", "011012", "011102", "211100", "211010", "210110", "201110", "00111", "10011", "10101", "10110", "01011", "10011", "11001", "11010", "01101", "10101", "11001", "11100",]
MIAN3_PLAYER = ["002221", "020221", "022021", "022201", "122200", "122020", "120220", "102220", "00222", "20022", "20202", "20220", "02022", "20022", "22002", "22020", "02202", "20202", "22002", "22200",]
HUO2_AI = ["000110", "001010", "001100", "001100", "010100", "011000", "000110", "010010", "010100", "001010", "010010", "011000",]
HUO2_PLAYER = ["000220", "002020", "002200", "002200", "020200", "022000", "000220", "020020", "020200", "002020", "020020", "022000",]
MIAN2_AI = ["000112", "001012", "010012", "10001", "2010102", "2011002", "211000", "210100", "210010", "2001102"]
MIAN2_PLAYER = ["000221", "002021", "020021", "20002", "1020201", "1022001", "122000", "120200", "120020", "1002201"]
# def computeScore() {
        # score = 0;
        # for (int i = 0; i < BOARD_SIZE; i++) {
            # for (int j = 0; j < BOARD_SIZE; j++) {
                # if (board[i][j] != BLANK) {
                    # List<String> list = getString(i, j);
                    # if (checkSituation(AI, list, WIN)) {
                        # score += 100000000;
                    # }
                    # if (checkSituation(PLAYER, list, WIN)) {
                        # score += -100000000;
                    # }
                    # if (checkSituation(AI, list, HUO4)) {
                        # score += 10000000;
                    # }
                    # if (checkSituation(PLAYER, list, HUO4)) {
                        # score += -10000000;
                    # }
                    # if (checkSituation(AI, list, CHONG4)) {
                        # score += 1000000;
                    # }
                    # if (checkSituation(PLAYER, list, CHONG4)) {
                        # score += -1000000;
                    # }
                    # if (checkSituation(AI, list, HUO3)) {
                        # score += 100000;
                    # }
                    # if (checkSituation(PLAYER, list, HUO3)) {
                        # score += -100000;
                    # }
                    # if (checkSituation(AI, list, MIAN3)) {
                        # score += 10000;
                    # }
                    # if (checkSituation(PLAYER, list, MIAN3)) {
                        # score += -10000;
                    # }
                    # if (checkSituation(AI, list, HUO2)) {
                        # score += 1000;
                    # }
                    # if (checkSituation(PLAYER, list, HUO2)) {
                        # score += -1000;
                    # }
                    # if (checkSituation(AI, list, MIAN2)) {
                        # score += 100;
                    # }
                    # if (checkSituation(PLAYER, list, MIAN2)) {
                        # score += -100;
                    # }
                    # if (checkSituation(AI, list, OL1)) {
                        # score += 10;
                    # }
                    # if (checkSituation(PLAYER, list, OL1)) {
                        # score += -10;
                    # }
                    # if (checkSituation(AI, list, NONE)) {
                        # score += 1;
                    # }
                    # if (checkSituation(PLAYER, list, NONE)) {
                        # score += -1;
                    # }
                # }
            # }
        # }
        # return score;
    # }

def check_has_neibor(board,i,j):
    h,w = board.shape[0],board.shape[1]
    flag = True
    if (i>0 and board[i-1][j]==0) and (i<h-1 and board[i+1][j]==0) and (j>0 and board[i][j-1]==0) and (j<w-1 and board[i][j+1]==0):
        return False
    return True
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
        "11111":100000000,
        "22222":-100000000,
        "011110":10000000,
        "022220":-10000000,
        "011112":1000000,
        "211110":1000000,
        "10111":1000000,
        "11011":1000000,
        "11101":1000000,
        "022221":-1000000,
        "122220":-1000000,
        "20222":-1000000,
        "22022":-1000000,
        "22202":-1000000,
        "001110":100000,
        "011100":100000,
        "010110":100000,
        "011010":100000,
        "002220":-100000,
        "022200":-100000,
        "020220":-100000,
        "022020":-100000,
        "001112":10000,
        "010112":10000,
        "011012":10000,
        "011102":10000,
        "211100":10000,
        "211010":10000,
        "210110":10000,
        "201110":10000,
        "00111":10000,
        "10011":10000,
        "10101":10000,
        "10110":10000,
        "01011":10000,
        "10011":10000,
        "11001":10000,
        "11010":10000,
        "01101":10000,
        "10101":10000,
        "11001":10000,
        "11100":10000,
        "002221":-10000,
        "020221":-10000,
        "022021":-10000,
        "022201":-10000,
        "122200":-10000,
        "122020":-10000,
        "120220":-10000,
        "102220":-10000,
        "00222":-10000,
        "20022":-10000,
        "20202":-10000,
        "20220":-10000,
        "02022":-10000,
        "20022":-10000,
        "22002":-10000,
        "22020":-10000,
        "02202":-10000,
        "20202":-10000,
        "22002":-10000,
        "22200":-10000,
        "000110":1000,
        "001010":1000,
        "001100":1000,
        "001100":1000,
        "010100":1000,
        "011000":1000,
        "000110":1000,
        "010010":1000,
        "010100":1000,
        "001010":1000,
        "010010":1000,
        "011000":1000,
        "000220":-1000,
        "002020":-1000,
        "002200":-1000,
        "002200":-1000,
        "020200":-1000,
        "022000":-1000,
        "000220":-1000,
        "020020":-1000,
        "020200":-1000,
        "002020":-1000,
        "020020":-1000,
        "022000":-1000,
        "000112":100,
        "001012":100,
        "010012":100,
        "10001":100,
        "2010102":100,
        "2011002":100,
        "211000":100,
        "210100":100,
        "210010":100,
        "2001102":100,
        "000221":-100,
        "002021":-100,
        "020021":-100,
        "20002":-100,
        "1020201":-100,
        "1022001":-100,
        "122000":-100,
        "120200":-100,
        "120020":-100,
        "1002201":-100,
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
    # rs = s[::-1]
    for k,v in eval_map.items():
        # if re.search(k,s) is not None or re.search(k,rs) is not None:
        if re.search(k,s) is not None:
            score += v
    return score

def get_eval2(board,row,col):
    row_pieces = board[row][(col-4 if col-4>=0 else 0):(col+5)]
    col_pieces = [i[col] for i in board[(row-4 if row-4>=0 else 0):(row+5)]]
    lu2rb_pieces = [board[row+i][col+i] for i in range(-min(min(row,col),4),min(min(ROW-row-1,COL-col-1),4)+1)]
    ru2lb_pieces = [board[row+i][col-i] for i in range(-min(min(row,COL-col-1),4),min(min(ROW-row-1,col),4)+1)]
    score = eval2(row_pieces)+eval2(col_pieces)+eval2(lu2rb_pieces)+eval2(ru2lb_pieces)
    return score

def get_test_eval(board):
    h,w = board.shape[0],board.shape[1]
    score = 0
    for i in range(h):
        for j in range(w):
            if board[i][j]!=0:
                score += get_eval2(board,i,j)
    return score
MAX_DEPTH = 2
AI_BEST_MOVE = None

def alpha_beta(board,depth,alpha,beta,flag):
    global AI_BEST_MOVE

    # if check_win(board,row,col,flag) :
        # return get_eval(board,row,col,flag)
        # return get_eval1(board,flag)
    if depth <= 0:
        # return get_eval(board,row,col,flag)
        return get_test_eval(board)
    enabled_place = get_enabled_place(board)
    # print("ai best ",AI_BEST_MOVE)
    if flag==AI_FLAG: #AI MAX
        for place in enabled_place:
            r = place[0]
            c = place[1]
            # board_next = board.copy()
            # board_next[r][c] = PLAYER_FLAG
            board[r][c] = AI_FLAG
            value = alpha_beta(board,depth-1,alpha,beta,neflag(flag))
            board[r][c] = 0
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
            # board_next = board.copy()
            # board_next[r][c] = AI_FLAG
            board[r][c] = PLAYER_FLAG
            value = alpha_beta(board,depth-1,alpha,beta,neflag(flag))
            board[r][c] = 0
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
def circle(r,c,color):
    # c = x//w_cell
    # r = y//h_cell
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
                            print("enabled_place",len(enabled_place))
                            # for place in enabled_place:
                                # board_next = BOARD.board.copy()
                                # board_next[tr][tc] = AI_FLAG
                            alpha_beta(BOARD.board.copy(),MAX_DEPTH,float("-inf"),float("inf"),turn)
                            tr = AI_BEST_MOVE[0]
                            tc = AI_BEST_MOVE[1]
                        elif turn == PLAYER_FLAG:
                            color_t = PLAYER_COLOR
                        BOARD.step(tc,tr,turn)
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
    # pygame.draw.rect(window,(255,255,255),(5,5,80,80))

    pygame.display.update()
