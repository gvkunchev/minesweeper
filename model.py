import os
import random

from enum import Enum
from itertools import product as itertool_product


class Content(Enum):
    '''Represent a cell content (aka value).'''
    empty = 0
    mine = 9
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8


class Cell:
    '''Minesweeper cell.'''

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shown = False
        self.marked = False
        self.content = Content.empty


class Table:
    '''Minesweeper table.'''

    def __init__(self, width, height, mine_count):
        '''Constructor.'''
        self.width = width
        self.height = height
        self.mine_count = mine_count
        self.cells = []
        self._init_cells()
        self._place_mines()
        self._assign_content()

    def _init_cells(self):
        '''Initiate cells in the table.'''
        for x in range(self.width):
            self.cells.append([])
            for y in range(self.height):
                self.cells[-1].append(Cell(x, y))

    def _place_mines(self):
        '''Place mines randomly.'''
        coordinates = list(itertool_product(range(self.width),
                                            range(self.height)))
        random.shuffle(coordinates)
        for x, y in coordinates[:self.mine_count]:
            self.cells[x][y].content = Content.mine

    def get_neightbours(self, cell):
        '''Get neighbours of a particulra cell.'''
        for offset_x in (-1, 0, 1):
            for offset_y in (-1, 0, 1):
                if (offset_x, offset_y) == (0, 0):
                    continue # The cell itself
                pos_x = cell.x + offset_x
                pos_y = cell.y + offset_y
                if pos_x < 0 or pos_x > self.width - 1:
                    continue # Table overflow
                if pos_y < 0 or pos_y > self.height - 1:
                    continue # Table overflow
                yield self.cells[cell.x + offset_x][cell.y + offset_y]

    def _assign_content(self):
        '''Assign content based on mine position.'''
        for x in range(self.width):
            for y in range(self.height):
                cell = self.cells[x][y]
                if cell.content == Content.mine:
                    continue # Mines are already determined
                value = 0
                for neighbour in self.get_neightbours(cell):
                    if neighbour.content == Content.mine:
                        value += 1
                cell.content = Content(value)

    def __repr__(self):
        '''String representation of the table.'''
        result = ''
        for y in range(self.height):
            result += os.linesep
            cell_list = []
            for x in range(self.width):
                cell_list.append(str(self.cells[x][y].content.value))
            result += '|'.join(cell_list)
        return result


if __name__ == '__main__':
    pass