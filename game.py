## Libraries ##

import numpy as np


## Class game ##

class Game:

    """
    A game is defined by:
    - a 4x4 board (_board)
    - the score (_score)
    - the last played action (_lastAction)
    - the number of actions played from the beginning (_nbActions)
    """

    # init function
    def __init__(self):
        self.init_board()
        self._score = 0
        self._lastAction = None
        self._nbActions = 0


    # initialize the board with 2 tiles
    def init_board(self):
        self._board = np.zeros((4, 4))
        free = np.where(self._board == 0)
        tiles = np.random.choice(range(len(free[0])), size=2, replace=False)
        value1 = np.random.choice([2, 4], p=[0.9, 0.1])
        value2 = np.random.choice([2, 4], p=[0.9, 0.1])
        self._board[free[0][tiles[0]], free[1][tiles[0]]] = value1
        self._board[free[0][tiles[1]], free[1][tiles[1]]] = value2
        return None


    # add a tile at a free place
    def add_tile(self):
        free = np.where(self._board == 0)
        tile = np.random.choice(range(len(free[0])))
        value = np.random.choice([2, 4], p=[0.9, 0.1])
        self._board[free[0][tile], free[1][tile]] = value
        return None


    # play an action, modify the board, return the score of the play
    def play(self, action):
        # return
        score = 0

        # move tiles
        for i in range(4):

            # get tiles of the i-th line
            if action == 'left':
                l = [e for e in self._board[i, :] if e != 0]
            elif action == 'right':
                l = list(reversed([e for e in self._board[i, :] if e != 0]))
            elif action == 'up':
                l = [e for e in self._board[:, i] if e != 0]
            elif action == 'down':
                l = list(reversed([e for e in self._board[:, i] if e != 0]))

            # move and melt
            k = 0
            while (k < len(l)-1):
                if l[k] == l[k+1]:
                    score += l[k]
                    l[k] *= 2
                    l = l[:k+1] + l[k+2:]
                k += 1
            l = l + [0 for e in range(4-len(l))]

            # replace
            if action == 'left':
                self._board[i, :] = l
            if action == 'right':
                self._board[i, :] = list(reversed(l))
            if action == 'up':
                self._board[:, i] = l
            if action == 'down':
                self._board[:, i] = list(reversed(l))

        return score


    # check if it is possible to play again
    def check(self):
        # if there is a blank tile
        if len(np.where(self._board == 0)[0]) > 0:
            return True
        # otherwise
        else:
            # if a merge can append
            for i in range(3):
                for j in range(4):
                    if self._board[i,j] == self._board[i+1,j]:
                        return True
            for i in range(4):
                for j in range(3):
                    if self._board[i,j] == self._board[i,j+1]:
                        return True

            return False


    # play a round: move tiles, add new tile and check if the game is finished
    # return check and score
    def round(self, action):
        board = self._board.copy()
        score = self.play(action)
        if not np.all(self._board == board):
            self.add_tile()
            self._score += score
            self._lastAction = action
            self._nbActions += 1

        check = self.check()
        return check, score


    # run the game on console for debugging
    def run_console(self):
        self.init_board()
        check = True
        while check:
            action = input("Quelle action? [left/right/up/down]")
            check, score = self.round(action)
            print('last score', score)
            print('total score', self._score)
            print('last action', self._lastAction)
            print('number of actions', self._nbActions)
            print('Board\n', self._board)
        return None
