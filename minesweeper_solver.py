import sys
from minesweeper import Board
from minesweeper import get_surrounding
import random
from timeit import default_timer


def autosolver(board):
	start = default_timer()

	N = board.n
	#starting move
	solving = True
	numbers = board.update((0,0))
	while type(numbers) == bool:
		board = Board(N,N)
		numbers = board.update((0,0))
	#row and col are in 0 index
	covered = board.get_covered()
	flagged = []
	#do i still need visited if I'm popping from a queue? prolly not
	visited = [[False] * 10] * 10
	#stop infinite looping
	max_moves = N*N

	while solving:
		if max_moves == 0:
			break
		#next list of numbered cells
		next_level = []
		#default needs a random variable
		need_random = True
		while numbers:
			if board.exploded:
				solving = False
				break
			#queue, FILO
			cur_coordinate = numbers.pop(0)
			#number of mines surrounding
			value = board.board[cur_coordinate[0]][cur_coordinate[1]]
			#get surrounding cells
			surrounding = get_surrounding(cur_coordinate, N)
			#track flagged cells and covered cells
			flagged_cells = []
			covered_cells = []
			for surrounding_cell in surrounding:
				if surrounding_cell in flagged:
					flagged_cells.append(surrounding_cell)
				elif surrounding_cell in covered:
					covered_cells.append(surrounding_cell)
			#4 cases given num_flagged cells and num_covered cells
			num_flagged = len(flagged_cells)
			num_covered = len(covered_cells)
			#no covered cells around cur_coordinate, don't care about this cell, don't add to keeper list
			if num_flagged + num_covered != 0:
				#if num_flagged + num_covered == num_mines (value), that means that all the covered cells around cur_coordinate are mines
				if num_flagged+num_covered == value:
					for mine in covered_cells:
						#flagging only covers a cell, should be removed from covered cells
						board.update(('F', mine[0], mine[1]))
						flagged.append(mine)
						covered.remove(mine)
						need_random = False
				#if num_flagged == num_mines (value), that means all the covered cells around cur_coordinate are safe to uncover
				elif num_flagged == value:
					for safe in covered_cells:
						#since there are new numbered cells coming out, add to list
						result = board.update((safe[0], safe[1]))
						covered.remove(safe)
						if result:
							#if result is True it measn teh cell was already uncovered
							if type(result) is list:
								next_level.extend(result)
						else:
							solving = False
						need_random = False
					if not solving:
						break
				else:
					#if no guaranteed update from this coordinate, throw cur_coorindate back into numbers
					next_level.append(cur_coordinate)
		#checked all border cells by now
		#if solving is false, break out
		if solving == False:
			break
		#if need_random is still true, have to guess
		if need_random:
			result = board.update(covered[random.randint(0, len(covered)-1)])
			if result:
				#if result is True it measn teh cell was already uncovered
				if type(result) is bool:
					solving = result
				else:
					next_level.extend(result)
		numbers.extend(next_level)
		next_level = []
		max_moves -= 1


	end = default_timer()
	return end-start
"""
def autosolver(board):
	start = default_timer()

	N = board.n
	#starting move
	solving = True
	board.update((0,0))
	#row and col are in 0 index
	numbers = board.get_numbers()
	covered = board.get_covered()
	flagged = []
	visited = [[False] * 10] * 10
	while solving:
		#default belief is that no guaranteed move is available
		need_random = True
		#check each numbered cell
		for numbered_cell in numbers:
			row, col = numbered_cell
			if visited[row][col]:
				continue
			#get the value of the numbered cell
			num_mines = board.board[row][col]
			#get all surrounding cells
			surrounding = get_surrounding(numbered_cell, N-1)
			num_surrounding = 0
			#how many covered spaces are surrounding the numbered space
			covered_surrounding = []
			for surrounding_cell in surrounding:
				if surrounding_cell in covered:
					num_surrounding = num_surrounding + 1
					covered_surrounding.append(surrounding_cell)
			if num_surrounding == 0:
				visited[row][col] = True
				continue
			#if number of surrounding covered spaces = number of mines around or there are less covered spaces than the number value, flag them
			if num_surrounding <= num_mines:
				#expansion is possible
				need_random = False
				#flag all the confirmed mines
				for mine in covered_surrounding:
					#flag mine if necessary
					if mine not in flagged:
						board.update(('F', mine[0], mine[1]))
						flagged.append(mine)
					#for each cell surrounding the mine, if all mines in their surroundings have been flagged, uncover all the other cells around them
					#NEEDS VERIFICATION SO AS TO NOT GO OUT OF BOUNDS (0,0) not handled by get_surrounding
					#get the cells surrounding the mines
					surrounding_mine = get_surrounding(mine, N-1)
					for s_m in surrounding_mine:
						#if a cell surrounding the mine is the current number cell or still covered, move on
						if s_m == numbered_cell or s_m in covered:
							continue
						#if a cell surrounding the mine is uncovered and not the current mine
						expansion = get_surrounding(s_m, N-1)
						#if the length of the overlap between the cells surrounding the cell next to the mine and the list of flagged cells
						#is the smame as the value of the cell next to the confirmed mine
						if len(expansion and flagged) == board.board[s_m[0]][s_m[1]]:
							#update all non-flagged cells surrounding the cell next to the mine
							for exp in expansion:
								if exp not in flagged:
									solving = board.update(exp)
		#checked all border cells by now
		#if need_random is still true, have to guess
		if need_random:
			solving = board.update(covered[random.randint(0, len(covered)-1)])

		numbers = numbers + list(set(board.get_numbers())-set(numbers))
		visited[row][col] = True

	end = default_timer()
	return end-start
"""

def run():
	total_time = 0
	boards_solved = 0
	for _ in range(100000):
		#board is 10x10 with 10 mines
		board = Board(10, 10)
		solve = autosolver(board)
		#print(board)
		#print('done')
		if not board.exploded:
			print('HOLY SHIT solved')
			boards_solved = boards_solved + 1
		#else:
			#print('fucked up')
		total_time = total_time + solve
	print("Solve {0} boards out of 100,000 with an total time of {1}".format(boards_solved, total_time))
	#Solve 27072 boards out of 100,000 with an total time of 689.9646616750006

if __name__ == "__main__":
	run()
	sys.exit(0)