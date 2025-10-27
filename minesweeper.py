import random


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


if __name__ == "__main__":
    random.seed(202)
    print(generate_helper_board(7, 7, 0) == init_board(7, 7, 0))

    print('\u2691')
