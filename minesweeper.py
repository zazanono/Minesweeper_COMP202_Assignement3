def init_board(nb_rows, nb_cols, value):
    matrix = []

    for i in range(nb_rows):
        matrix.append([])
        for j in range(nb_cols):
            matrix[i].append(value)

    return matrix

    # for i in range(nb_rows):
    #     print()
    #     for j in range(nb_cols):
    #         print(matrix[i][j], end=" ")



if __name__ == "__main__":
    init_board(10, 10, 0)