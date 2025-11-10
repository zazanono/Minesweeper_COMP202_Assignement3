import random


# Fraction of cells that will be mines based on difficulty
EASY_DIFFICULTY = 0.1
MEDIUM_DIFFICULTY = 0.3
HARD_DIFFICULTY = 0.5


def init_board(nb_rows, nb_cols, value):
    """
    Create a rectangular game board filled with a given value.

    Parameters:
        nb_rows (int): Number of rows in the board.
        nb_cols (int): Number of columns in the board.
        value (any): Initial value stored in every cell.

    Returns:
        board (list): A list of lists representing the board.

    Examples:
        >>> init_board(2, 3, 0)
        [[0, 0, 0], [0, 0, 0]]
        >>> init_board(1, 4, '?')
        [['?', '?', '?', '?']]
        >>> init_board(3, 1, -1)
        [[-1], [-1], [-1]]
    """

    # Create an empty list
    board = []

    # Append new empty lists to make the rows of the 2D board
    for i in range(nb_rows):
        board.append([])

        # Fill the rows with the value
        for j in range(nb_cols):
            board[i].append(value)

    return board


def count_total(board, value):
    """
    Count how many times a given value appears on the board.

    Parameters:
        board (list): A list of lists representing the board.
        value (any): The value to count on the board.

    Returns:
        count (int): Number of occurrences of the value.

    Examples:
        >>> count_total([[0, 1], [1, 0]], 1)
        2
        >>> count_total([['?', '?'], ['⚑', '?']], '?')
        3
        >>> count_total([[True, False], [True, True]], True)
        3
    """

    # Initialize counter
    count = 0

    # Check all the cells in the board
    for i in range(len(board)):
        for j in range(len(board[i])):

            # Add 1 to the counter if the cell matches the value
            if board[i][j] == value:
                count += 1

    # Return the number of occurrences of the value
    return count


def is_valid_position(board, row, col):
    """
    Check if a (row, col) position is part of the board.

    Parameters:
        board (list): A list of lists representing the board.
        row (int): Row index to check.
        col (int): Column index to check.

    Returns:
        valid (bool): True if position is valid, False otherwise.

    Examples:
        >>> is_valid_position([[0, 0], [0, 0]], 0, 1)
        True
        >>> is_valid_position([[0, 0], [0, 0]], 2, 0)
        False
        >>> is_valid_position([[0], [0], [0]], 1, 0)
        True
    """

    # Check if the coordinates are respecting the board's limits
    return 0 <= row < len(board) and 0 <= col < len(board[0])


def get_neighbour_positions(board, row, col):
    """
    Get all the valid neighbour positions around a cell.

    Neighbours include up to 8 surrounding cells (horizontally,
    vertically, and diagonally).

    Parameters:
        board (list): A list of lists representing the board.
        row (int): Row index of the central cell.
        col (int): Column index of the central cell.

    Returns:
        neighbour_positions (list): List of [row, col] pairs of neighbours.

    Examples:
        >>> get_neighbour_positions([[0, 0, 0],
        ...                          [0, 0, 0],
        ...                          [0, 0, 0]], 1, 1)
        [[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [2, 2]]
        >>> get_neighbour_positions([[0, 0], [0, 0]], 0, 0)
        [[0, 1], [1, 0], [1, 1]]
        >>> get_neighbour_positions([[0, 0], [0, 0]], 1, 1)
        [[0, 0], [0, 1], [1, 0]]
    """
    neighbour_positions = []

    # The neighbours' coordinates can either be the same, be one more, or one
    # less than the ones of the cell.
    for i in range(-1, 2):
        for j in range(-1, 2):

            # If the neighbouring positon is part of the board, and it's not
            # the position of the original cell, add it to the list.
            if (is_valid_position(board, row + i, col + j)
                    and (i != 0 or j != 0)):

                neighbour_positions.append([row + i, col + j])

    # Return the list of positions
    return neighbour_positions


def count_neighbours(board, row, col, value):
    """
    Count how many neighbouring cells contain a given value.

    Parameters:
        board (list): A list of lists representing the board.
        row (int): Row index of the central cell.
        col (int): Column index of the central cell.
        value (any): The value to count in neighbouring cells.

    Returns:
        count (int): Number of neighbouring cells that contain the value.

    Examples:
        >>> b = [[-1, 1, 0],
        ...      [ 1, 2, 1],
        ...      [ 0, 1,-1]]
        >>> count_neighbours(b, 1, 1, -1)
        2
        >>> count_neighbours(b, 0, 1, -1)
        1
        >>> count_neighbours(b, 2, 0, 1)
        2
    """
    neighbours = get_neighbour_positions(board, row, col)

    count = 0

    # Go through every neighbouring cell
    for pos in neighbours:

        # Add 1 if it contains the value
        if board[pos[0]][pos[1]] == value:
            count += 1

    return count


