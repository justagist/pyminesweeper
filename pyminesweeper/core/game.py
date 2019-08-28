
import random
import numpy as np
from pyminesweeper.core import Cell


class Board(tuple):


    def __init__(self, tup):
        ''' 
            Create a blank grid

        '''
        super().__init__()

        assert len(self) > 0, "Invalid size for board. Num of rows: %d"%len(self)

        self.num_rows = len(self)
        self.num_cols = len(self[0])

        assert self.num_rows == self.num_cols, "Invalid size for board. Num of rows: %d, Num of cols: %d"%(self.num_rows, self.num_cols)

        self._num_mines = 0
        self._mine_locations = []
        self._board_ready = False

    def _place_mine_at(self, row, col):

        if not self[row][col].is_mine:
            self[row][col]._place_mine()
            self._mine_locations.append([row,col])
            self._num_mines += 1

    def _place_random_mines(self, num_mines):

        xy = [] 
        while self._num_mines < num_mines: 
            x = random.randint(0,self.num_rows-1)
            y = random.randint(0,self.num_cols-1)
            xy.append([x,y]) 
            if xy.count([x,y]) > 1: 
                xy.remove([x,y]) 
            elif (x == 0 and y == 0) or (x == 0 and y == self.num_cols-1) or (x == self.num_rows-1 and y == 0) or (x == self.num_rows-1 and y == self.num_cols-1):
                xy.remove([x,y])
            else: 
                self._place_mine_at(x, y)

    def _initialise(self):
        '''
            Has to be run before running the game.

        '''
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if not self[r][c].is_mine:
                    self[r][c].number = self._count_surrounding(r,c)

        self._board_ready = True

    def _count_surrounding(self, row_id, col_id):
        return sum(1 for (surr_row, surr_col) in self._get_neighbours(row_id, col_id)
                        if (self._is_inside_field(surr_row, surr_col) and
                            self[surr_row][surr_col].is_mine))

    def _get_neighbours(self, row_id, col_id):
        SURROUNDING = ((-1, -1), (-1,  0), (-1,  1),
                       (0 , -1),           (0 ,  1),
                       (1 , -1), (1 ,  0), (1 ,  1))
        return ((row_id + surr_row, col_id + surr_col) for (surr_row, surr_col) in SURROUNDING)

    def _is_inside_field(self, row_id, col_id):
        return 0 <= row_id < self.num_rows and 0 <= col_id < self.num_cols


    @classmethod
    def create_new(cls, row, col, num_mines):
        ''' 
            Creates a 'row' x 'col' grid with 'num_mines' number of mines at random location (except at the corners)

        '''
        board = cls(tuple([tuple([Cell(False) for i in range(row)])
                         for j in range(col)]))

        board._place_random_mines(num_mines)

        board._initialise()

        return board


class Game:

    def __init__(self, row, col, num_mines):

        self._minefield = Board.create_new(row, col, num_mines)
        self._game_on = True

    @property
    def minefield(self):
        return self._minefield
    


