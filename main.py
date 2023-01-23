from random import choice


def determine_starter() -> str:
	'''
	This function will randomly determine who should start the game.
	'''

	players = ('computer', 'player')
	return choice(players)

def print_board(board: list) -> None:
	'''
	This function will show the board at the beginning of the game and after each player has
	made a move. Player's spaces are shown by X, computer's spaces are shown by O and unoccupied
	spaces have numbers.
	'''

	print('Current board:')
	for i in range(9):
		if (i + 1) % 3 == 0:
			print(board[i])
			if i != 8:
				print('-----')

		else:
			print(board[i], end='|')
	print()

def make_player_move(board: list) -> int:
	'''
	This function will ask the player to choose a space and mark the move of the board if it is
	a valid move.
	'''

	n = input('Choose an unoccupied space: ')

	# Check if user's input can be converted to int
	if n.isdigit():
		n = int(n)

		# Check if user's input is a space in the board
		if 0 <= n <= 8:

			# Check if user's choice isn't occupied by the computer
			if board[n] != 'O':

				# Check if user's choice isn't occupied by themself
				if board[n] != 'X':
					board[n] = 'X'
					return n
				print('You have already made that move.')
				return make_player_move(board)

			print('That space is occupied by your opponent.')
			return make_player_move(board)

		print('Please enter a space from the board (hint: between 0 and 8).')
		return make_player_move(board)

	print('Please enter a valid integer.')
	return make_player_move(board)


def find_winning_move(player: str, board: list) -> int:
	'''
	This function will find which move should a player make to win. It will help the computer
	decide how to win or how to prevent the player from winning.
	'''

	mark = 'O'
	other_mark = 'X'
	if player == 'player':
		mark = 'X'
		other_mark = 'O'

	# Horizontal states
	for i in (0, 3, 6):
		if board[i] == mark:
			if board[i + 1] == mark and board[i + 2] != other_mark:
				return i + 2
			if board[i + 2] == mark and board[i + 1] != other_mark:
				return i + 1
		if board[i] != other_mark:
			if board[i + 1] == mark and board[i + 1] == mark:
				return i

	# Vertical states
	for i in (0, 1, 2):
		if board[i] == mark:
			if board[i + 3] == mark and board[i + 6] != other_mark:
				return i + 6
			if board[i + 6] == mark and board[i + 3] != other_mark:
				return i + 3
		if board[i] != other_mark:
			if board[i + 3] == mark and board[i + 6] == mark:
				return i

	# Diagonal states
	if board[0] == mark:
		if board[4] == mark and board[8] != other_mark:
			return 8
		if board[8] == mark and board[4] != other_mark:
			return 4
	if board[0] != other_mark:
		if board[4] == mark and board[8] == mark:
			return 0

	if board[2] == mark:
		if board[4] == mark and board[6] != other_mark:
			return 6
		if board[6] == mark and board[4] != other_mark:
			return 4
	if board[2] != other_mark:
		if board[4] == mark and board[6] == mark:
			return 2


def has_won(player: str, board: list) -> bool:
	'''
	This function will decide whether a player has won the game after making a move.
	'''

	mark = 'O'
	if player == 'player':
		mark = 'X'

	# Horizontal states
	for i in (0, 3, 6):
		if board[i] == mark:
			if board[i + 1] == mark and board[i + 2] == mark:
				return True

	# Vertical states
	for i in (0, 1, 2):
		if board[i] == mark:
			if board[i + 3] == mark and board[i + 6] == mark:
				return True

	# Diagonal states
	if board[0] == mark:
		if board[4] == mark and board[8] == mark:
			return True

	if board[2] == mark:
		if board[4] == mark and board[6] == mark:
			return True

	# Player hasn't won
	return False


def make_computer_move(board: list) -> int:
	'''
	This function will decide which move the computer should make in different situations.
	'''

	move = None

	# First situation: There exists a single move such that the computer can win the game.
	if move is None:
		move = find_winning_move('computer', board)

	# Second situation: There exists a single move for the player that will cause the computer to lose the game.
	if move is None:
		move = find_winning_move('player', board)

	# Third situation: At least one of the corner spaces (spaces 0, 2, 6, or 8) is free.
	if move is None:
		for space in (0, 2, 6, 8):
			if board[space] not in ('X', 'O'):
				move = space
				break

	# Fourth situation: The center space (space 4) is free.
	if move is None:
		if board[4] not in ('X', 'O'):
			move = 4

	# Fifth situation: At least of the side pieces (spaces 1, 3, 5, or 7) is free.
	if move is None:
		for space in (1, 3, 5, 7):
			if board[space] != 'X' and board[space] != 'O':
				move = space
				break

	board[move] = 'O'
	return move


def main():
	# Define game state
	game_state = 'ongoing'

	# Find starter using determine_starter
	player_turn = determine_starter()

	# Define the message of the finale
	message = ''

	# Create and show the primary board of the game
	board = list(range(9))
	print_board(board)

	# Start the game and taking turns
	while game_state == 'ongoing':

		# The player's turn
		if player_turn == 'player':
			print('It\'s your turn.')

			# Let the player make a move
			move = make_player_move(board)
			print(f'Your move is {move}.')

			# Check if player won with their move
			if has_won('player', board):
				game_state = 'won'
				message = 'You won.'

			# Switch turns
			player_turn = 'computer'

		# The computer's turn
		else:
			print('It\'s computer\'s turn.')

			# Let the computer make a move
			move = make_computer_move(board)
			print(f'Computer\'s move is {move}.')

			# Check if computer won with its move
			if has_won('computer', board):
				game_state = 'won'
				message = 'Computer won.'

			# Switch turns
			player_turn = 'player'

		# Show the board's situation
		print_board(board)

		if board.count('X') + board.count('O') == 9 and not has_won('computer', board) and not has_won('player', board):
			game_state = 'tie'
			message = 'Game ended with a tie.'

	# Show the results
	print(message)


if __name__ == "__main__":
	main()
