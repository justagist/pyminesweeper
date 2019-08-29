
import random

class Cell(object):
    def __init__(self, is_mine, is_visible=False, is_flagged=False):
        self._is_mine = is_mine
        self.is_visible = is_visible
        self.is_flagged = is_flagged

        self._number = None # Number of mines in the neighbourhood

    def show(self):
        self.is_visible = True
        if not self._is_mine:
            self.is_flagged = False

    def flag(self):
        if not self.is_visible:
            self.is_flagged = not self.is_flagged

    def _place_mine(self):
        self._is_mine = True

    def get_number(self):
        if self.is_visible:
            return self._number
        else:
            return None

    def __str__(self):
        if self.is_flagged:
            return 'F'
        if self.is_visible:
            if self._is_mine:
                return 'X'
            else:
                return str(self._number)
        return ' '

    def __repr__(self):

        return self.__str__()



class MineField(tuple):

    '''
        An object of this class (the return value itself) is a list of list (representing the minefield) of strings with each value in the list being either 'F' for 'flagged' cells, 'X' for revealed mines, a number (as string) for revealed cells, '  ' for hidden cells.

    '''


    def __init__(self, tup):
        ''' 
            Create a blank grid

        '''
        super().__init__()

        assert len(self) > 0, "Invalid size for board. Num of rows: %d"%len(self)

        self.num_rows = len(self)
        self.num_cols = len(self[0])

        assert self.num_rows == self.num_cols, "Invalid size for board. Num of rows: %d, Num of cols: %d"%(self.num_rows, self.num_cols)

        self.revealed_safe_cells = 0
        self._num_mines = 0
        self._mine_locations = []
        self._is_playing = False

    def _place_mine_at(self, row, col):
        if not self._is_playing:
            if not self[row][col]._is_mine:
                self[row][col]._place_mine()
                self._mine_locations.append([row,col])
                self._num_mines += 1
        else:
            raise Exception("Error: Should not add mine after initialising MineField!")

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

    def initialise(self):
        '''
            Has to be run before running the game.

        '''
        if not self._is_playing and self._num_mines > 0 and self._num_mines <= (self.num_rows*self.num_cols - 4) and self._num_mines == len(self._mine_locations):  
            self.safe_cells = self.num_rows*self.num_cols - self._num_mines

            for r in range(self.num_rows):
                for c in range(self.num_cols):
                    if not self[r][c]._is_mine:
                        self[r][c]._number = self._count_surrounding(r,c)

            self._is_playing = True
        else:
            print ("Error while Initialising MineField: Check number of mines!")
        return self._is_playing

    def _count_surrounding(self, row_id, col_id):
        return sum(1 for (surr_row, surr_col) in self._get_neighbours(row_id, col_id)
                        if (self._is_inside_field(surr_row, surr_col) and
                            self[surr_row][surr_col]._is_mine))

    def _get_neighbours(self, row_id, col_id):
        SURROUNDING = ((-1, -1), (-1,  0), (-1,  1),
                       (0 , -1),           (0 ,  1),
                       (1 , -1), (1 ,  0), (1 ,  1))
        return ((row_id + surr_row, col_id + surr_col) for (surr_row, surr_col) in SURROUNDING)

    def _is_inside_field(self, row_id, col_id):
        return 0 <= row_id < self.num_rows and 0 <= col_id < self.num_cols

    def reveal_cells(self, row_id, col_id):
        '''
            A recursive method to reveal safe cells.
            Reveals the selected cell. If it is safe, and has no mines around it, adjacent cells are revealed.
            If the selected cell is a mine, game is over.

        '''
        cell = self[row_id][col_id]
        if not cell.is_visible:
            self[row_id][col_id].show()
            self.revealed_safe_cells += 1

            if (cell._is_mine):
                assert [row_id,col_id] in self._mine_locations
                self.stop_play()
                self.revealed_safe_cells -= 1

            elif self[row_id][col_id]._number == 0:
                for (surr_row, surr_col) in self._get_neighbours(row_id, col_id):
                    if self._is_inside_field(surr_row, surr_col):
                        self.reveal_cells(surr_row, surr_col) 

    def flag_cell(self, row_id, col_id):

        self[row_id][col_id].flag()

    # @property
    # def current_state():
    #     return []
    def stop_play(self):
        self._is_playing = False

    def reveal_all(self, only_mines = True):

        if not self._is_playing:
            for r in range(self.num_rows):
                for c in range(self.num_cols):
                    if self[r][c]._is_mine:
                        self[r][c].show()
        else:
            raise Exception("Cannot reveal all cells when still in play. End game using stop_play() method (of MineField class) if required.")


    @classmethod
    def create_new(cls, row, col, num_mines):
        ''' 
            Creates a 'row' x 'col' grid with 'num_mines' number of mines at random location (except at the corners)

        '''
        board = cls(tuple([tuple([Cell(False) for i in range(row)])
                         for j in range(col)]))

        board._place_random_mines(num_mines)

        return board

    @property
    def is_intact(self):
        return self._is_playing

    @property
    def revealed_all_safe_cells(self):
        return self.revealed_safe_cells == self.safe_cells

    def __str__(self):
        '''
            To String method: shows minefield row by row, including flags and revealed cells.
            Flagged cells are marked 'F'
            Mines are marked 'X'

        '''
        retval = ''
        for row in self:
            retval += str(row) + '\n'

        return retval
    


if __name__ == '__main__':
    

    field = MineField.create_new(5,5,5)
    field.initialise()

    print (field)

    # field.flag_cell(1,1)

    field.reveal_cells(0,0)

    print (field)
