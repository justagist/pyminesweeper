''' 

An Example child class to show the usage of the Interface super class. This class implements an interactive interface using the std out and keyboard input.


    @author: JustaGist (saifksidhik@gmail.com)
    @file: example_keyboard_interface.py
    @package: pyminesweeper v0.9

'''
from pyminesweeper.core import Game
from pyminesweeper.interface import GameInterface

class ExampleKeyboardInterface(GameInterface):

	def get_input(self):
		'''
			Get keyboard input from user in the format: <row> <col> <action>
		'''

		inp =  input("Enter <row> <col> <action>: ").split()

		if len(inp) != 3:
			print("Invalid input. Provide row_id, col_id, and action (R / F) separated by spaces.")
			return self.get_input()

		row = int(inp[0])
		col = int(inp[1])

		if inp[2] == 'r' or inp[2] == 'R':
			action = Game.GameAction.REVEAL 
		elif inp[2] == 'f' or inp[2] == 'F':
			action = Game.GameAction.FLAG
		else:
			print ("Invalid Action: Provide 'R'/'F' as action.")
			return self.get_input()

		return row, col, action



if __name__ == '__main__':
	
	game = Game(row = 3, col = 3, num_mines = 1, end_program_when_game_finishes=False)

	interface = ExampleKeyboardInterface(game)

	interface.run()

