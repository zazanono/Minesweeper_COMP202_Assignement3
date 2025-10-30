import random

EASY_DIFFICULTY = 0.1
MEDIUM_DIFFICULTY = 0.3
HARD_DIFFICULTY = 0.5


def init_board(nb_rows, nb_cols, value):
    matrix = []

    for i in range(nb_rows):
        matrix.append([])
        for j in range(nb_cols):
            matrix[i].append(value)

    return matrix


def count_total(board, value):
    count = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == value:
                count += 1
    return count


def is_valid_position(board, row, col):
    return 0 <= row < len(board) and 0 <= col < len(board[0])


def get_neighbour_positions(board, row, col):
    neighbour_positions = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if (is_valid_position(board, row + i, col + j)
                    and (i != 0 or j != 0)):

                neighbour_positions.append([row + i, col + j])

    return neighbour_positions


def count_neighbours(board, row, col, value):
    neighbours = get_neighbour_positions(board, row, col)

    count = 0

    for pos in neighbours:
        if board[pos[0]][pos[1]] == value:
            count += 1

    return count


def new_mine_position(board):
    invalid_mine_pos = True

    while invalid_mine_pos:
        rand_row = random.randint(0, len(board)-1)
        rand_col = random.randint(0, len(board[0])-1)

        if board[rand_row][rand_col] != -1:
            board[rand_row][rand_col] = -1
            invalid_mine_pos = False


def generate_helper_board(nb_rows, nb_cols, nb_mines):
    board = init_board(nb_rows, nb_cols, 0)
    for _ in range(nb_mines):
        new_mine_position(board)

        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] != -1:
                    board[i][j] = count_neighbours(board, i, j, -1)

    return board


def flag(board, row, col):
    if board[row][col] == "?":
        board[row][col] = "\u2691"

    if board[row][col] != "\u2691":
        board[row][col] = "?"


def reveal(helper_board, game_board, row, col):
    if helper_board[row][col] == -1:
        raise AssertionError("BOOM! You lost.")
    else :
        game_board[row][col] = helper_board[row][col]


def print_board(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            print(board[i][j], end=" ")
        print("")


def init_game(difficulty, num_cols, num_rows):
    if difficulty == "EASY":
        difficulty = EASY_DIFFICULTY
    elif difficulty == "MEDIUM":
        difficulty = MEDIUM_DIFFICULTY
    elif difficulty == "HARD":
        difficulty = HARD_DIFFICULTY

    num_mines = int(difficulty * num_rows * num_cols)

    helper_board = generate_helper_board(num_rows, num_cols, num_mines)
    game_board = init_board(num_rows, num_cols, '?')

    return game_board, helper_board, num_mines


def is_game_over(game_board, helper_board):

    for i in range(len(game_board)):
        for j in range(len(game_board[i])):
            if game_board[i][j] == '?' or helper_board[i][j] == '\u2691':
                if helper_board[i][j] != -1:
                    return False

    return True


def play():
    num_rows = int(input("Enter number of rows for the board: "))
    num_cols = int(input("Enter number of columns for the board: "))
    difficulty = input("Enter difficulty: ")
    game_board, helper_board, num_mines = (
        init_game(difficulty, num_cols, num_rows))

    print_board(helper_board)

    game_over = False
    while not game_over:
        curr_mines = num_mines - count_total(game_board, "\u2691")

        print("Current Board: (" + str(curr_mines) + " Mines remaining)")
        print_board(game_board)

        chosen_move = int(input("Choose 0 to reveal or 1 to flag: "))
        chosen_row = int(input("Which row? "))
        chosen_col = int(input("Which column? "))

        if chosen_move == 0:
            reveal(helper_board, game_board, chosen_row, chosen_col)
        elif chosen_move == 1:
            flag(game_board, chosen_row, chosen_col)

        game_over = is_game_over(game_board, helper_board)

    print("Congratulations! You won!")
    print("Final Board:")
    print_board(game_board)


if __name__ == "__main__":
    random.seed(202)
    play()