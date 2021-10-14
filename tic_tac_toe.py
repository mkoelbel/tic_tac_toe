import itertools     # to switch players


def get_y_n(question):
    """ Prompt players for a 'Y' or a 'N', until you get an appropriate response. """
    y_n_option = ""
    chances = 0
    while not (y_n_option.casefold() == "y" or y_n_option.casefold() == "n"):
        if chances > 0:
            print("\nPlease enter 'Y' or 'N'.")
        y_n_option = input(f"{question}? (Y/N)\n")
        chances += 1
    if y_n_option.casefold() == "y":
        return True
    else:
        return False
        

def is_integer(entry):
    """ Check that the entry is an integer. """
    try:
        int(entry)
        return True
    except ValueError:
        return False


def is_positive(entry):
    """ Check that the entry is a positive number. """
    return entry > 0


def is_in_range(entry):
    """ Check that the entry is within the range of the game board. """
    return entry in range(game_size)


def is_valid_game_size(entry):
    """ Check that the player entered a valid game board size. """
    if not is_integer(entry):
        print("\nPlease enter a number.")
        return False
    elif not is_positive(int(entry)):
        print("\nPlease enter a number greater than 0. ")
        return False
    else:
        return True


def is_valid_row_col(entry):
    """ Check that the player entered a valid row or column. """
    if not is_integer(entry):
        print_game_board(game)
        print(f"\nPlease enter a number.")
        return False
    elif not is_in_range(int(entry)):
        print_game_board(game)
        print(f"\nPlease play a position between 0 and {game_size-1}.")
        return False
    else: 
        return True


def check_continue(entry):
    """ Determine whether players want to continue playing the current game. """
    # if player enters 'x' as their move, they don't want to continue
    if entry.casefold() == 'x':
        print("You don't want to finish this game. Don't blame you!")
        return False
    else:
        return True


def print_game_board(game_map):
    """ Print out the game board without making a move. """
    print("   "+"  ".join(str(i) for i in range(len(game_map))))
    for count, row in enumerate(game_map):
        translation = {39: None}    # remove the '' in the print out
        print(count, str(row).translate(translation))


def check_valid_move(game_map, player='', row=0, column=0):
    """ Check whether the move is in an open space. """
    try:
        # check to see if the position is open
        if game_map[row][column] != '_':
            # if the position isn't open, re-print the game board anyway, so the player can see that it's not open
            print_game_board(game_map)
            print(f"\nPlayer {player}, please play in an open position.")
            return False
        else: 
            return True
    
    # if it doesn't work, print some error messages
    # except IndexError:
    #     print(f"\nPlayer {player}, please play a position between 0 and "
    #           f"{len(game_map[0])-1}.")
    #     return False
    except Exception as e:
        print(str(e))
        return False


def make_move(game_map, player='', row=0, column=0):
    """ Make the move on the game board. """
    # modify game board with new move
    game_map[row][column] = player
    # print out the new game board
    print_game_board(game_map)
    return game_map
    

def check_for_streak(iterable):
    """ Check if a list has a streak. """
    if iterable.count(iterable[0]) == len(iterable) and iterable[0] != '_':
        return True
    else:
        return False


def check_game_over(current_game):
    """ Check if there's a winner. """
    # check if there's a "row" winner
    for row in current_game:
        if check_for_streak(row):
            print(f"Player {row[0]} is the winner! They won a row.")
            return True

    # check if there's a "col" winner
    for col in range(len(current_game[0])):
        check_col = [] 
        for row in current_game:
            check_col.append(row[col])
        if check_for_streak(check_col):
            print(f"Player {check_col[0]} is the winner! They won a column.")
            return True

    # check if there's a "back diagonal" winner
    b_diag = []
    for index in range(len(current_game)):
        b_diag.append(current_game[index][index])
    if check_for_streak(b_diag):
        print(f"Player {b_diag[0]} is the winner! "
              f"They won a back diagonal.")
        return True

    # check if there's a "front diagonal" winner    
    f_diag = []
    for index in range(len(current_game)):
        f_diag.append(current_game[index][len(current_game) - 1 - index])
    if check_for_streak(f_diag):
        print(f"Player {f_diag[0]} is the winner!"
              f"They won a front diagonal.")
        return True

    # check if there are still available positions
    # if there are, game is not over
    for row in current_game:
        for i in row:
            if i == '_':
                return False

    # if we've gotten to this point, then no one has won
    # but there are no more available moves, so game is over
    print("\nThere are no more available moves -- GAME OVER")
    return True


############################################################################
play = True
while play:

    valid_game_size = False
    # ask players what size board they want to play on, and make sure they enter something valid (positive integer)
    while not valid_game_size:
        game_size = input("What size board to you want to play on?\n"
                          "Ex: 3\n")
        valid_game_size = is_valid_game_size(game_size)  
    game_size = int(game_size)

    # set up game board
    game = [['_' for i in range(game_size)] for i in range(game_size)]
    # print out game board
    print_game_board(game)

    take_back_allow = False
    # ask players if they want to allow taking back moves
    take_back_allow = get_y_n("Taksies backsies")
    if take_back_allow:
        print("You've elected to play with taksies backsies!")

    # create the sequence of turn switches
    player_turns = itertools.cycle(["X", "O"])

    continue_playing = True
    game_over = False
    while continue_playing and not game_over:
        # switch players (or pick a first player)
        current_player = next(player_turns)

        valid_move = False
        while continue_playing and not valid_move:
            # players can end a game early by entering 'x'
            # instead of a number
            print(f"\nPlayer: {current_player}")

            # get the row and column choices from the player.
            # if they enter something invalid, catch that right away
            valid_row = False
            while continue_playing and not valid_row:
                row_choice = (input("Which row?  (Enter 'x' to stop playing.)\n"))
                continue_playing = check_continue(row_choice)
                if not continue_playing:
                    continue
                valid_row = is_valid_row_col(row_choice)
            row_choice = int(row_choice)
            
            valid_col = False
            while continue_playing and not valid_col:
                col_choice = (input("Which col?  (Enter 'x' to stop playing.)\n"))
                continue_playing = check_continue(col_choice)
                if not continue_playing:
                    continue
                valid_col = is_valid_row_col(col_choice)
            col_choice = int(col_choice)

            # check if it's a valid move by trying to make the move,
            # but don't yet modify the game board
            if continue_playing:
                valid_move = check_valid_move(game, current_player, row_choice, col_choice)

        # make their move! (and save the old game board, and output the new version of the game board)
        if continue_playing:
            old_game_board = game
            game = make_move(game, current_player, row_choice, col_choice)
            # check if the game is over
            game_over = check_game_over(game)

    # final last thing: ask players if they want to play another game.
    # if they don't want to start a new game, set play = False
    play = get_y_n("Play again")
    if not play:
        print("Goodbye, hope you had fun, see you next time! :D")
