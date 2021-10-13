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


def check_game_size_integer(entry):
    """ Make sure player entered a number for their game board size. """
    try:
        int(entry)
        return True
    except ValueError:
        print("\nPlease enter a number.")
        return False


def check_game_size_positive(entry):
    """ Make sure player entered a positive number for their game board size. """
    if entry > 0:
        return True
    else:
        print("\nPlease enter a number greater than 0. ")
        return False


def check_integer(entry):
    """ Make sure player entered a number for their move. """
    try:
        int(entry)
        return True
    except ValueError:
        print_game_board(game)
        print(f"\nPlayer {current_player}, please enter a number.")
        return False


def check_in_range(entry):
    """ Make sure player entered a move that is within the game board. """
    if entry in range(game_size):
        return True
    else:
        print_game_board(game)
        print(f"\nPlayer {current_player}, please play a position between 0 "
              f"and {game_size-1}.")
        return False


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


def game_board(game_map, player='_', row=0, column=0, make_move=True):
    """ Make sure a move is valid, then make the move on the game board. """
    try:
        # check to see if the position is open
        if game_map[row][column] != '_':
            # if the position isn't open, re-print the game board anyway, so the player can see that it's not open
            print_game_board(game_map)
            print(f"\nPlayer {player}, please play in an open position.")
            return False
        # only modify and print out the board if we're explicitly told to
        if make_move:
            # modify game board with new move
            game_map[row][column] = player
            # print out the new game board
            print_game_board(game_map)
            return game_map

    # if it doesn't work, print some error messages
    # except IndexError:
    #     print(f"\nPlayer {player}, please play a position between 0 and "
    #           f"{len(game_map[0])-1}.")
    #     return False
    except Exception as e:
        print(str(e))
        return False

    # if we've gotten to this point, then make_move is False
    # (meaning we don't want to modify the board),
    # but it IS a valid move, so return True
    return True
    

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
                print("Keep playing!")
                return False

    # if we've gotten to this point, then no one has won
    # but there are no more available moves, so game is over
    print("\nThere are no more available moves -- GAME OVER")
    return True


############################################################################
play = True
while play:

    # set up original (standard) 3x3 game board
    # game = [['_', '_', '_'],
    #         ['_', '_', '_'],
    #         ['_', '_', '_']]

    game_size_integer = False
    game_size_positive = False
    # ask players what size board they want to play on, and make sure they enter something valid (positive integer)
    while not (game_size_integer and game_size_positive):
        game_size = input("What size board to you want to play on?\n"
                          "Ex: 3\n")
        game_size_integer = check_game_size_integer(game_size)
        if game_size_integer:
            # if game size is number, re-declare it as an integer, to be compatible with later functions
            game_size = int(game_size)
            game_size_positive = check_game_size_positive(game_size)

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
            print(f"\n(At anytime, to discontinue this game, enter 'x'.)"
                  f"\nPlayer: {current_player}")

            row_integer = False
            column_integer = False
            row_in_range = False
            column_in_range = False
            # get the row and column choices from the player.
            # if they enter something invalid, catch that right away
            while continue_playing and not (row_integer and row_in_range):
                row_choice = (input("Which row?\n"))
                continue_playing = check_continue(row_choice)
                if continue_playing:
                    row_integer = check_integer(row_choice)
                    if row_integer:
                        row_choice = int(row_choice)
                        row_in_range = check_in_range(row_choice)

            while continue_playing and (not column_integer or not column_in_range):
                column_choice = (input("Which column?\n"))
                continue_playing = check_continue(column_choice)
                if continue_playing:
                    column_integer = check_integer(column_choice)
                    if column_integer:
                        column_choice = int(column_choice)
                        column_in_range = check_in_range(column_choice)

            # check if it's a valid move by trying to make the move,
            # but don't yet modify the game board
            if continue_playing:
                valid_move = game_board(game, current_player, row_choice, column_choice, make_move=False)

        # make their move! (and save the old game board, and output the new version of the game board)
        if continue_playing:
            old_game_board = game
            game = game_board(game, current_player, row_choice, column_choice)
            # check if the game is over
            game_over = check_game_over(game)

    # final last thing: ask players if they want to play another game.
    # if they don't want to start a new game, set play = False
    play = get_y_n("Play again")
    if not play:
        print("Goodbye, hope you had fun, see you next time! :D")
