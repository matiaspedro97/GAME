# Battle Game

A simple battle game developed in Python using the Pygame library.

## Description

The Battle Game is a 2D game where players control characters and engage in battles against each other. The game features a top-down perspective, real-time combat, and various weapons and abilities for the players to utilize.

## Features

- Real-time battles in PVP style (1vs1)
- Player input for movement and attacks
- Health and energy management
- Interactive game environment
- Sound and visual effects

## How to Play

- Use the **`WADS`** keys (Player 1) or **`arrowkeys`** (Player 2) to control the character's movement.
- Press the **`R key`** (Player 1) or the **`spacebar`** (Player 2) to attack.
- Follow the in-game instructions for additional controls or features.


## Installation

1. Clone the repository:
```
git clone https://github.com/matiaspedro97/GAME.git
```


2. Install the required dependencies:
 - Build the development environment:
```bash 
python3 -m virtualenv -p /path/to/python3.7 .{your-env} 

. .{your-env}/bin/activate  # Linux
. .{your-env}/Scripts/Activate.ps1  # Windows

# Install dependencies
pip install -r requirements/requirements-dev.txt
```

- Activate the desired environment by doing:
```bash
. .{your-env}/bin/activate  # Linux
.{your-env}/Scripts/Activate.ps1  # Windows
```


3. Run the game:
```python
python src/runs/run_game.py
```


## Launch the Game as an executable file
1. Use pyinstaller library and run the following command:
```
pyinstaller --onefile --paths=src/ src/runs/run_game.py
```

2. Remove the .exe file outside the dist/ folder generated after the command runs

3. Launch the .exe file

4. Have fun :)


## Demo
Take a look at the battle game demo running from the terminal

![OMD, that smile...](img/demo.gif)

## Contributions

Contributions are welcome! If you want to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive commit messages.
4. Push your changes to your forked repository.
5. Submit a pull request detailing your changes.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [Pygame](https://www.pygame.org) - The library used for game development.

## Contact

For any questions or inquiries, please contact matiaspedro97@gmail.com
