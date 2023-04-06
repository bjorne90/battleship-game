<div align="center">
  <a href="https://bjorne90.github.io/math-games-for-children/index.html" target="_blank">
    <img src="assets/images/logo.jpg" alt="Logo" width="250" height="100">
  </a>

  <h3 align="center">Project 3 - Battleship game in Pyhton</h3>

  <p align="center">
    My Python project for Code Institute. A Battleship game.
    <br />
    <br />
    <a href="https://battleship-game-bc.herokuapp.com/" target="_blank">View Demo Website</a>
  </p>
</div>

## Table of Contents
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#Features">Features</a></li>
    <li><a href="#How-to-Play">How to Play</a></li>
    <li><a href="#Game-Instructions">Game Instructions</a></li>
    <li><a href="#Known-Bugs-and-Fixes">Known Bugs and Fixes</a></li>
    <li><a href="#Data-Model">Data Model</a></li>
    <li><a href="#Validating-&-Testing">Validating & Testing</a></li>
    <li><a href="#Credits">Credits</a></li>
  </ol>
</details>
<br />


# Python Battleship Game 🗺️

Battleship is a classic grid-based strategy game where the player competes against the computer by guessing the locations of its hidden fleet of ships. The objective is to sink all of the computer's ships within a limited number of turns.

![Mockup of the game](assets/images/mockupscreen.png)

# Features

- Choose between three difficulty levels: easy, medium, and hard
- Random ship placement for the computer's fleet
- Customizable fleet configuration and grid size based on the chosen difficulty level
- Score tracking and leaderboard to save top 10 players' scores
- Age and name input for a more personalized experience
- Reads and writes name, age and score to Google Sheet

  ![Features of the game](assets/images/features.png)

## How to Play

1. Clone or download this repository
2. Run the Battleship game in a Python 3 environment using the following command: `python battleship.py`
3. Follow the on-screen instructions to provide your name, age, and desired difficulty level
4. Start guessing the locations of the computer's ships by entering the row and column numbers
5. Try to sink all of the computer's ships within the given number of turns
6. You can also play it via Demo link in the top of whis README

![Fun Math Game Screenshot 2](assets/images/howtoplay.png)

## Game Instructions

1. In this game, you'll try to sink a fleet of ships hidden on a grid by guessing their positions.
2. You'll have a limited number of turns to guess their locations, and the game will show you whether your guess was a hit, miss, or a duplicate guess.
3. To make a guess, enter the row and column of the cell you want to target.
4. Good luck!

## Scoring

Players earn points for each successful hit. The points earned for a hit depend on the type of ship hit and the ship's size. The top 10 players' scores will be displayed on the scoreboard.

![Scoreboard of the game](assets/images/scoring.png)

---

## Known Bugs and Fixes

* Write name, age and score to the top 10 list **(*Solved*)**
* No information came out to the leaderboard **(*Solved*)**
* Syntax error when game ended, no information saved **(*Solved*)**
* The gameboard was flashing turing play, trying to change os.system to termclear, without result.
  Fixing it by make *'guess_row, guess_col = user_guess(player_board)'* inside the *'while turns > 0:' loop.* **(*Solved*)**
* The top 10 scoreboard dont show when player wins by sinking all ships **(*Solved*)**
* The computers score if there are a hit is not always showing **(*Not Solved*)**

* A fix for the code is to make the *def main():* shorter. I haven't found a workaround for it yet. **(*In progress*)**

---

## Data Model

The Battleship game is designed with the following data model:

### Player

*A Player object represents a player in the game. It has the following attributes:*

* `name` (str): The player's name.
* `age` (int): The player's age.
* `score` (int): The player's score.

### Ship

*A Ship object represents a ship on the game board. It has the following attributes:*

* name (str): The name of the ship.
* size (int): The size of the ship (in grid units).
* hits (int): The number of times the ship has been hit.

### Board

A Board object represents a game board. It has the following attributes:

