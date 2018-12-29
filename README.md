![](https://i.imgur.com/nXCZXwm.png)


# PyChessBot

PyChessBot is a chess bot written in Python. 

Disclaimer
----------
- I do **NOT** endorse any sort of cheating. This program should be used for educational purposes only, or against offline bots.

Installing
----------
- Clone the repository or [download the zip file from GitHub](https://github.com/LouisAsanaka/PyChessBot/archive/master.zip)
- Install dependencies:

        pip install -r requirements.txt

- Download a chess engine of your choice | [Stockfish 10](https://stockfishchess.org/files/stockfish-10-win.zip)
- Extract the zip, and create a folder called "bin" in the root program folder
- Rename the engine executable to "engine.exe"
- Place the renamed executable in the "bin" folder

- Run the program:

        cd PyChessBot
        python main.py
    
Usage
-----

- Toggle between play as white and play as black mode
- Click on start to select the boundaries of the board on the screen
Long click the top-left corner until indicated in the log window,
then repeat for the bottom-right corner.
- The bot will start playing _immediately_ after selection
- Hold the **CTRL** key to pause the bot (Not implemented yet)

Notes
-----

- Do **NOT** move the mouse while the bot is playing, or move any window over the board.
- Make the colors of the board different from the colors of the pieces
- If you can, turn **off** piece animations
- The sliders currently don't work yet
- The bot assumes that the opponent always promotes to a queen, so it **WILL** malfunction if they promote to something else
- The bot can promote to other pieces, but only on chess.com


Citation
--------
Logo Sources:
- [Python Logo](https://commons.wikimedia.org/wiki/File:Python-logo-notext.svg)
- [Chess Pawn](https://www.clipartmax.com/middle/m2H7i8b1m2H7m2b1_pawn-chess-figure-chess/)