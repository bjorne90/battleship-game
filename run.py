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
    """
    Return a random row number within the bounds of the given board.
    """
    return random.randint(0, len(board) - 1)


def random_col(board):
    """
    Return a random column number within the bounds of the given board.
    """
    return random.randint(0, len(board[0]) - 1)


def print_board(board):
    """
    Print the given board in a human-readable format.
    """
    print("  " + " ".join(str(i) for i in range(len(board[0]))))
    for i, row in enumerate(board):
        print(str(i) + " " + " ".join(row))


def print_boards(player_board, computer_board, name):
    """
    Print the player and computer boards side by side.
    """
    hidden_computer_board = [
            ['0' if cell == 'S' else cell for cell in row]
            for row in computer_board]

    print(f"{name}'s Board:")
    print("  " + " ".join(str(i) for i in range(len(player_board[0]))))
    for i, row in enumerate(player_board):
        print(str(i) + " " + " ".join(row))

    print("\nComputer's Board:")
    print("  " + " ".join(str(i)
          for i in range(len(hidden_computer_board[0]))))
    for i, row in enumerate(hidden_computer_board):
        print(str(i) + " " + " ".join(row))


def check_ship_placement_valid(board, row, col, size, orientation):
    """
    Check if a ship can be placed at the given position on the board.
    """
    if orientation == "horizontal":
        if col + size > len(board[0]):
            return False
        for i in range(size):
            if board[row][col + i] != "0":
                return False
    else:
        if row + size > len(board):
            return False
        for i in range(size):
            if board[row + i][col] != "0":
                return False
    return True


def place_ship(board, row, col, size, orientation):
    """
    Place a ship of given size and orientation on the board at the specified
    position.
    """
    if orientation == "horizontal":
        for i in range(size):
            board[row][col + i] = "S"
    else:  # vertical
        for i in range(size):
            board[row + i][col] = "S"


def place_random_fleet(board, fleet):
    """
    Place the given fleet randomly on the board.
    """
    for ship in fleet:
        size, _ = ship
        while True:
            row, col = random_row(board), random_col(board)
            orientation = random.choice(["horizontal", "vertical"])
            if check_ship_placement_valid(board, row, col, size, orientation):
                place_ship(board, row, col, size, orientation)
                break


def user_guess(board):
    """
    Prompt the user for a row and column guess within the board's dimensions.
    """
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
    """
    Check the result of a guess on the given board at the specified row and
    column.
    """
    if board[row][col] == "S":
        board[row][col] = "H"
        return "hit"
    elif board[row][col] == "H" or board[row][col] == "M":
        return "duplicate"
    else:
        board[row][col] = "M"
        return "miss"


def update_board(board, row, col, result):
    """
    Update the board based on the result of a guess at the specified row and
    column.
    """
    if result == "hit":
        board[row][col] = "H"
    elif result == "miss":
        board[row][col] = "M"


def computer_guess(board):
    """
    Generate a random row and column guess within the board's dimensions.
    """
    guess_row = random_row(board)
    guess_col = random_col(board)
    return guess_row, guess_col


def print_scoreboard():
    """
    Print the top 10 player scores from the scores.txt file.
    """
    print("\nTop 10 Players:")
    print("-" * 25)
    try:
        with open("scores.txt", "r") as score_file:
            scores = []
            for line in score_file.readlines():
                try:
                    name, age, score = line.strip().split(",")
                    scores.append((name, age, score))
                except ValueError:
                    print("Invalid score format:", line.strip())
                    continue
            sorted_scores = sorted(
                scores, key=lambda x: int(x[2]), reverse=True)[:10]
            for idx, (name, age, score) in enumerate(sorted_scores):
                print(f"{idx + 1}. {name} ({age}) - {score} points")
    except FileNotFoundError:
        print("No scores recorded yet.")


def main():
    """
    The main function to run the Battleship game.
    """
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
            if sure == "y":
                return

    difficulty = input(
        "Choose difficulty level (e)asy, (m)edium, or (h)ard: ").lower()
    if difficulty == "e":
        grid_size = 5
        fleet = [(2, "destroyer"), (3, "cruiser"), (4, "battleship")]
        turns = 10
    elif difficulty == "m":
        grid_size = 7
        fleet = [
            (2, "destroyer"),
            (3, "cruiser"),
            (4, "battleship"),
            (5, "aircraft_carrier"),
        ]
        turns = 15
    else:  # Hard
        grid_size = 10
        fleet = [
            (2, "destroyer"),
            (3, "cruiser"),
            (4, "battleship"),
            (5, "aircraft_carrier"),
            (6, "aircraft_carrier"),
        ]
        turns = 20

    ship_points = {
        "destroyer": 4,
        "cruiser": 6,
        "battleship": 8,
        "aircraft_carrier": 10,
    }

    player_board = [["0"] * grid_size for _ in range(grid_size)]
    computer_board = [["0"] * grid_size for _ in range(grid_size)]
    place_random_fleet(computer_board, fleet)

    hits = {ship_name: 0 for _, ship_name in fleet}
    total_ship_sizes = sum(size for size, _ in fleet)
    score = 0
    computer_score = 0

    while turns > 0:
        print(f"Turns remaining: {turns}")
        print_boards(player_board, computer_board, name)
        print(f"Your socre: {score}")
        print(f"Computer's Score: {computer_score}")

        guess_row, guess_col = user_guess(player_board)
        result = check_guess(computer_board, guess_row, guess_col)
        update_board(player_board, guess_row, guess_col, result)

        if result == "hit":
            print("You hit a ship")
            ship_name = None
            for ship_size, ship_name in fleet:
                if computer_board[guess_row][guess_col] == ship_name[0]:
                    ship_name = ship_name
                    break
            hits[ship_name] += 1
            score += ship_points[ship_name] // ship_size

            if sum(hits.values()) == total_ship_sizes:
                print("Congratulations! You sank all the ships!")
                break
        elif result == "miss":
            print("You missed.")
        else:
            print("You already guessed that location.")

        guess_row, guess_col = computer_guess(player_board)
        result = check_guess(player_board, guess_row, guess_col)
        update_board(player_board, guess_row, guess_col, result)

        if result == "hit":
            print("The Computer hit your ship!")
            ship_name = None
            for ship_size, ship_name in fleet:
                if player_board[guess_row][guess_col] == ship_name[0]:
                    ship_name = ship_name
                    break
            computer_score += ship_points[ship_name] // ship_size
        elif result == "miss":
            print("The computer missed.")
        else:
            print("The computer already guessed that location.")

        if sum(hits.values()) == total_ship_sizes:
            print("Game Over! The computer sank all your ships!")
            break

        turns -= 1

    if turns == 0:
        print("Game Over! You ran out of turns!")

    print_boards(player_board, computer_board, name)
    print(f"Your final score: {score}")
    print(f"Computer's final score: {computer_score}")

    with open("scores.txt", "a", encoding="utf-8") as score_file:
        score_file.write(f"{name},{age},{score}\n")

    print_scoreboard()


if __name__ == "__main__":
    main()
