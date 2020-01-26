import sys
import random

#Exit flag
exit = ('EXIT')

#Board class
class Board:

    """
    n is dimensions width/height
    mines is list of coordinates (tuples) that are mines
    board is list of list (2D list) of game board
    ■ is covered/untouched square
    . is uncovered/empty square
    M is uncovered mine
    """
    def __init__(self, n, num_mines):
        #stores the dimension of nxn board as n
        self.n = n
        #list of coordinate tuples that represent mines
        self.mines = []
        #list of coordinate tuples that represent flagged cells
        self.flag = []
        #list of coordinate tuples that are numbered (have at least one mine next to them)
        self.numbers = []
        #2D list of values representing board. [row][col] represent location of cell in the board, value represents displayed value
        self.board = []
        #AM I DEAD!?
        self.exploded = False
        #initialize everything to untouched tile piece
        for _ in range(n):
            self.board.append(['\u25A0'] * n)
        #open represents all untouched squares that are safe to open
        #starts off as list of all coordinate tuples in board
        self.open = []
        for row in range(n):
            for col in range(n):
                self.open.append((row, col))
        #randomly choose coordinate tuples to be mines, move it to the mines list and out of open list
        for mine in range(num_mines):
            self.mines.append(self.open.pop(random.randint(0, len(self.open)-1)))

    #str representation of the board, printed in 2D board
    def __str__(self):
        rt_str = ''
        for row in range(self.n):
            for square in range(self.n):
                rt_str = rt_str + str(self.board[row][square]) + ' '
            rt_str = rt_str[:-1] + '\n'
        return rt_str[:-1]

    def get_flagged(self):
        return self.flag

    def get_covered(self):
        return self.open + self.mines

    def get_numbers(self):
        return self.numbers

    #given a coordinate tuple, update the board
    #return true if play continues and moves on to next turn
    #return false if hit mine or if all empty squares are cleared
    def update(self, move):
        if isinstance(move, str) and move.upper() == exit:
            return exit
        else:
            #check whether the update is a flag move or not
            flag = False
            if move[0] == 'F':
                flag = True
                print('flag')
                move = move[1:]
                print(move)
            row, col = move
            #check if given move is flag move or not
            if flag:
                #cell could be in open, in that case, move cell from open to flagged
                if move in self.open:
                    self.board[row][col] = '\u2690'
                    print('row {0} and col {1} has been flagged'.format(row+1, col+1))
                    self.flag.append(move)
                    self.open.remove(move)
                #cell could be in flag, in that case, move cell from flagged to open
                elif move in self.flag:
                    self.board[row][col] = '\u25A0'
                    print('row {0} and col {1} has been UN-flagged'.format(row+1, col+1))
                    self.open.append(move)
                    self.flag.remove(move)
                #finally, cell could be in mines, in that case, flag cell but don't do anything else
                elif move in self.mines:
                    self.board[row][col] = '\u2690'
                    print('row {0} and col {1} has been flagged'.format(row+1, col+1))
                    self.flag.append(move)
                else:
                    print('the cell at {0} has already been uncovered'.format(move))
                print(self)
                return True
            #check that given move is not a mine (return False if it is a mine)
            if move in self.mines:
                for mine in self.mines:
                    r, c = mine
                    self.board[r][c] = 'M'
                print('YOU DIED')
                self.exploded = True
                return False
            #from there, use queue to branch out and uncover surrounding cells
            queue = []
            queue.append(move)
            #if the move is called on a previously opened cell, move on and ask for next move
            if move not in self.open:
                print("The cell at row {0} and col {1} has already been uncovered".format(row+1, col+1))
                return True
            #return list of numbered cells
            rt_list = []
            while queue:
                cur_coordinate = queue.pop(0)
                #check if the current coordinate is still covered and untouched
                if cur_coordinate in self.open:
                    #each cell checks the 8 or less cells around it for mines
                    #keep count of number of mines in those surrounding cells
                    mine_count = 0
                    surrounding = get_surrounding(cur_coordinate, self.n-1)
                    for coordinate in surrounding:
                        if coordinate in self.mines:
                            mine_count = mine_count + 1
                    #if count > 0, set coordinate to count
                    if mine_count:
                        self.board[cur_coordinate[0]][cur_coordinate[1]] = mine_count
                        self.numbers.append((cur_coordinate[0], cur_coordinate[1]))
                        rt_list.append(cur_coordinate)
                    #if count == 0, set coordinate to '.', add surrounding cells to queue (only uncover more if zero, borders of space should be numbers)
                    else:
                        self.board[cur_coordinate[0]][cur_coordinate[1]] = '.'
                        queue.extend(surrounding)
                    #each time "uncover a cell", remove from self.open
                    self.open.remove(cur_coordinate)                    
            #print the board
            print(self)
            #if there are no more open spaces, signal to end the game
            if not self.open:
                return False
            return rt_list

#return list of all tuples of surrounding cells
def get_surrounding( coordinate, N):
    row, col = coordinate
    surrounding = []
    poss_rows = [row]
    if row < N:
        poss_rows.append(row+1)
    if row > 0:
        poss_rows.append(row-1)
    if col < N:
        surrounding.extend([(r, col+1) for r in poss_rows])
    if col > 0:
        surrounding.extend([(r, col-1) for r in poss_rows])
    surrounding.extend([(r, col) for r in poss_rows])
    surrounding.remove((row, col))
    return surrounding

    #return [(row,col+1),(row,col-1), (row-1,col-1),(row-1,col),(row-1,col+1), (row+1,col-1),(row+1,col),(row+1,col+1)]
    