* size (int): The size of the board (in grid units).
* ships (list): A list of Ship objects on the board.
* grid (list): A 2D list representing the state of the board. Each element in the grid can be one of the following:
    * "0": An empty cell.
    * "S": A cell containing part of a ship.
    * "H": A cell containing a part of a ship that has been hit.
    * "M": A cell that has been fired at and missed.

### Game

A Game object represents a game instance. It has the following attributes:

* player (Player): The player object for the game.
* board_size (int): The size of the game board.
* difficulty (str): The difficulty level of the game ("easy", "medium", or "hard").
* player_board (Board): The player's game board.
* computer_board (Board): The computer's game board.
* fleet (list): A list of tuples representing the ships in the game fleet. Each tuple contains the size of the ship and its name.
* turns (int): The number of turns the player has to sink all the ships.
* ship_points (dict): A dictionary mapping ship names to their point values.
* hits (dict): A dictionary mapping ship names to the number of hits they have received.
* total_ship_sizes (int): The sum of the sizes of all the ships in the game fleet.
* score (int): The player's score.
* computer_score (int): The computer's score.

### Functions

The following functions are defined in the module:

* place_random_fleet(board, fleet): Places the ships in the fleet randomly on the given board.
* user_guess(board): Prompts the user for a guess on the given board.
* check_guess(board, row, col): Checks the result of a guess on the given board at the specified row and column.
* update_board(board, row, col, result): Updates the given board based on the result of a guess at the specified row and column.
* computer_guess(board): Generates a random guess for the computer on the given board.
* read_scores_from_sheet(): Reads the game scores from a Google Sheet.
* write_score_to_sheet(name, age, score): Writes the player's name, age, and score to a Google Sheet.
* print_board(board): Prints the given board in a human-readable format.
* print_boards(player_board, computer_board, name): Prints the player and computer boards side by side.
* print_scoreboard(): Prints the top 10 players in right order




---

## Validating & Testing

- Validate the code from Code Institutes [CI Pyhton Linter](https://pep8ci.herokuapp.com//) without any error.

  ![Screenshot from CI Python Linter](assets/images/testing1.png)

- The game is tested in diffrent browsers, Chrome, Safari and Firefox, without problem.
- The game is also tested in VScode desktop version
---

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Requirements

- Python 3.x
- Library: google-api-python-client
```bash
pip install google-api-python-client
```

---

## Customization

To customize the game settings, you can modify the fleet configuration, grid size, and number of turns in the `main()` function of the `battleship.py` file. The default settings are as follows:

- Easy: Grid size of 5x5, fleet consisting of a destroyer (2 cells), cruiser (3 cells), and battleship (4 cells), and 10 turns.
- Medium: Grid size of 7x7, fleet consisting of a destroyer (2 cells), cruiser (3 cells), battleship (4 cells), and aircraft carrier (5 cells), and 15 turns.
- Hard: Grid size of 10x10, fleet consisting of a destroyer (2 cells), cruiser (3 cells), battleship (4 cells), aircraft carrier (5 cells), and an additional aircraft carrier (6 cells), and 20 turns.

To customize the game further, you can adjust the ship points, ASCII art, or instructions displayed during the game.

----

## Contributing

If you would like to contribute to this project, please feel free to submit a pull request or open an issue on GitHub. I appreciate any suggestions or improvements to the game.

---

## Credits

* Thanks to the creators of the original Battleship game for inspiring this project
* Pythons documentation about PEP8 guidelines
* The art in the game is with help from [ASCII-Generator](https://ascii-generator.site/)
* Logo is downloaded from [FreePik](https://www.freepik.com/free-vector/illustration-transportation-icon_2944816.htm#query=battleship%20logo&position=28&from_view=keyword&track=ais)
* Thanks for the guides at [The Python Package Index](https://pypi.org/)

---

## Author

- Björn Centio - _Initial work_ - [Bjorne90](https://github.com/bjorne90)

---

## Contact

If you have any questions or suggestions, feel free to reach out to me at bjce90@gmail.com
