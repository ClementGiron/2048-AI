## Libraries ##

import numpy as np
import pygame
from constants import *


## Functions ##

# create a label object
# return label center and dimensions
def label_object(text, font, col):
    surf = font.render(text, True, col)
    return surf, surf.get_rect()


# update the leaderboard file
def update_leaderboard(scoresPath, newScore, newName):

    # read leaderboard file
    leaderboard = []
    with open(scoresPath) as f:
        for line in f.readlines():
            leaderboard.append(line.strip().split())

    # get names
    names = [e[0] for e in leaderboard]
    names.append(newName)

    # get scores
    scores = [int(float(e[1])) for e in leaderboard]
    scores.append(newScore)

    # sort
    sortedIdx = np.argsort(scores)

    # write
    with open(scoresPath, 'w') as f:
        for idx in reversed(sortedIdx[-5:]):
            f.write("{} {}\n".format(names[idx], scores[idx]))

    return None


# 4-tuple network to index row in the related numpy array
def index_row(l, b=B):
    res = ""
    for e in l:
        res += HEX_DICT[e]

    return int(res, b)


# for a given board, the related network arrays rows
def networks_rows(board, networks=TUPLE_NETWORKS, netnames=NETWORKS_NAMES, b=B):
    res = []
    for net in netnames:
        values_net = [int(np.log2(board[x,y])) if (board[x,y] > 0) else 0 for x,y in networks[net]]
        res.append(index_row(values_net, b))

    return res
