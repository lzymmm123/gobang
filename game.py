import pygame
from pygame.locals import *


class Point:
    row = 0
    col = 0
    def __init__(self,row,col):
        self.row = row
        self.col = col
    def copy(self):
        return Point(self.row,self.col)



pygame.init()
w = 800
h = 800
ROW = 10
COL = 10
size = (w,h)
direct = "left"
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
        self.board = [[0]*COL for i in range(ROW)]
    def step(self,x,y,flag):
        ct = int(x//w_cell)
        rt = int(y//h_cell)
        print(rt,ct)
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

def check_win_piece_list(pieces):
    assert isinstance(pieces,list)
    assert len(pieces)<=9
    for i in range(len(pieces)-4):
        print("asjdklasjdklasdjk",sum(pieces[i:i+5]) , -turn*5)
        if sum(pieces[i:i+5]) == turn*5:
            return True
    return False
def check_win(row,col):
    row_pieces = BOARD.board[row][(col-4 if col-4>=0 else 0):(col+5)]
    col_pieces = [i[col] for i in BOARD.board[(row-4 if row-4>=0 else 0):(row+5)]]
    # print("sadasd0",-min(min(row,col),4),COL)
    # print("sadasd1",0,min(min(ROW-row,COL-col),4))
    # print("sadasd2",-min(min(row,col),4),min(min(ROW-row,COL-col)),4)
    # print("sadasd3",range(-min(min(row,col),4),min(min(ROW-row,COL-col)),4)+1)
    print("asdas",-min(min(row,col),4),min(min(ROW-row-1,COL-col-1),4)+1,ROW-row-1,COL-col-1)
    lu2rb_pieces = [BOARD.board[row+i][col+i] for i in range(-min(min(row,col),4),min(min(ROW-row-1,COL-col-1),4)+1)]
    ru2lb_pieces = [BOARD.board[row+i][col-i] for i in range(-min(min(row,COL-col-1),4),min(min(ROW-row-1,col),4)+1)]
    print(row_pieces)
    print(col_pieces)
    print(lu2rb_pieces)
    print(ru2lb_pieces)
    return check_win_piece_list(row_pieces) or check_win_piece_list(col_pieces) or check_win_piece_list(lu2rb_pieces) or check_win_piece_list(ru2lb_pieces)

while quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = False
        elif event.type == MOUSEBUTTONDOWN:
            pressed_array = pygame.mouse.get_pressed()
            for index in range(len(pressed_array)):
                if pressed_array[index]:
                    if index==0:
                        tx , ty = pygame.mouse.get_pos()
                        tc = int(tx//w_cell)
                        tr = int(ty//h_cell)
                        if BOARD.board[tr][tc]!=0:
                            print("you can't")
                            continue
                        if turn == AI_FLAG:
                            color_t = (255,255,255)
                            turn = PLAYER_FLAG
                        elif turn == PLAYER_FLAG:
                            color_t = (0,0,0)
                            turn = AI_FLAG
                        BOARD.step(tx,ty,turn)
                        circle(tx,ty,color_t)
                        if check_win(tr,tc):
                            print("win")

    # print(pygame.mouse.get_pos())
    # print(pygame.mouse.get_focused())
    draw_board()
    # pygame.draw.rect(window,(255,255,255),(5,5,80,80))

    pygame.display.update()
