"""
This modul contains a simple implementation of a Battleship game.
The game allows the user to play against the computer in various difficulty
levels.
Both the player and the computer take turns guessing ship location on each
other's boards.
"""


import random
import os


def print_ascii_art():
    """
    Print the ASCII art representing the game's title (Battleship).
    """
    print(
        """
      #####    ##   ##### ##### #      ######  ####  #    # # #####  
      #    #  #  #    #     #   #      #      #      #    # # #    # 
      #####  #    #   #     #   #      #####   ####  ###### # #    # 
      #    # ######   #     #   #      #           # #    # # #####  
      #    # #    #   #     #   #      #      #    # #    # # #      
      #####  #    #   #     #   ###### ######  ####  #    # # #
    """
    )


def print_instruction():
    """
    Print the game instructions for the Battleship game.
    """
    print(
        """
-- Welcome to my Battleship game!
- In this game, you'll try to sink a fleet of ships hidden on a grid by
guessing their positions.
- You'll have a limited number of turns to guess their locations, and the game
will show you.
- whether your guess was a hit, miss, or a duplicate guess.
- To make a guess, enter the row and column of the cell you want to target.
- Good luck!
    """
    )



def random_row(board):
    return random.randint(0, len(board) - 1)


def random_col(board):
    return random.randint(0, len(board[0]) - 1)


def print_board(board):
    print(" " + " ".join.(str(i) for i in range(len(board[0]))))
    for i, row in enumerate(board):
        print(str(i) + " " + " ".join(row))


def print_boards(player_board, computer_board, name):
    hidden_computer_board = [
        ['0' if cell == 'S' else cell for cell in row] for row in computer_board]

    print(f"{name}'s Board:")
    print(" " + " ".join(str(i) for i in range(len(player_board[0]))))
    for i, row in enumerate(player_board):
        print(str(i) + " " + " ".join(row))

    print("\nComputer's Board:")
    print(" " + " ".join(str(i)
          for i in range(len(hidden_computer_board[0]))))
    for i, row in enumerate(hidden_computer_board):
        print(str(i) + " " + " ".join(row))


def check_ship_placement_valid(board, row, col, size, orientation):
    if orientation == "horizontal":
        if col + size > len(board[0]):
            return False
        for i in range(size):
            if board[row][col + i] != "0":
                return False
    else: #vertical
        if row + size > len(board):
            return False
        for i in range(size):
            if board[row + i][col] != "0":
                return False
    return True


def place_ship(board, row, col, size, orientation):
    if orientation == "horizontal":
        for i in range(size):
            board[row][col + i] = "S"
    else: #vertical
        for i in range(size):
            board[row + i][col] = "S"


def place_random_fleet(board, fleet):
    for ship in fleet:
        size, _ = ship
        while True:
            row, col = random_row(board), random_col(board)
            orientation = random.choice(["horizontal", "vertical"])
            if check_ship_placement_valid(board, row, col, size, orientation):
                place_ship(board, row, col, size, orientation)
                break


def user_guess(board):
    while True:
        try:
            guess_row = int(input("Guess Row: "))
            guess_col = int(input("Guess Col: "))
            if 0 <= guess_row < len(board) and 0 <= guess_col < len(board[0]):
                return guess_row, guess_col
            else:
                print("Oops, that's not even in the ocean.")
        except ValueError:
            print("Please enter a valid number.")