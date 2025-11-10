def test_bot(helper_board, game_board):
    
    total_mines = count_total(helper_board, -1)
    private_board = [] #cheat prevention
    for row in game_board: #deep copy
        tmp = []
        for value in row:
            tmp.append(value)
        private_board.append(tmp)
        
    def left_click(row, col):
        #tip: consider raising an error here if (row, col) is not a valid cell
        reveal(helper_board, private_board, row, col) #for verification
        reveal(helper_board, game_board, row, col) #for the bot
        print('Current Board:')
        print_board(game_board)
        
    def right_click(row, col):
        #tip: consider raising an error here if (row, col) is not a valid cell
        flag(private_board, row, col) #for verification
        flag(game_board, row, col) #for the bot
        print('Current Board:')
        print_board(game_board)
    
    print('Current Board:')
    print_board(game_board)
    solve(game_board, left_click, right_click)
    
    if count_total(private_board, '?') == 0 and \
       count_total(private_board, '⚑') == total_mines:
        #IMPORTANT: in play(), we do not need all mines to be flagged to win,
        #but we do when testing the bot,
        #so you will need to modify this condition for play()
        print('Congratulations! You won!')
    else:
        print('Bad Bot :(')
        
BOT_TEST_1 = [[[1, -1, 1, 1, 1],
               [1, 1, 1, 2, -1],
               [1, 2, 3, 5, -1],
               [1, -1, -1, -1, -1],
               [1, 2, 3, 3, 2]],
              [['1', '?', '?', '?', '?'],
               ['1', '1', '?', '?', '?'],
               ['?', '?', '?', '?', '?'],
               ['?', '?', '?', '?', '?'],
               ['?', '?', '?', '?', '?']]]

#test_bot(BOT_TEST_1[0], BOT_TEST_1[1])