## Libraries ##

from game import *
from ai import *
from utils import *
from constants import *
from tqdm import tqdm
import matplotlib.pyplot as plt
import os
import sys


## script ##

if __name__ == '__main__':

    # Load AI
    nameAI = sys.argv[1].strip()
    epochs = int(sys.argv[2].strip())
    ai = ArtificialIntelligence(nameAI, warm_start=True)
    scores = []
    won = []

    # Play
    for _ in tqdm(range(epochs)):
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
                v = ai.evaluate(board, a)
                if v != None:
                    if v > bestScore:
                        bestScore = v
                        bestAction = a

            check, r = g.round(bestAction)
        if np.max(g._board) >= 2048:
            won.append(1)
        else:
            won.append(0)
        scores.append(g._score)


    # plot
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.canvas.set_window_title('Statistics on {} AI'.format(nameAI))
    fig.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)

    bp = ax.boxplot(scores, notch=0, sym='+', vert=1, whis=1.5)
    ax.axhline(np.mean(scores), label='mean')
    ax.axhline(np.max(scores), label='max', color='r')
    ax.axhline(np.min(scores), label='min', color='g')
    plt.title('Scores distribution on {} games'.format(epochs))
    plt.legend(loc='best')
    print('Percentage of won games: {}'.format(100*round(np.sum(won)/len(won), 3)))
    plt.show()
