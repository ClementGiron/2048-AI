## Libraries ##

import numpy as np
from utils import *
from constants import *
from game import *
from tqdm import tqdm
import os


## Class AI ##

class ArtificialIntelligence:

    """
    An AI is defined by:
    - a name (_name)
    - a dictionary of look-up tables, one for each network (_lut)
    In the init function, warm_start is true to train or use a pre-trained AI,
    false to create a new AI.
    """

    # init function
    def __init__(self, name, warm_start=False):
        self._name = name
        self._lut = {}
        if warm_start:
            for net in NETWORKS_NAMES:
                self._lut[net] = np.load('./AIs/{}/{}.npy'.format(self._name, net))
        else:
            for net in NETWORKS_NAMES:
                self._lut[net] = np.zeros((B**4, 1))
            if not os.path.exists('./AIs'):
                os.makedirs('./AIs')
            if not os.path.exists('./AIs/'+self._name):
                os.makedirs('./AIs/'+self._name)


    # compute the afterstate of a state given an action
    # return afterstate and score related to this action
    def compute_afterstate(self, board, action):
        # return
        score = 0
        afterstate = np.zeros((4, 4))

        # move tiles
        for i in range(4):
            if action == 'left':
                l = [e for e in board[i, :] if e != 0]
            elif action == 'right':
                l = list(reversed([e for e in board[i, :] if e != 0]))
            elif action == 'up':
                l = [e for e in board[:, i] if e != 0]
            elif action == 'down':
                l = list(reversed([e for e in board[:, i] if e != 0]))
            # if no possible action
            else:
                return board, (-16384 + np.max(board))
            k = 0
            while (k < len(l)-1):
                if l[k] == l[k+1]:
                    score += l[k]
                    l[k] *= 2
                    l = l[:k+1] + l[k+2:]
                k += 1
            l = l + [0 for e in range(4-len(l))]
            if action == 'left':
                afterstate[i, :] = l
            if action == 'right':
                afterstate[i, :] = list(reversed(l))
            if action == 'up':
                afterstate[:, i] = l
            if action == 'down':
                afterstate[:,   i] = list(reversed(l))

        return afterstate, score


    # evaluate the value function of the afterstate given a state and an action
    def evaluate(self, board, action):
        value = 0
        afterstate, reward = self.compute_afterstate(board, action)
        if np.all(board == afterstate):
            return None
        else:
            for i,idx in enumerate(networks_rows(afterstate)):
                value += self._lut[NETWORKS_NAMES[i]][idx, 0]
            value /= len(NETWORKS_NAMES)

            return reward + value


    # given a state, an action, the related reward, the afterstate and the next
    # state, update the value function
    def learn_evaluation(self, board, action, reward, afterstate, afterBoard):
        bestScore = -1e10
        bestAction = ''
        # find best action
        for a in ['up','right', 'down', 'left']:
            v = self.evaluate(afterBoard, a)
            if v != None:
                if v > bestScore:
                    bestScore = v
                    bestAction = a

        # compute afterstate
        afterAfterBoard, reward = self.compute_afterstate(afterBoard, bestAction)

        # update look-up tables
        afterstateNetworksRows = networks_rows(afterstate)
        afterAfterBoardNetworksRows = networks_rows(afterAfterBoard)
        for i,net in enumerate(NETWORKS_NAMES):
            self._lut[net][afterstateNetworksRows[i], 0] = self._lut[net][afterstateNetworksRows[i], 0] + \
            ALPHA*(reward + self._lut[net][afterAfterBoardNetworksRows[i], 0] - self._lut[net][afterstateNetworksRows[i], 0])

        return None


    # save the look-up tables of the AI
    def save(self):
        for net in NETWORKS_NAMES:
            np.save('./AIs/{}/{}'.format(self._name, net), self._lut[net])
        return None


    # iterate the learning process over N games
    def reinforce(self, N):

        scores = []

        for _ in range(N):

            # begin new game
            g = Game()
            check = True

            # while not lost
            while check:
                board = g._board.copy()
                # find best action
                bestScore = -1e10
                bestAction = ''
                for a in ['up','right', 'down', 'left']:
                    v = self.evaluate(board, a)
                    if v != None:
                        if v > bestScore:
                            bestScore = v
                            bestAction = a

                # learn
                afterstate, s = self.compute_afterstate(board, bestAction)
                check, r = g.round(bestAction)
                afterBoard = g._board.copy()
                self.learn_evaluation(board, bestAction, r, afterstate, afterBoard)

            #print(g._score)
            #print(g._board)
        # save the look-up tables
        self.save()

        return None


    # play without learning
    def play(self, board):
        # find best action
        bestScore = -1e10
        bestAction = ''
        for a in ['up','right', 'down', 'left']:
            v = self.evaluate(board, a)
            if v != None:
                if v > bestScore:
                    bestScore = v
                    bestAction = a
        return bestAction

#ai = ArtificialIntelligence('testmean', warm_start=False)
#ai.reinforce(5000)
