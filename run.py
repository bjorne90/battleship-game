"""
This modul contains a simple implementation of a Battleship game.
The game allows the user to play against the computer in various difficulty
levels.
Both the player and the computer take turns guessing ship location on each
other's boards.
"""


import random
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Replace this with your Spreadsheet ID
SPREADSHEET_ID = "15KLsoXYCguRlQVbJ9AJMAcFooVNqE8uRy70E2Brq8oY"


def get_creds():
    """
    Returns Google Sheets credentials to authorize API requests.
    """
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = service_account.Credentials.from_service_account_file(
        "creds.json"
    ).with_scopes(scopes)
    return creds


def read_scores_from_sheet():
    """
    Reads the game scores from a Google Sheet.
    """
    creds = get_creds()
    service = build("sheets", "v4", credentials=creds)
    # Check if the service object is properly initialized
    if not hasattr(service, 'spreadsheets'):
        raise ValueError("Service object does not have a member named "
                         "'spreadsheets'.")

    range_name = "Sheet1!A2:C"
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=SPREADSHEET_ID, range=range_name)
        .execute()
    )

    return result.get("values", [])


def write_score_to_sheet(name, age, score):
    """
    Writes the player's name, age, and score to a Google Sheets file.

    Args:
        name (str): The player's name.
        age (int): The player's age.
        score (int): The player's score.
    """
    creds = get_creds()
    service = build("sheets", "v4", credentials=creds)

    range_name = "Sheet1!A2:C"
    values = [[name, age, score]]
    body = {"values": values}

    service.spreadsheets().values().append(
        spreadsheetId="15KLsoXYCguRlQVbJ9AJMAcFooVNqE8uRy70E2Brq8oY",
        range=range_name,
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()


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
        print(str(i) + " " + " ".join(
            cell if cell in ('0', 'H', 'M') else '0'
            for cell in row))

    print("\nComputer's Board:")
    print("  " + " ".join(str(i)
          for i in range(len(hidden_computer_board[0]))))
    for i, row in enumerate(hidden_computer_board):
        print(str(i) + " " + " ".join(
            cell if cell in ('0', 'H') else '0'
            for cell in row))


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


def place_ship(board, row, col, size, orientation, ship_name):
    """
    Place a ship of given size and orientation on the board at the specified
    position.
    """
    if orientation == "horizontal":
        for i in range(size):
            board[row][col + i] = ship_name[0]
    else:  # vertical
        for i in range(size):
            board[row + i][col] = ship_name[0]


def place_random_fleet(board, fleet):
    """
    Place the given fleet randomly on the board.
    """
    for ship in fleet:
        size, name = ship
        while True:
            row, col = random_row(board), random_col(board)
            orientation = random.choice(["horizontal", "vertical"])
            if check_ship_placement_valid(board, row, col, size, orientation):
                place_ship(board, row, col, size, orientation, name)
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
    ship_name = None
    if board[row][col] != "0" and board[row][col] not in ("H", "M"):
        ship_name = board[row][col]
        board[row][col] = "H"
        return "hit", ship_name
    elif board[row][col] == "H" or board[row][col] == "M":
        return "duplicate", ship_name
    else:
        board[row][col] = "M"
        return "miss", ship_name


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
    result, _ = check_guess(board, guess_row, guess_col)
    return guess_row, guess_col, result


def print_scoreboard():
    """
    Print the top 10 player scores from the Google Spreadsheet.
    """
    print("\nTop 10 Players:")
    print("-" * 25)
    scores = read_scores_from_sheet()
    sorted_scores = sorted(scores, key=lambda x: int(x[2]), reverse=True)[:10]
    for idx, (name, age, score) in enumerate(sorted_scores):
        print(f"{idx + 1}. {name} ({age}) - {score} points")


def main():
    """
    The main function to run the Battleship game.
    """
    os.system("cls" if os.name == "nt" else "clear")
    print_ascii_art()
    print_instructions()

    print_scoreboard()

    print()
    while True:
        name = input("What's your name? ").strip()
        if name and all(c.isalpha() or c.isspace() for c in name):
            break
        else:
            print("Please enter a valid name (letters and spaces only).")

    while True:
        try:
            age = int(input("What's your age? "))
            if 1 <= age <= 105:
                break
            else:
                print("Please enter a valid age (non-negative integer).")
        except ValueError:
            print("Please enter a valid age (non-negative integer).")

    while True:
        play = input("Do you want to play? (y/n) ").lower()
        if play == "y":
            break
        elif play == "n":
            sure = input("Are you sure? (y/n) ").lower()
            if sure == "y":
                return

    while True:
        difficulty = input("Choose difficulty level (e)asy, (m)edium, "
                           "or (h)ard: ").lower()
        if difficulty in ("e", "m", "h"):
            break
        else:
            print("Please enter a valid difficulty level (e, m, or h).")

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

        result, ship_name = check_guess(computer_board, guess_row, guess_col)
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
                write_score_to_sheet(name, age, score)
                print_scoreboard()
                again = input("Do you want to play again? (y/n) ").lower()
                if again == "y":
                    main()
                else:
                    return
        elif result == "miss":
            print("You missed.")
        else:
            print("You already guessed that location.")

        if ship_name is not None:
            hits[ship_name] += 1

        guess_row, guess_col, result = computer_guess(player_board)
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
            return

        turns -= 1

        if turns == 0:
            print("Game Over! You ran out of turns!")

    print_boards(player_board, computer_board, name)
    print(f"Your final score: {score}")
    print(f"Computer's final score: {computer_score}")

    write_score_to_sheet(name, age, score)

    print_scoreboard()

    # Ask the player if they want to play again
    while True:
        again = input("Do you want to play again? (y/n) ").lower()
        if again == "y":
            break
        elif again == "n":
            break


if __name__ == "__main__":
    main()