#return coordinate tuple if conditions are met
#must be within boundaries
#must be int
def get_move(N):
    input_list = input().split()
    #check to see if input is exit keyword
    #if only one input, invalid, try again
    if len(input_list) == 1:
        if isinstance(input_list[0], str) and input_list[0].upper() == exit:
            return exit
        else:
            print("Please enter a ROW and a COLUMN")
            return get_move(N)
    #check to see if it's a flag move
    flag = False
    if len(input_list) > 3:
        print("Please specify a move by inputing a row and column as such \n1 2 or F 1 2")
        return get_move(N)
    if isinstance(input_list[0], str) and input_list[0].upper() == 'F':
        flag = True
        input_list = input_list[1:]

    #needs two input, check more conditions
    if len(input_list) != 2:
        print("Please specify a move with two number representing the row and then the column of the cell you want to update")
        return get_move(N)
    #check both inputs are numbers
    elif not (input_list[0].isnumeric() and input_list[1].isnumeric()):
        print("Rows and columns must be specified by integers")
        return get_move(N)
    row = int(input_list[0])
    col = int(input_list[1])
    #check row and column input are both in range
    if not (row > 0 and row <= N and col > 0 and col <= N):
        print("Each coordinate must be in the range 1 <= N <= {0}".format(N))
        return get_move(N)
    #return coordinate tuple
    if flag:
        return ('F', row-1, col-1)
    return (row-1, col-1)

#prompt is a print statement
#num_input is number of input parameters
    #if 1, either N,M or EXIT
    #if 2, uncover a cell
    #if 3, flag a cell
#conditions is a dictionary
    #keys are lambda functions to test (return the condition applied to the value or False)
    #values are print statements to return
def get_input(prompt, num_input, conditions):
    if prompt:
        print(prompt)
    input_list = input().split()[:num_input]
    if input_list[0].upper() == 'EXIT':
        return exit
    if len(input_list) != num_input:
        print('IMPROPER NUMBER OF PARAMETERS')
        return get_input('', num_input, conditions)
    for condition in list(conditions.keys()):
        for sys_index in range(len(input_list)):
            test = condition(input_list[sys_index])
            if not test and test is not 0:
                print(conditions[condition])
                return get_input(prompt, num_input, conditions)
            input_list[sys_index] = test
    if num_input == 1:
        return input_list[0]
    return tuple(input_list)

def run():
    #exit keyword it 'EXIT'
    print("ENTER 'EXIT' AT ANY TIME TO ESCAPE")
    """
    print("Enter the dimension of the square board:")
    #get a valid N (dimensions of square board)
    validN = False
    N = "DEFAULT VALUE"
    while not validN:
        N = input().split()[0]
        if N == 'EXIT':
            return "EXIT"
        if not N.isnumeric():
            print("Please enter a number")
            continue
        N = int(N)
        if N > 100:
            print("Please choose a smaller number")
            continue
        validN = True
    print("The board will be {0} by {0}".format(N))
    #get a valid M (number of mines). must be less than N*N
    print("Enter how many mines you want:")
    validM = False
    M = "DEFAULT VALUE"
    while not validM:
        M = input().split()[0]
        if M == 'EXIT':
            return "EXIT"
        if not M.isnumeric():
            print("Please enter a number")
            continue
        M = int(M)
        if M >= N*N:
            print("There must be less mines than cells on the square")
            continue
        validM = True
    print("There are {0} mines on the board".format(M))
    """
    #getting a valid N (dimensions of board)
    #tested if N is a number and less than 100
    N = get_input('Please enter the dimensions of the square board:', 1, 
        {lambda n: int(n) if n.isnumeric() else False : 'Please enter a number:', 
        lambda n: n if n <= 100 else False : 'Please enter a number less than 100'})
    if N == exit:
        return 'EXIT'
    print("The board will be {0} by {0}".format(N))
    #getting a valid M (number of mines)
    #tested if M is a number and less than N^2
    M = get_input('Please enter the number of mines to be placed on the board:', 1,
        {lambda m: int(m) if m.isnumeric() else False : 'Please enter a number:',
        lambda m: m if m < N*N else False : 'There must be less mines than cells on the board:'})
    if M == exit:
        return 'EXIT'
    print("There are {0} mines on the board. You win when you've uncovered all cells that don't contain mines.".format(M))

    #initialize game board
    game_board = Board(N, M)
    print("Rows and columns are from 1 to {0}".upper().format(N))
    print(game_board)
    print("Enter the row and column to begin (You can't blow up immediately, so have no fear):")
    #get initial move, check if exit keyword
    initial_move = get_move(N)
    if initial_move != 'EXIT':
        #if the first move is a mine
        #move the mine to the upper left corner
        #if the upper left is occupied, move to the right
        if initial_move in game_board.mines:
            new_mine = (0,0)
            while new_mine in game_board.mines:
                if new_mine[1]+1 == game_board.n:
                    new_mine = (new_mine[0]+1, 1)
                else:
                    new_mine = (new_mine[0], new_mine[1]+1)
            game_board.open.append(initial_move)
            game_board.mines.remove(initial_move)
            game_board.mines.append(new_mine)
            game_board.open.remove(new_mine)
        #continues to call update until update returns False
        go = game_board.update(initial_move)
        print("Please enter next move")
        while go:
            go = game_board.update(get_move(N))
            if go == 'EXIT':
                return 'EXIT'
            if go:
                print("Please enter next move, there are {0} empty spaces left".format(len(game_board.open)))
        #if done, check if win or loss
        #if not game_board.open, list of safe and untouched cells is empty, return win
        if not game_board.exploded:
            print("YOU WIN")
        else:
            print("BOOM BIG EXPLOSION I'M SORRY")
            print(game_board)
    else:
        return 'EXIT'

if __name__ == "__main__":
    run()

    sys.exit(0)
