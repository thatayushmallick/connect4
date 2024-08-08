import numpy as np
import pygame
import sys
import math
import random

# Define colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Define game settings
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)

# Set player order
PLAYER = 0
AI = 1

EMPTY = 0
WINDOW_LENGTH = 4

# Initialize game board
def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

# Drop a piece into the board
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Check if a location is valid for placing a piece
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

# Get the next available row for placing a piece in a column
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# Check if a player has won
def winning_move(board, piece):
    # Check horizontal locations
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Check vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

# Draw the game board
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def is_terminal_node(board):
	return winning_move(board, PLAYER + 1) or winning_move(board, AI + 1) or len(get_valid_locations(board)) == 0

def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER + 1
	if piece == PLAYER + 1:
		opp_piece = AI + 1

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI + 1):
				return (None, 100000000000000)
			elif winning_move(board, PLAYER + 1):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI + 1))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI + 1)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER + 1)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

# Print the game board (for debugging)
def print_board(board):
    print(np.flip(board, 0))

if __name__ == "__main__":
    board = create_board()
    print_board(board)
    game_over = False
    turn = 0

    pygame.init()
    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT + 1) * SQUARESIZE
    size = (width, height)
    screen = pygame.display.set_mode(size)
    draw_board(board)
    pygame.display.update()
    font = pygame.font.SysFont("monospace", 75)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                if turn == PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER + 1)

                        if winning_move(board, PLAYER + 1):
                            label = font.render("You win !", 1, RED)
                            screen.blit(label, (150,10))
                            game_over = True

                        turn += 1
                        turn %= 2

                        print_board(board)
                        draw_board(board)

        if turn == AI and not game_over:				

            col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI + 1)

                if winning_move(board, AI + 1):
                    label = font.render("You Lose !", 1, YELLOW)
                    screen.blit(label, (150,10))
                    game_over = True

                turn += 1
                turn %= 2

                print_board(board)
                draw_board(board)
        
        if game_over:
            pygame.time.wait(3000)