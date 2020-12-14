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
pygame.display.set_caption("五子棋")

w_cell = w/COL
h_cell = h/ROW

def rect(point,color):
    left = point.col*w_cell
    top = point.row*h_cell
    pygame.draw.rect(window,color,(left,top,w_cell,h_cell))

quit = True
clock = pygame.time.Clock()

def draw_board():
    for i in range(COL):
        pygame.draw.line(window,(255,255,255),(i*w_cell,0),(i*w_cell,w))
    for i in range(ROW):
        pygame.draw.line(window,(255,255,255),(0,i*h_cell),(h,i*h_cell))

while quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = False
    draw_board()
    rect(Point(0,0),(255,255,0))
    # pygame.draw.rect(window,(255,255,255),(5,5,80,80))

    pygame.display.update()
