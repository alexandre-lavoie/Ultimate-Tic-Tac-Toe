# CS Games Tryout: Artificial Intelligence
Welcome to the second tryout for CS Games. Your task for this tryout will be to
create a bot to win at the game of [Ultimate Tic-Tac-Toe](https://ultimate-t3.herokuapp.com/rules) make sure to get familliar with the rules.

## Installation
If you do not have **Python3** installed you can get it [here](https://www.python.org/downloads/release/python-374/).

Create a virtual environment and install the requirements:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Program execution
To test you bot execute the following command:
```bash
python3 driver.py path/to/bot-1 path/to/bot-2
```
** Do not include the `.py` extension**

If you want to debug your bot it might be useful to use the `--verbose` flag as follows:
```bash
python3 driver.py path/to/bot-1 path/to/bot-2 --verbose
```

# Your Task
You will only have to modify the file `my_bot.py`.
You have to change the value of `self.team_name` to your team name.
Afterwrds, implement the logic for your bot in the `my_bot.py` module.
You are allowed to add function as needed.
The `move` method will have to return a move `X/Y` were `X` and `Y` are geographic coordiantes among the followings: NW, N, NE, W, C, E, SW, S, SE.
e.g. "NW/C" would place a move in the center (small) of the top-right (big).

# Board Visualization
```
         NW   N  NE   W   C   E  SW   S  SE 
    NW  ['.' '.' '.' '.' '.' '.' '.' '.' '.']
    N   ['.' '.' '.' '.' '.' '.' '.' '.' '.']
    NE  ['.' '.' '.' '.' '.' '.' '.' '.' '.']
    W   ['.' '.' '.' '.' '.' '.' '.' '.' '.']
    C   ['.' '.' '.' '.' '.' '.' '.' '.' '.']
    E   ['.' '.' '.' '.' '.' '.' '.' '.' '.']
    SW  ['.' '.' '.' '.' '.' '.' '.' '.' '.']
    S   ['.' '.' '.' '.' '.' '.' '.' '.' '.']
    SE  ['.' '.' '.' '.' '.' '.' '.' '.' '.']
```

Where rows represent coordinates in the big board while columns represent coordinates in the small board.

## Constraint
* The first valid move your bot do will be registered
* Your bot can attempt as many move as it wants