def new_mine_position(board):
    """
    Pick a random position on the board that does not already contain a mine.

    Parameters:
        board (list): Helper board containing mine locations.

    Returns:
        position (tuple): A pair (row, col) for a free cell.

    Examples:
        >>> random.seed(0)
        >>> new_mine_position([[0, -1], [0, 0]])  # position without -1
        (1, 1)
        >>> random.seed(1)
        >>> new_mine_position([[0, 0], [0, -1]])
        (0, 0)
        >>> random.seed(2)
        >>> new_mine_position([[0]])
        (0, 0)
    """

    # Loop until the position isn't already a mine
    while True:
        rand_row = random.randint(0, len(board)-1)
        rand_col = random.randint(0, len(board[0])-1)

        # Stop and return once the new mine position is created
        if board[rand_row][rand_col] != -1:
            return rand_row, rand_col


def new_mine(board):
    """
    Place a new mine on the board and update neighbour counts.

    The mine is placed at a random free position (value not -1).
    All adjacent non-mine cells are increased by 1.

    Parameters:
        board (list): Helper board containing current mine layout and counts.

    Returns:
        None

    Examples:
        >>> random.seed(0)
        >>> b = init_board(2, 2, 0)
        >>> new_mine(b)
        >>> b  # one cell becomes -1, neighbours increased
        [[-1, 1], [1, 1]]
        >>> random.seed(1)
        >>> b = init_board(2, 2, 0)
        >>> new_mine(b)
        >>> b
        [[1, 1], [1, -1]]
        >>> random.seed(2)
        >>> b = init_board(1, 3, 0)
        >>> new_mine(b)
        >>> b
        [[0, -1, 0]]
    """
    # Use the previous function to get the position
    row, col = new_mine_position(board)

    # Create the new mine
    board[row][col] = -1

    # Add 1 to the number of adjacent mines for all neighbours
    adj_pos = get_neighbour_positions(board, row, col)
    for pos in adj_pos:
        if board[pos[0]][pos[1]] != -1:
            board[pos[0]][pos[1]] += 1


def generate_helper_board(nb_rows, nb_cols, nb_mines):
    """
    Generate the helper board containing mines and neighbour counts.

    The helper board stores -1 for mines and integers for the number
    of adjacent mines in each safe cell.

    Parameters:
        nb_rows (int): Number of rows.
        nb_cols (int): Number of columns.
        nb_mines (int): Number of mines to place.

    Returns:
        board (list): The fully initialized helper board.

    Examples:
        >>> random.seed(0)
        >>> h = generate_helper_board(2, 2, 1)
        >>> len(h), len(h[0])
        (2, 2)
        >>> random.seed(1)
        >>> h = generate_helper_board(3, 3, 2)
        >>> count_total(h, -1)
        2
        >>> random.seed(2)
        >>> h = generate_helper_board(1, 4, 1)
        >>> count_total(h, -1)
        1
    """

    # Generate a board filled with 0
    board = init_board(nb_rows, nb_cols, 0)

    # Generate the board with the chosen amount of mines
    for n in range(nb_mines):
        # I wasn't sure if I should've used 'for _ in range(nb_mines):'
        # because i forgot if we saw it in class.

        # Add the mine
        new_mine(board)

        # Update the value of the neighbouring cells
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] != -1:
                    board[i][j] = count_neighbours(board, i, j, -1)

    return board


def flag(board, row, col):
    """
    Switch between '?' and '⚑' on the game board

    If the cell currently contains '?', it becomes a flag (⚑).
    If it currently contains a flag, it becomes '?' again.

    Parameters:
        board (list): Visible game board.
        row (int): Row index of the cell.
        col (int): Column index of the cell.

    Returns:
        None

    Examples:
        >>> g = [['?', '?'], ['?', '?']]
        >>> flag(g, 0, 1)
        >>> g
        [['?', '⚑'], ['?', '?']]
        >>> flag(g, 0, 1)
        >>> g
        [['?', '?'], ['?', '?']]
        >>> flag(g, 1, 0)
        >>> g
        [['?', '?'], ['⚑', '?']]
    """

    # Switch between '?' and '⚑' on the game board
    if board[row][col] == '?':
        board[row][col] = '\u2691'
    elif board[row][col] == '\u2691':
        board[row][col] = '?'


