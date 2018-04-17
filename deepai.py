## Libraries ##
import numpy as np
import json
import os
from game import *
from constants import *
import keras
from keras.models import Sequential, model_from_json
from keras.layers.core import Dense, Flatten
from keras.optimizers import sgd
from keras.layers import Conv2D, MaxPooling2D, Activation, AveragePooling2D,Reshape, BatchNormalization


## Class Memory ##

class Memory(object):
    def __init__(self, max_memory=100):
        self._max_memory = max_memory
        self._memory = list()

    def remember(self, m):
        self._memory.append(m)
        if len(self._memory) > self._max_memory:
            self._memory.pop(0)

    def random_access(self):
        i = np.random.randint(0, len(self._memory))
        return self._memory[i]


## Class DeepAI ##

class DeepAI(object):
    def __init__(self, name, warm_start=False, batch_size=32, discount=0.99, mem_max=100, lr=0.1):
        self._name = name
        self._batch_size = batch_size
        self._discount = discount
        self._lr = lr
        self._memory = Memory(mem_max)
        if warm_start:
            self.load_model(name)
        else:
            self.init_model()
            if not os.path.exists('./AIs'):
                os.makedirs('./AIs')
            if not os.path.exists('./AIs/'+self._name):
                os.makedirs('./AIs/'+self._name)


    def init_model(self):
        model = Sequential()
        #model.add(Conv2D(filters=32, kernel_size=(3, 3), activation='relu', input_shape=(4, 4, 1)))
        #model.add(Conv2D(filters=16, kernel_size=(2, 2), activation='relu'))
        #model.add(Flatten())
        #model.add(Dense(4))
        model.add(Flatten(input_shape=(4, 4, 1)))
        model.add(Dense(128, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(16, activation='relu'))
        model.add(Dense(4))
        model.compile(sgd(lr=self._lr, decay=1e-4, momentum=0.0), "mse")
        self._model = model
        return None


    def load_model(self, name):
        name_model = "./AIs/{}/model.json".format(name)
        name_weights = "./AIs/{}/weights.h5".format(name)
        with open(name_model, "r") as jfile:
            model = model_from_json(json.load(jfile))
        model.load_weights(name_weights)
        model.compile("sgd", "mse")
        self._model = model
        return None


    def save_model(self, name):
        name_model = "./AIs/{}/model.json".format(name)
        name_weights = "./AIs/{}/weights.h5".format(name)
        self._model.save_weights(name_weights, overwrite=True)
        with open(name_model, "w") as outfile:
            json.dump(self._model.to_json(), outfile)
        return None


    def reinforce(self, state, next_state, action, reward, game_over):
        self._memory.remember([state, next_state, action, reward, game_over])
        X = np.zeros((self._batch_size, 4, 4, 1))
        y = np.zeros((self._batch_size, 4))
        for i in range(self._batch_size):
            s, ns, a, r, go = self._memory.random_access()
            r = r
            X[i, :, :, 0] = s
            Qs, Q_ns = self._model.predict(np.vstack((s[np.newaxis, :], ns[np.newaxis, :]))[:, :, :, np.newaxis])
            y[i, :] = Qs
            if go:
                y[i, a] = r
            else:
                y[i, a] = r + self._discount*np.max(Q_ns)
        y = np.clip(y, -16384, 16384)

        loss = self._model.train_on_batch(X, y)

        return loss


    def train(self, epochs, eps_function):
        for i in range(epochs):
            eps = eps_function(i)
            g = Game()
            check = True
            loss = []
            while check:
                s = g._board.copy()
                u = np.random.rand()
                if u < eps:
                    a = np.random.randint(0, 4)
                else:
                    a = np.argmax(self._model.predict(s[np.newaxis, :, :, np.newaxis]))
                check, r = g.round(INT_TO_ACT[a])
                ns = g._board.copy()
                go = not(check)
                loss.append(self.reinforce(s, ns, a, r, go))

            print("Epoch {:03d}/{:03d} | Loss {:.4f} | Score {}"
              .format(i+1, epochs, np.mean(loss), g._score))
        self.save_model(self._name)
        return None


ai = DeepAI("testdeep", warm_start=False, discount=0.6)
eps_function = lambda x: 0.001
ai.train(10000, eps_function)
