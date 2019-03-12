# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 09:21:01 2019

@author: jp16g11
"""

class Lines:
    '''
        A Lines object contains:
            
            - All of the horizontal and vertical line coordinates for a grid of
              dimensions ('rows' x 'columns').
    '''
    def __init__(self, rows, columns):
        '''
            - Initialise input variables ('rows' and 'columns').
            - Call class function '_getLines()' to automatically generate a list
              of line coordinates.
        '''
        self.rows = rows
        self.columns = columns
        self.lines = self._getLines(rows, columns)
        
    def _getLines(self, nRows, nColumns):
        return self._getRows(nRows, nColumns) + self._getColumns(nRows, nColumns) + self._getDiagonalNE(nRows, nColumns) + self._getDiagonalSW(nRows, nColumns)

    def _findLine(self, startRow, startColumn, nRows, nColumns, rowIncrement, columnIncrement):
        '''
            - Starting from the coordinate ('startRow', 'startColumn'), finds
              all points at set increments (+'rowIncrement', + 'columnIncrement')
              until the edge of the grid is reached.
            - 'nRows' and 'nColumns' specifies the grid dimensions.
            > Returns a list of the coordinates, as found in manner above.
        '''
        row, column = startRow, startColumn
        line = []
        while 0 <= row < nRows and 0 <= column < nColumns:
            line.append((row, column))
            row += rowIncrement
            column += columnIncrement
        return line
    
    def _getRows(self, nRows, nColumns):
        '''
            - Finds all of the horizontal line coordinates.
            - 'nRows' and 'nColumns' specifies the grid dimensions.
            > Returns a list of sublists; each sublist corresponds to a set of
              line coordinates.
        '''
        return [self._findLine(rr, 0, nRows, nColumns, 0, 1) for rr in range(nRows)]
    
    def _getColumns(self, nRows, nColumns):
        '''
            - Calls the '_findLine()' function, to find all of the vertical 
              line coordinates.
            - 'nRows' and 'nColumns' specifies the grid dimensions.
            > Returns a list of sublists; each sublist corresponds to a set of
              line coordinates.
        '''
        return [self._findLine(0, cc, nRows, nColumns, 1, 0) for cc in range(nColumns)]
            
    def _getDiagonalNE(self, nRows, nColumns):
        '''
            - Calls the '_findLine()' function, to find all of the diagonal line
              coordinates from bottom left to top right.
            - 'nRows' and 'nColumns' specifies the grid dimensions.
            > Returns a list of sublists; each sublist corresponds to a set of
              line coordinates.
        '''
        lineListV = [self._findLine(rr, 0, nRows, nColumns, -1, 1) for rr in range(nRows)]
        lineListH = [self._findLine(nRows -1, cc, nRows, nColumns, -1, 1) for cc in range(1, nColumns)]
        return lineListV + lineListH
    
    def _getDiagonalSW(self, nRows, nColumns):
        '''
            - Calls the '_findLine()' function, to find all of the diagonal line
              coordinates from top right to bottom left.
            - 'nRows' and 'nColumns' specifies the grid dimensions.
            > Returns a list of sublists; each sublist corresponds to a set of
              line coordinates.
        '''
        lineListV = [self._findLine(rr, 0, nRows, nColumns, 1, 1) for rr in range(nRows)]
        lineListH = [self._findLine(0, cc, nRows, nColumns, 1, 1) for cc in range(1, nColumns)]
        return lineListV + lineListH