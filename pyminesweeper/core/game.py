#!/usr/bin/python3

import sys
from pyminesweeper.core import MineField
from enum import Enum, unique

class Game:

    NOT_RUNNING = 0
    RUNNING = 1
    FAILED = -1
    WON = 2

    def __init__(self, row, col, num_mines, end_program_when_game_finishes = True):

        self._minefield = MineField.create_new(row, col, num_mines)
        self._shut_down_when_finished = end_program_when_game_finishes
        self._game_status = NOT_RUNNING

    @property
    def minefield(self):
        return self._minefield

    @property
    def is_running(self):
        return self._game_status == RUNNING

    @property
    def game_status(self):
        return self._game_status
    

    def start_game(self):
        if self._minefield.initialise():
            self._game_status = RUNNING
        else:
            raise Exception("Game Failed to Start. MineField Initialising Failed.")

    def play_move(self, row, col):

        if self._game_status == RUNNING:
            self._minefield.reveal_cells(row, col)

            if not self._minefield.is_intact():
                self._game_status = FAILED
            else:
                if self._minefield.

            if self._shut_down_when_finished:
                if self._game_status == FAILED:
                    raise Exception("Game Over: Cell at [%d,%d] was a mine!"%(row,col))
                elif self._game_status == WON:
                    print ("\n\tGame Won!\n")
                    sys.exit()
            return self._game_status
        else:
            raise Exception("Game is not running!")
