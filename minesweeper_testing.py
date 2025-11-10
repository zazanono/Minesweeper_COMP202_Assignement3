import minesweeper as m

def test_bot(helper_board, game_board):
    
    total_mines = m.count_total(helper_board, -1)
    private_board = [] #cheat prevention
    for row in game_board: #deep copy
        tmp = []
        for value in row:
            tmp.append(value)
        private_board.append(tmp)
        
    def left_click(row, col):
        #tip: consider raising an error here if (row, col) is not a valid cell
        m.reveal(helper_board, private_board, row, col) #for verification
        m.reveal(helper_board, game_board, row, col) #for the bot
        print('Current Board:')
        m.print_board(game_board)
        
    def right_click(row, col):
        #tip: consider raising an error here if (row, col) is not a valid cell
        m.flag(private_board, row, col) #for verification
        m.flag(game_board, row, col) #for the bot
        print('Current Board:')
        m.print_board(game_board)
    
    print('Current Board:')
    m.print_board(game_board)
    m.solve(game_board, left_click, right_click)
    
    if m.count_total(private_board, '?') == 0 and \
       m.count_total(private_board, '⚑') == total_mines:
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

if __name__ == '__main__':
    test_bot(BOT_TEST_1[0], BOT_TEST_1[1])