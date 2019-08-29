#!/usr/bin/python3

import sys
from pyminesweeper.core import MineField
from enum import Enum, unique

class Game:

    @unique
    class GameAction(Enum):
        REVEAL = 10
        FLAG = 20

    @unique
    class GameStatus(Enum):
        NOT_RUNNING = 0
        RUNNING = 1
        FAILED = -1
        WON = 2

    def __init__(self, row, col, num_mines, end_program_when_game_finishes = True):

        self._minefield = MineField.create_new(row, col, num_mines)
        self._shut_down_when_finished = end_program_when_game_finishes
        self._status = Game.GameStatus.NOT_RUNNING

    @property
    def minefield(self):
        return self._minefield

    @property
    def is_running(self):
        return self._status == Game.GameStatus.RUNNING

    @property
    def status(self):
        return self._status
    

    def start_game(self):
        if self._minefield.initialise():
            self._status = Game.GameStatus.RUNNING
        else:
            raise Exception("Game Failed to Start. MineField Initialising Failed.")

    def play_move(self, row, col, action):
        '''
            Args:
                action: if action is Game.GameAction.REVEAL, cell at [row,col] is revealed 
                        if action is Game.GameAction.FLAG, cell at [row,col] is flagged/unflagged

        '''

        if self._status == Game.GameStatus.RUNNING:
            if action == Game.GameAction.FLAG:
                self._minefield.flag_cell(row,col)

            elif action == Game.GameAction.REVEAL:
                self._minefield.reveal_cells(row, col)

                if not self._minefield.is_intact:
                    self._status = Game.GameStatus.FAILED
                elif self._minefield.revealed_all_safe_cells:
                    self._status = Game.GameStatus.WON

                if self._shut_down_when_finished:
                    if self._status == Game.GameStatus.FAILED:
                        print("Game Over: Cell at [%d,%d] was a mine!"%(row,col))
                        sys.exit()
                    elif self._status == Game.GameStatus.WON:
                        print ("\n\tGame Won!\n")
                        sys.exit()
            else:
                raise Exception("Unknown Action requested")

        else:
            raise Exception("Game is not running!")

        return self._status


if __name__ == '__main__':
    
    game = Game(5,5,5, False)
    game.start_game()

    print(game.minefield)

    game.play_move(1,1,Game.GameAction.FLAG)

    print(game.minefield)
