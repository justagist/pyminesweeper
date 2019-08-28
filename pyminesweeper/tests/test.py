
from pyminesweeper.core import Game


if __name__ == '__main__':
	
	game = Game(row=10, col=10, num_mines=12)

	print (game.minefield.num_rows)
	print (game.minefield._num_mines)

	print (game.minefield._mine_locations)

	# print ([cell.value for cell in row for row in game.minefield]) 
	# for row in game.minefield:
	# 	for cell in row:
	# 		print(cell.number)