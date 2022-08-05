import random
import math

def show_board(board): # show passed board to the user
    print(f' {board[7]}' + f'  |{board[8]}'  + f'  | {board[9]}')
    print(' ---|---|----')
    print(f' {board[4]}' + f'  |{board[5]}' + f'  | {board[6]}')
    print(' ---|---|----')
    print(f' {board[1]}' + f'  |{board[2]}' + f'  | {board[3]}')  

def pick_letter(): # lets the player choose a letter
    letter = input('Pick a letter (X, O): ')

    if letter.upper() == 'X':
        return ['X', 'O']
    elif letter.upper() == 'O':
        return ['O', 'X']
    else:
        letter = input('Pick a letter: ')

def first(): # turn of the game is chosen at random
    turn = random.randrange(0, 2)

    if turn == 1:
        return 'player'
    else:
        return 'computer'

def play_again(): # asks whether the player wants tom play again
    print('Type y/n to choose whether you want to play again: ')
    choice = input()
    if choice == 'n':
        return False
    return True

def duplicate_array(board): # duplicates the board for the computer to test its moves before making them
    duplicate_array = []
    for i in board:
        duplicate_array.append(i)

    return duplicate_array

def make_move(board, letter, num): # makes move for the player
    board[num] = letter

def is_winner(bo, le): # checks winner for all options
    if(bo[7] == le and bo[8] == le and bo[9] == le) or (bo[4] == le and bo[5] == le and bo[6] == le) or (bo[1] == le and bo[2] == le and bo[3] == le) or (bo[1] == le and bo[4] == le and bo[7] == le) or (bo[2] == le and bo[5] == le and bo[8] == le) or (bo[3] == le and bo[6] == le and bo[9] == le) or (bo[1] == le and bo[5] == le and bo[9] == le) or(bo[3] == le and bo[5] == le and bo[7] == le):
        return True

def is_free(board, move): # is the space empty?
    if board[move] == ' ':
        return True
    return False

def get_player_move(board): # gets player move
    move = ''

    while move not in '1 2 3 4 5 6 7 8 9'.split() or is_free(board, int(move)) == False:
        move = input('Type a number form 1-9 to choose a move:')
    else:
        return int(move)

def return_random_moves_from_list(board, moves_list): 
    possible_moves = [] 
    for i in moves_list:
        if is_free(board, i):
            possible_moves.append(i)
    try:
        return random.choice(possible_moves)
    except:
        return None

def evaluate(board, letter):
    if letter == 'X':
        opp = 'O'
    else:
        opp = 'X'
    if is_winner(board, letter): # if this player has won and they're the maximiser, then return 10
        return 10
    elif is_winner(board, opp): # if this player has won and they're the minimiser(always the oppositon), then return -10
        return -10 
    else:
        return 0   # its a tie

def minimax(board, depth, ismaxim, letter):
    if letter == 'X': # if the letter passed in is X
        opp = 'O' # opposing player gets O
    else:
        opp = 'X' # and vise versa
    score = evaluate(board, letter) #evaluate the board state

    if score == 10: # if it returns a 10
        return score - depth # return that 10-depth(this is only for it to choose moves that make it win faster than others)
    
    if score == -10:
        return score + depth # same but reverse for oppositionm player

    if board_is_full(board):
        return 0 # if no moves left, no one has won, return 0

    if ismaxim: # if maximiser's turn
        best = -math.inf # start off score is -infinity,which they'll try to maximise

        for move in range(1, 10): # for every move in the board
            if is_free(board, move): # if its free
                make_move(board, letter, move) # make that move
                best = max(best, minimax(board, depth+1, False, letter)) # best score is the maximum between the initial best score and recursive call on minimax, which returns a score after re-evaliuating the board. it asks the minimising player what score it would get if it plays this specific move, and on the next call, the minimiser asks the maximiser the same, this way, we move down the game tree through possible states, until a terminal state, which is when someone has won or a tie, so the minimax returns a score then
                board[move] = ' ' # undo that move
        return best # return best possible score
    else: # same concept as maximiser, but reverse(minimiser turn)
        best = math.inf

        for move in range(1, 10):
            if is_free(board, move):
                make_move(board, opp, move)
                best = min(best, minimax(board, depth+1, True, letter))
                board[move] = ' '
        return best

def ai_make_move(board, letter): # we then use minimax to help the computer make moves on the board
    best =  -math.inf #-math.inf # its the maximising player, so its starts off with a score of -infinity
    best_move = None # no best move.....yet ;)

    for move in range(1, 10):
        if is_free(board, move):
            make_move(board, letter, move)
            move_value = minimax(board, 0, False, letter) # start at depth 0, where they aren't the maximising player
            if move_value > best: # if the value of this move is less than the best move, its the new best score
              best_move = move # therefore we have a new best move
              best = move_value
               
            board[move] = ' ' # undo the move
            print(best_move,best)

    return best_move # return best possible move

def computer_choose_moves(computer_letter, board): #nolonger in use
    if computer_letter == 'X':
        player_letter = 'O'
    else:
        player_letter = 'X'
    
    #computer "AI"

    # return a move that blocks the oppostion player from winning
    copy = duplicate_array(board)
    for i in range(1, 10):
        if is_free(copy, i):
            make_move(copy, player_letter, i)
            if is_winner(copy, player_letter):
                return i

    # take corners if free
    corner_move = return_random_moves_from_list(board, [1,7,3,9])
    if corner_move != None:
        return corner_move

    #take centre if free
    centre_move = return_random_moves_from_list(board, [5])
    if centre_move != None:
        return centre_move

    #move to sides
    return_random_moves_from_list(board, [2,4,6,8])

    # return move if it helps computer win in next move
    copy = duplicate_array(board)
    for i in range(1, 10):
        if is_free(copy, i):
            make_move(copy, computer_letter, i)
            if is_winner(copy, computer_letter):
                print(i,"is the winning move")
                return i
            else:
                copy[i] = ' '

def board_is_full(board): #help us determine whether the game is a tie
    for i in range(1, 10):
        if is_free(board, i):
            return False
    return True

print('T I C T A C T O W') 

def main():
    while True:
        the_board = [' ']*10
        p_letter, c_letter = pick_letter()
        turn = first()
        game_over = False

        print(f'It\'s the {turn}\'s turn!')

        while game_over != True:
            if turn == 'player':
                show_board(the_board)
                move = get_player_move(the_board)
                make_move(the_board,p_letter, move)

                if is_winner(the_board, p_letter):
                    show_board(the_board)
                    print('Player wins')
                    game_over = True
                else:
                    if board_is_full(the_board):
                        show_board(the_board)
                        print('Its a tie!')
                        break
                    else:
                        turn = 'computer'

            else:
                move = ai_make_move(the_board, c_letter)
                make_move(the_board, c_letter, move)

                if is_winner(the_board, c_letter):
                    show_board(the_board)
                    print('Minimax wins')
                    game_over = True
                else:
                    if board_is_full(the_board):
                        show_board(the_board)
                        print('Its a tie!')
                        break
                    else:
                        turn = 'player'

        if not play_again():
            break
main()



    