def reveal(helper_board, game_board, row, col):
    """
    Reveal the value of a cell on the visible game board.

    If the chosen cell contains a mine on the helper board, an
    AssertionError is raised. Otherwise the number of adjacent
    mines is revealed on the game board.

    Parameters:
        helper_board (list): Board with mine locations and counts.
        game_board (list): Visible board shown to the player.
        row (int): Row index to reveal.
        col (int): Column index to reveal.

    Returns:
        None

    Examples:
        >>> h = [[0, 1], [-1, 2]]
        >>> g = [['?', '?'], ['?', '?']]
        >>> reveal(h, g, 0, 0)
        >>> g
        [['0', '?'], ['?', '?']]
        >>> reveal(h, g, 0, 1)
        >>> g
        [['0', '1'], ['?', '?']]
        >>> # reveal(h, g, 1, 0)  # would raise AssertionError ("BOOM! You lost.")
    """

    # If that cell is a bomb, the game is lost
    if helper_board[row][col] == -1:
        raise AssertionError("BOOM! You lost.")

    # If not, replace '?' with the value on the helper board
    else:
        game_board[row][col] = str(helper_board[row][col])


def print_board(board):
    """
    Print the board to the console, row by row.

    Parameters:
        board (list): A list of lists representing the board.

    Returns:
        None

    Examples:
        >>> print_board([[0, 1], [2, 3]])
        0 1
        2 3
        >>> print_board([['?', '⚑'], ['1', '2']])
        ? ⚑
        1 2
        >>> print_board([[True], [False]])
        True
        False
    """

    for i in range(len(board)):
        for j in range(len(board[i])):
            # Print the values with a space, without going to next line
            print(board[i][j], end=" ")

        # Go to next line after each row
        print("")


def init_game(difficulty, num_cols, num_rows):
    """
    Initialize the game boards and choose the number of mines.

    Difficulty is one of "EASY", "MEDIUM", or "HARD" and controls
    the fraction of cells that will contain mines.

    Parameters:
        difficulty (str): Chosen difficulty level.
        num_cols (int): Number of columns of the board.
        num_rows (int): Number of rows of the board.

    Returns:
        game_board (list): Visible board filled with '?'.
        helper_board (list): Board with mines and neighbour counts.
        num_mines (int): Total number of mines placed.

    Examples:
        >>> random.seed(0)
        >>> g, h, m = init_game("EASY", 5, 5)
        >>> len(g), len(g[0]), m
        (5, 5, 2)
        >>> random.seed(1)
        >>> g, h, m = init_game("MEDIUM", 4, 4)
        >>> len(h), len(h[0]), m
        (4, 4, 4)
        >>> random.seed(2)
        >>> g, h, m = init_game("HARD", 3, 3)
        >>> count_total(h, -1)
        4
    """

    # Select the right difficulty
    if difficulty == "EASY":
        difficulty = EASY_DIFFICULTY
    elif difficulty == "MEDIUM":
        difficulty = MEDIUM_DIFFICULTY
    elif difficulty == "HARD":
        difficulty = HARD_DIFFICULTY

    # Compute the number of mines required
    num_mines = int(difficulty * num_rows * num_cols)

    # Initialize the two boards
    helper_board = generate_helper_board(num_rows, num_cols, num_mines)
    game_board = init_board(num_rows, num_cols, '?')

    return game_board, helper_board, num_mines


def is_game_over(game_board, helper_board):
    """
    Check if all safe cells have been revealed.

    The game is over when every non-mine cell on the helper board
    has been revealed on the game board.

    Parameters:
        game_board (list): Visible board.
        helper_board (list): Board with mines and counts.

    Returns:
        over (bool): True if the game is won, False otherwise.

    Examples:
        >>> g = [['0', '1'], ['⚑', '?']]
        >>> h = [[0, 1], [-1, 1]]
        >>> is_game_over(g, h)
        False
        >>> g[1][1] = '1'
        >>> is_game_over(g, h)
        True
        >>> is_game_over([['?']], [[-1]])
        True
    """

    # Go through all cells
    for i in range(len(game_board)):
        for j in range(len(game_board[i])):

            # If a cell isn't a mine and still '?', game isn't over
            if helper_board[i][j] != -1 and game_board[i][j] == '?':
                return False

    return True


