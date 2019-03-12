# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:07:20 2019

@author: Josh
"""

class Chip:
    '''
        Chip object containing team/color info and the coordinatesof the chip
    '''
    def __init__(self, row, column, color):
        '''
            - Initiates class variables from input ('row', 'column', 'color')
        '''
        self.row = row
        self.column = column
        self.color = color
        
    def __repr__(self):
        '''
            > Returns the string representation of the chip -> this shows up
              when printing the board (see 'printBoard()' in 'Board' class).
        '''
        return "{}".format(self.color)