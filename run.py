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


def print_instructions():
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


def check_guess(board, row, col):
    if board[row][col] == "S":
        board[row][col] = "H"
        return "hit"
    elif board[row][col] == "H" or board[row][col] == "M":
        return "duplicate"
    else:
        board[row][col] = "M"
        return "miss"


def update_board(board, row, col, result):
    if result == "hit":
        board[row][col] = "H"
    elif result == "miss":
        board[row][col] = "M"


def computer_guess(board):
    guess_row = random_row(board)
    guess_col = random_col(board)
    return guess_row, guess_col


def print_scoreboard():
    print("\nTop 10 Players:")
    print("-" * 25)
    try:
        with open("scores.txt", "r") as score_file:
            scores = [line.strip().split(",")
                      for line in score_file.readlines()]
            sorted_scores = sorted(
                scores, key=lambda x: int(x[2]), reverse=True)[:10]
            for idx, (name, age, score) in enumerate(sorted_scores):
                print(f"{idx + 1}. {name} ({age}) - {score} points")
    except FileNotFoundError:
        print("No scores recorded yet.")


def main():
    os.system("cls" if os.name == "nt" else "clear")
    print_ascii_art()
    print_instructions()

    print_scoreboard()

    print()
    name = input("What's your name? ")
    age = int(input("What's your age? "))
    if age < 15:
        print("Sorry, you must be at least 15 years old to play.")
        return

    while True:
        play = input("Do you want to play? (y/n) ").lower()
        if play == "y":
            break
        elif play == "n":
            sure = input("Are you sure? (y/n) ").lower()
            if sure = "y":
                return

    