def play():
    """
    Run the full interactive Minesweeper game.

    The function asks the user for board size and difficulty,
    then repeatedly asks the player to reveal or flag cells
    until the game is won or a mine is revealed.

    Parameters:
        None

    Returns:
        None
    """

    # Ask the user for the game parameters
    num_rows = int(input("Enter number of rows for the board: "))
    num_cols = int(input("Enter number of columns for the board: "))
    difficulty = input("Enter difficulty: ")

    # Initialize the game
    game_board, helper_board, num_mines = (
        init_game(difficulty, num_cols, num_rows))

    # Play as long as the game isn't over
    game_over = False
    while not game_over:
        # Compute the supposed number of mines left based on user's flags
        mines_left = num_mines - count_total(game_board, "\u2691")

        # Print the board and the amount of mines left
        print("Current Board: (" + str(mines_left) + " mines remaining)")
        print_board(game_board)

        # Let the user chose the next move
        chosen_move = int(input("Choose 0 to reveal or 1 to flag: "))
        chosen_row = int(input("Which row? "))
        chosen_col = int(input("Which column? "))

        # Reveal or flag the chosen cell accordingly
        if chosen_move == 0:
            reveal(helper_board, game_board, chosen_row, chosen_col)
        elif chosen_move == 1:
            flag(game_board, chosen_row, chosen_col)

        # Check if the game is over
        game_over = is_game_over(game_board, helper_board)

    # Congratulate when the game is over
    print("Congratulations! You won!")

    # Replace remaining '?' with flags
    for i in range(len(game_board)):
        for j in range(len(game_board[i])):
            if game_board[i][j] == '?':
                game_board[i][j] = '\u2691'

    # Print the final board
    print("Final Board:")
    print_board(game_board)


def apply_click_to_neighbours(board, col, row, click_function):
    """
    Apply the click function to all unrevealed neighbours of a cell.

    I didn't add examples since I figured it was technically a sub function
    to reduce repetitiveness in the code of the solve_cell() function, which
    didn't need examples.

    Parameters:
        board (list): Visible game board.
        col (int): Column index of the central cell.
        row (int): Row index of the central cell.
        click_function (callable): Function taking (row, col) as arguments.

    Returns:
        None
    """

    # Get all neighbouring positions
    neighbour_pos = get_neighbour_positions(board, row, col)

    # Go through all neighbouring positions
    for pos in neighbour_pos:

        # Check if it's a valid one
        if is_valid_position(board, pos[0], pos[1]):

            # Apply the function to unrevealed cells
            if board[pos[0]][pos[1]] == '?':
                click_function(pos[0], pos[1])


def solve_cell(board, row, col, left_click, right_click):
    """
    Try to solve a cell based on its neighbours.

    If the number shown in the cell equals the number of adjacent
    flags, all other unknown neighbours are left-clicked.
    If the number of revealed neighbours minus flags equals the
    number of unknown neighbours, all unknown neighbours are right-clicked.
    Otherwise, it does nothing.

    Parameters:
        board (list): Visible game board.
        row (int): Row index of the cell to solve.
        col (int): Column index of the cell to solve.
        left_click (callable): Function used to reveal a cell.
        right_click (callable): Function used to flag a cell.

    Returns:
        None
    """

    main_cell = board[row][col]

    # Check if the main cell has an integer
    try:
        main_cell = int(main_cell)
    except ValueError:
        return  # Not a digit, so exit the function

    n_neigh = len(get_neighbour_positions(board, row, col))

    # Count the number of neighbouring flags
    adj_flags = count_neighbours(board, row, col, '\u2691')

    # Count the number of revealed neighbour (8 - number of unrevealed)
    adj_revealed = n_neigh - count_neighbours(board, row, col, '?')

    # No more unflagged mines
    if adj_flags == main_cell:
        apply_click_to_neighbours(board, col, row, left_click)

    # All unrevealed neighbours are mines
    if adj_revealed - adj_flags == n_neigh - main_cell:
        apply_click_to_neighbours(board, col, row, right_click)

    # Otherwise, do nothing


def solve(board, left_click, right_click):
    """
    Repeatedly try to solve every cell on the board.

    The function calls solve_cell on every cell while there are still
    unknown cells ('?') on the board.

    Parameters:
        board (list): Visible game board.
        left_click (callable): Function used to reveal a cell.
        right_click (callable): Function used to flag a cell.

    Returns:
        None
    """

    # Loop until all cells are revealed
    while count_total(board, '?') != 0:

        # Try to solve each cell on the board
        for row in range(len(board)):
            for col in range(len(board[row])):
                solve_cell(board, row, col, left_click, right_click)


if __name__ == "__main__":
    random.seed(202)
    play()
