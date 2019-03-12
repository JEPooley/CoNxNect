# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 20:11:18 2019

@author: Josh
"""

import numpy as np
from chip_class import Chip
from lines_class import Lines
import random
import copy 
import math

class Board(Lines):
    '''
        A Board object contains:
            
            - The size of the board ('rows' x 'columns').
            - A list of team colours ('chipColors').
            - A winning score ('streakTarget').
    '''
    
    def __init__(self, rows, columns, chipColors, streakTarget = 4):
        '''
            - Initiates class variables ('rows', 'columns', 'chipColors', 'streakTarget').
            - Generates an empty board ('boardArray').
            - Creates empty list of chips ('chipList').
            - Creates initial list of available columns ('availableColumns').
            - finds the central column(s) of the board for scoring purposes ('centralColumns').
        '''
        Lines.__init__(self, rows, columns)
        self.boardArray = [ [None for cc in range(columns)] for rr in range(rows) ]
        self.chipColors = chipColors
        self.chipList = []
        self.streakTarget = streakTarget
        self.availableColumns = list(range(columns))
        if columns%2 != 0:
            self.centralColumns = [int((columns+1)/2)-1]
        else:
            self.centralColumns = [int(columns/2)-1, int((columns)/2)]
        
    def _checkAllLines(self):
        '''
            - Finds the number of consecutive same-color chips for every vertical, 
              horizontal and diagonal line of the board.
            > Returns a dictionary which gives a separate count for each team 
              color e.g. {color : [ list of color streaks ] } ('lineScoreDict').
        '''
        lineScoreDict = {c : [] for c in self.chipColors}
        for line in self.lines:
            lineScore = self._checkLine(line)
            for color in lineScore.keys():
                lineScoreDict[color].extend(lineScore[color])
        return lineScoreDict
        
    def _checkLine(self, lineCoords):
        '''
            - Finds the number of consecutive same-color chips for a set of 
              line coordinates ('lineCoords') assuming that the coordinates
              are given in a logical order.
            > Returns a dictionary which gives a separate count for each team 
              color e.g. {color : [ list of color streaks ] } ('lineScoreDict').
        '''
        lineScoreDict = {c : [] for c in self.chipColors}
        if len(lineCoords) < self.streakTarget:
            return lineScoreDict
        streak = 0
        currentColor = None
        for coord in lineCoords:
            value = self.boardArray[coord[0]][coord[1]]
            if value == None:
                if streak > 1:
                    lineScoreDict[currentColor].append(streak)
                streak = 0
                currentColor = None
            elif value.color == currentColor:
                streak += 1
            else:
                if streak > 1:
                    lineScoreDict[currentColor].append(streak)
                streak = 1
                currentColor = value.color
        if streak > 1:
            lineScoreDict[currentColor].append(streak)
        return lineScoreDict
        
    def _chipCount(self, column):
        '''
            - Counts the number of any-color chips in a specified column ('column').
            > Returns this number.
        '''
        count = 0
        for c in self.boardArray:
            if c[column] != None:
                count += 1
        return count
    
    def _cloneBoard(self):
        '''
            - Creates a deep copy of itself, with the same chip configuration ('clone').
            > Returns the cloned 'Board' object.
        '''
        clone = Board(self.rows, self.columns, self.chipColors, self.streakTarget)
        clone.boardArray = copy.deepcopy(self.boardArray)
        return clone
    
    def _findAvailable(self):
        '''
            - Checks the top row to see if any columns are full.
            - Changes 'availableColumns' by removing any full columns.
        '''
        count = 0
        available = []
        for c in self.boardArray[0]:
            if c == None:
                available.append(count)
            count += 1
        self.availableColumns = available
        
    def _getNextTurn(self, color):
        '''
            - Continuously cycles through each color in the 'chipColors' list.
            > Returns consecutive colors as a string.
        '''
        idx = self.chipColors.index(color)
        if idx != len(self.chipColors) - 1:
            return self.chipColors[idx + 1]
        else:
            return self.chipColors[0]
        
    def _minimax(self, depth, color, streakMultiply = 2, middleBonus = 4):
        '''
            - Implementation of the maxN algorithm to find an optimal next move
              for the specified team color ('color').
            - The algorithm searches possible moves at a specified depth ('depth')
            - The 'streakMultiply' and 'middleBonus' inputs are passed to the 
              function '_scoreBoard()' to assess the success of a move.
            > Returns the optimised move ('column'), along with the corresponding
              success score ('value').
              
        '''
        winner = self.checkWin()
        if depth == 0 or winner != None or len(self.availableColumns) == 0:
            if winner != None:
                score = {cc : -1e6 for cc in self.chipColors}
                score[winner] = 1e6
                return None, score
            elif len(self.availableColumns) == 0:
                return None, {cc : 0 for cc in self.chipColors}
            else:
                return None, self._scoreBoard(streakMultiply, middleBonus)
        value = {cc : -math.inf for cc in self.chipColors}
        column = random.choice(self.availableColumns)
        nextColor = self._getNextTurn(color)
        for c in self.availableColumns:
            clone = self._cloneBoard()
            clone.addChip(c, color)
            score = clone._minimax(depth-1, nextColor)[1]
            if score[color] > value[color]:
                value = score
                column = c
        return column, value
    
    def _scoreBoard(self, streakMultiply, middleBonus):
        '''
            - For a given board state ('boardArray'), each color chip is given
              a score based on the liklihood of it winning.
            - The score is calculated as: 
                
                'streakMultiply' x sum of (number of consecutive chips) +
                'middleBonus' x number of chips in the middle of the board ('centralColumns' list)
                
            > Returns a dictionary which gives a separate score for each team 
              color e.g. {color : score } ('scoreDict').
        '''
        lineScoreDict = self._checkAllLines()
        scoreDict = {}
        for color in self.chipColors:
            score = 0
            score += sum([s*streakMultiply for s in lineScoreDict[color]])
            for r in range(self.rows):
                for c in self.centralColumns:
                    if self.boardArray[r][c] != None and self.boardArray[r][c].color == color:
                        score += middleBonus
            scoreDict[color] = score
        return scoreDict

    def addChip(self, column, color):
        '''
            - Creates a new 'Chip' object of the given color ('color') 
              and puts it at the bottom of specified the column ('column') if
              available.
            - Also adds the new chip to the 'chipList', which keeps track of all
              current chips.
        '''
        assert color in self.chipColors, 'chip colour "{}" not defined'.format(color)
        numberInColumn = self._chipCount(column)
        if column in self.availableColumns:
            self.boardArray[self.rows - numberInColumn -1][column] = Chip(numberInColumn, column, color)
            self.chipList.append(self.boardArray[self.rows - numberInColumn -1][column])
            self._findAvailable()
        else:
            pass
    
    def checkWin(self):
        '''
            - Checks each line on the board to see if a streak of 'streakTarget'
              has been reached.
            > Returns 'None' if this condition is not met.
            > Returns the 'color' of the winning team if the condition is met.
              
        '''
        lineScoreDict = self._checkAllLines()
        for color in lineScoreDict:
            if any([s>=self.streakTarget for s in lineScoreDict[color]]):
                return color
        return None
    
    def findMove(self, color):
        '''
            - Initiates the maxN algorithm for a specified 'color'.
            > Returns the column that the algorithm has settled on.
        '''
        return self._minimax(3, color)[0]
    
    def printBoard(self):
        '''
            - Prints the 'boardArray' as a series of row lists.
        '''
        for r in self.boardArray:
            print(r)
