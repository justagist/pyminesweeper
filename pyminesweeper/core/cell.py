#!/usr/bin/python3

class Cell(object):
    def __init__(self, is_mine, is_visible=False, is_flagged=False):
        self.is_mine = is_mine
        self.is_visible = is_visible
        self.is_flagged = is_flagged

        self.number = None # Number of mines in the neighbourhood

    def show(self):
        self.is_visible = True

    def flag(self):
        self.is_flagged = not self.is_flagged

    def _place_mine(self):
        self.is_mine = True

    def __str__(self):

    	return "X" if self.is_mine else ":"

