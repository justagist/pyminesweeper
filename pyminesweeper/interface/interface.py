
from pyminesweeper.core import Game


class GameInterface:
	'''
		Base for interface classes to solve a PyMinesweeper Minefield.
		Requires sending a Game instance of a defined minefield. See Example below.

	'''

	def __init__(self, game_instance):

		self._game = game_instance
		self._game.start_game()


	def get_input(self):
		'''
			Has to be implemented in derived class

			@Return -- something meaningful (for example):
				row: integer representing row in minefield
				col: integer representing col in minefield
				action: A GameAction enum value representing action to perform at [row,col] (GAME.GameAction.REVEAL / GAME.GameAction.FLAG)

		'''
		raise NotImplementedError

		# return row, col, action

	def run(self):
		'''
			Override in derived class if required

		'''
		assert self._game.status != Game.GameStatus.NOT_RUNNING, "Error: Game is not Running!"

		print(self._game.minefield)

		while self._game.status == Game.GameStatus.RUNNING:

			row, col, action = self.get_input()

			self._game.play_move(row,col, action)

			print(self._game.minefield)

		if self._game.status == Game.GameStatus.FAILED:
			self.game_lost()

		elif self._game.status == Game.GameStatus.WON:
			self.game_won()

	def game_won(self):
		'''
			Override in derived class if required

		'''
		print ("Yaay! Game Won!")

	def game_lost(self):
		'''
			Override in derived class if required

		'''
		self._game.end_and_reveal_field(only_mines=True)
		print ("You lost!\n\nSolution:\n%s"%str(self._game.minefield))






