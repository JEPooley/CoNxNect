# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 11:41:20 2019

@author: Josh
"""

import pygame
import pygame.gfxdraw
from board_class import Board
from itertools import cycle
import numpy as np
import math
import random

'''
    - Simple pygame script to visualise the connect 4 game 
'''


def play(columns, aiNum, target):
    '''
        - Initialise pygame, set window size and create a list of possible chip 
          colors.
    '''
    pygame.init()
    
    boardWidth = 504
    boardHeight = 588   
    gameDisplay = pygame.display.set_mode((boardWidth,boardHeight))
    pygame.display.set_caption('CoNxNect')
    
    colorBank = ['0x7bdff2', '0xf0544f', '0xffff82', '0x5ad800', '0xba48ba']

    teams = random.sample(colorBank, aiNum+1)
    username = teams[0]

    takeTurns(gameDisplay, columns, username, teams, target, boardWidth, boardHeight)
        
    pygame.quit()
    quit()
    
def drawBoard(surface, board):
    '''
        - Draw all the chips from the 'Board' classes 'chipList' attribute.
    '''
    white = (255,255,255)
    surface.fill(white)
    pygame.draw.rect(surface, (50,50,50), (0,84,504,588))
    diam = int(504/board.columns)
    for cp in board.chipList:
        drawChip(surface, cp.column, cp.row, diam, pygame.Color(cp.color))
       
def drawChip(surface, col, row, diam, color):
    '''
        - Draw an individual chip with 'color' and grid position ('row', 'column')
        - Convert grid position to pixel values.
        - the chip diameter is set by 'diam'
    '''
    radius = diam/2
    black = pygame.Color('0x000000')
    white = pygame.Color('0x0000001f')
    x = int( radius*( (col*2) +1) )
    y = int( 588-radius*( (row*2) +1) )
    pygame.gfxdraw.aacircle(surface, x, y, int(radius*0.9), color)
    pygame.gfxdraw.filled_circle(surface, x, y, int(radius*0.9), color)
    pygame.gfxdraw.aacircle(surface, x, y, int(radius*0.7), white)
    pygame.gfxdraw.filled_circle(surface, x, y, int(radius*0.7), white)

def takeTurns(gameDisplay, columns, username, teams, target, boardWidth, boardHeight):
    '''
        - Creates basic gameplay loop.
        - Each team/color takes it in turns to add a chip to the board. The user
          can click to add a chip. On a CPU's turn, the 'findMove()' function
          from the 'Board' object is called.
    '''
    exitGame = False
    teamsIter = cycle(iter(teams))
    clock = pygame.time.Clock()
    for i in range(np.random.randint(1, len(teams)+1)):
        next(teamsIter)
    turn = next(teamsIter)
    board = Board(columns, columns, teams, target)
    
    while not exitGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitGame = True
        if board.checkWin() == None and board.availableColumns != []:
            if turn != username:
                newColumn = board.findMove(turn)
                board.addChip(newColumn, turn)
                turn = next(teamsIter)
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    move = int(math.floor(posx/(boardWidth/columns)))
                    if move in board.availableColumns:
                        board.addChip(move, turn)
                        turn = next(teamsIter)
            drawBoard(gameDisplay, board)
            
        if board.checkWin() != None:
            print('{} wins!!'.format(turn))
        elif board.availableColumns == []:
            print("It's a draw!!")
            
        pygame.display.update()
        clock.tick(25)

if __name__ == '__main__':
    play(9, 2, 4)