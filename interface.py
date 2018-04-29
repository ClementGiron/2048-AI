## Libraries ##
import pygame
from pygame.locals import *
import os
import time
from game import Game
from ai import ArtificialIntelligence
from utils import *
from constants import *


## Class Interface ##

class Interface:

    def __init__(self, img='layout.jpg', dim=(800, 450)):
        self._window = pygame.display.set_mode(dim)
        self._background = pygame.image.load(img).convert()
        self._state = "menu"
        self._score = 0
        self._max = 0
        self._clock = pygame.time.Clock()
        self._scoresPath = 'scores.txt'

        if not os.path.exists('./save'):
            os.makedirs('./save')
        if len(os.listdir('./save')) == 0:
            self._savedGame = False
        else:
            self._savedGame = True


    def display_menu(self):
        # Background
        self._window.blit(self._background, (0,0))

        titleSurf, titleRect = label_object("2048", FONT2048, BLACK)
        titleRect.center = (400, 20)
        self._window.blit(titleSurf, titleRect)

        # Play button
        pygame.draw.rect(self._window, RED, [300, 50, 200, 50], 0)
        playSurf, playRect = label_object("NEW GAME", BUTTONFONT, WHITE)
        playRect.center = (400, 75)
        self._window.blit(playSurf, playRect)

        # Saved game button
        if self._savedGame:
            pygame.draw.rect(self._window, RED, [300, 133, 200, 50], 0)
            savedSurf, savedRect = label_object("CONTINUE", BUTTONFONT, WHITE)
            savedRect.center = (400, 158)
            self._window.blit(savedSurf, savedRect)

        # Scores button
        pygame.draw.rect(self._window, RED, [300, 150+67*self._savedGame, 200, 50], 0)
        bestSurf, bestRect = label_object("BEST SCORES", BUTTONFONT, WHITE)
        bestRect.center = (400, 175+67*self._savedGame)
        self._window.blit(bestSurf, bestRect)

        # AI button
        pygame.draw.rect(self._window, RED, [300, 250+50*self._savedGame, 200, 50], 0)
        AISurf, AIRect = label_object("Watch AI", BUTTONFONT, WHITE)
        AIRect.center = (400, 275+50*self._savedGame)
        self._window.blit(AISurf, AIRect)

        return None


    def display_scores(self, scoresPath):
        # Background
        self._window.blit(self._background, (0,0))

        # Load leaderboard
        leaderboard = []
        with open(scoresPath) as f:
            for line in f.readlines():
                leaderboard.append(line.strip())

        # title leaderboard
        titleSurf, titleRect = label_object("LEADERBOARD", FONT2048, BLACK)
        titleRect.center = (400, 50)
        self._window.blit(titleSurf, titleRect)

        # Display leaderboard
        score_x = 300
        score_y = 100
        for i,e in enumerate(leaderboard):
            label = LEADERBOARDFONT.render("{}. {}".format(i+1, e), 1, BLACK)
            self._window.blit(label, (score_x, score_y))
            score_y += 30

        # Display menu button
        pygame.draw.rect(self._window, RED, [300, 300, 200, 50], 0)
        menuSurf, menuRect = label_object("BACK TO MENU", BUTTONFONT, WHITE)
        menuRect.center = (400, 325)
        self._window.blit(menuSurf, menuRect)

        return None


    def display_board(self, game):
        # draw board background
        pygame.draw.rect(self._window, BACK, [275, 100, 250, 250], 0)

        # draw tiles
        x_corner = 275
        y_corner = 100
        for i in range(4):
            for j in range(4):
                pygame.draw.rect(self._window, TILES_COLORS[game._board[i,j]],
                [x_corner+10*(j+1)+50*j, y_corner+10*(i+1)+50*i, 50, 50], 0)
                if game._board[i,j] != 0:
                    tileSurf, tileRect = label_object(str(int(game._board[i,j])), TILESFONT, BLACK)
                    tileRect.center = (x_corner+10*(j+1)+50*j+25, y_corner+10*(i+1)+50*i+25)
                    self._window.blit(tileSurf, tileRect)
        return None


    def display_game(self, game):
        # Background
        self._window.blit(self._background, (0,0))

        # Game
        self.display_board(game)

        # Display menu button
        pygame.draw.rect(self._window, RED, [575, 330, 150, 40], 0)
        menuSurf, menuRect = label_object("BACK TO MENU", SMALLBUTTONFONT, WHITE)
        menuRect.center = (650, 350)
        self._window.blit(menuSurf, menuRect)

        # Display restart button
        pygame.draw.rect(self._window, RED, [575, 270, 150, 40], 0)
        restartSurf, restartRect = label_object("RESTART", SMALLBUTTONFONT, WHITE)
        restartRect.center = (650, 290)
        self._window.blit(restartSurf, restartRect)

        # Display save button
        if self._state != "ai":
            pygame.draw.rect(self._window, RED, [575, 210, 150, 40], 0)
            saveSurf, saveRect = label_object("SAVE", SMALLBUTTONFONT, WHITE)
            saveRect.center = (650, 230)
            self._window.blit(saveSurf, saveRect)

        # title
        titleSurf, titleRect = label_object("2048", FONT2048, BLACK)
        titleRect.center = (400, 50)
        self._window.blit(titleSurf, titleRect)

        # score
        scoreSurf, scoreRect = label_object("Score: {}".format(int(game._score)), TILESFONT, BLACK)
        scoreRect.center = (650, 125)
        self._window.blit(scoreSurf, scoreRect)

        # plays
        scoreSurf, scoreRect = label_object("{} plays".format(game._nbActions), TILESFONT, BLACK)
        scoreRect.center = (650, 175)
        self._window.blit(scoreSurf, scoreRect)

        pygame.display.flip()

        return None


    def display_lost(self):
        # loose message
        result = "LOOSE" if self._max < 2048 else "WIN"
        looseSurf, looseRect = label_object("YOU {}! Your score: {}".format(result, self._score), FONT2048, BLACK)
        looseRect.center = (400, 100)
        self._window.blit(looseSurf, looseRect)

        # name message
        nameSurf, nameRect = label_object("Enter your name:", SMALLBUTTONFONT, BLACK)
        nameRect.center = (400, 160)
        self._window.blit(nameSurf, nameRect)

        return None


    def display_chooseAI(self):
        # loose message
        welcomeSurf, welcomeRect = label_object("Welcome to the AI mode!", FONT2048, BLACK)
        welcomeRect.center = (400, 100)
        self._window.blit(welcomeSurf, welcomeRect)

        # name message
        nameSurf, nameRect = label_object("Enter the name of the AI you want to watch playing:", SMALLBUTTONFONT, BLACK)
        nameRect.center = (400, 160)
        self._window.blit(nameSurf, nameRect)

        return None


    def run_menu(self):
        self.display_menu()
        pygame.display.flip()
        done = False
        res = "menu"
        while not done:
            self._clock.tick(CLOCK_TICK)
            for event in pygame.event.get():
                if event.type == QUIT:
                    res = "end"
                    done = True
                    break
                if event.type == MOUSEBUTTONDOWN and event.button == 1 \
                and event.pos[0] < 500 and event.pos[0] > 300 \
                and event.pos[1] > 50 and event.pos[1] < 100:
                    res = "game"
                    done = True
                if event.type == MOUSEBUTTONDOWN and event.button == 1 and self._savedGame\
                and event.pos[0] < 500 and event.pos[0] > 300 \
                and event.pos[1] > 133 and event.pos[1] < 183:
                    res = "savedgame"
                    done = True
                if event.type == MOUSEBUTTONDOWN and event.button == 1 \
                and event.pos[0] < 500 and event.pos[0] > 300 \
                and event.pos[1] > 150+67*self._savedGame and event.pos[1] < 200+67*self._savedGame:
                    res = "scores"
                    done = True
                if event.type == MOUSEBUTTONDOWN and event.button == 1 \
                and event.pos[0] < 500 and event.pos[0] > 300 \
                and event.pos[1] > 250+50*self._savedGame and event.pos[1] < 300+50*self._savedGame:
                    res = "ai"
                    done = True
        return res


    def run_game(self, saved=False):
        # re-init max
        self._max = 0
        # launch the game
        game = Game()

        if saved:
            game.load()
        if self._savedGame:
            game.destroy()
            self._savedGame = False

        #iterate while not lost
        done = False
        c = True
        while not done:
            # draw the board
            self._clock.tick(CLOCK_TICK)
            self.display_game(game)

            # get event
            for event in pygame.event.get():
                # quit
                if event.type == QUIT:
                    res = "end"
                    done = True

                # go back to menu
                if event.type == MOUSEBUTTONDOWN and event.button == 1 \
                and event.pos[0] < 725 and event.pos[0] > 575 \
                and event.pos[1] > 330 and event.pos[1] < 370:
                    res = "menu"
                    done = True

                # restart
                if event.type == MOUSEBUTTONDOWN and event.button == 1 \
                and event.pos[0] < 725 and event.pos[0] > 575 \
                and event.pos[1] > 270 and event.pos[1] < 310:
                    res = "game"
                    done = True

                # save
                if event.type == MOUSEBUTTONDOWN and event.button == 1 \
                and event.pos[0] < 725 and event.pos[0] > 575 \
                and event.pos[1] > 210 and event.pos[1] < 250:
                    res = "menu"
                    game.save()
                    self._savedGame = True
                    done = True

                # plays
                if event.type == KEYDOWN and event.key == K_UP:
                    c,s = game.round('up')
                if event.type == KEYDOWN and event.key == K_RIGHT:
                    c,s = game.round("right")
                if event.type == KEYDOWN and event.key == K_DOWN:
                    c,s = game.round("down")
                if event.type == KEYDOWN and event.key == K_LEFT:
                    c,s = game.round("left")
            if c == False:
                res = "lost"
                self._score = game._score
                self._max = np.max(game._board)
                done = True
        return res


    def run_scores(self, scoresPath):
        self.display_scores(scoresPath)
        pygame.display.flip()
        done = False
        res = "menu"

        while not done:
            self._clock.tick(CLOCK_TICK)
            for event in pygame.event.get():
                if event.type == QUIT:
                    res = "end"
                    done = True

                if event.type == MOUSEBUTTONDOWN and event.button == 1 \
                and event.pos[0] < 500 and event.pos[0] > 300 \
                and event.pos[1] > 300 and event.pos[1] < 350:
                    res = "menu"
                    done = True

        return res


    def run_lost(self):
        # Background
        self._window.blit(self._background, (0,0))

        # messages
        self.display_lost()

        # copied
        # thanks https://stackoverflow.com/questions/46390231/how-to-create-a-text-input-box-with-pygame
        font = TILESFONT
        input_box = pygame.Rect(300, 200, 200, 32)
        color_inactive = RED2
        color_active = RED
        color = color_inactive
        active = False
        text = ''
        done = False
        self._clock.tick(CLOCK_TICK)

        while not done:
            for event in pygame.event.get():
                if event.type == QUIT:
                    res = -1
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if input_box.collidepoint(event.pos):
                        # Toggle the active variable.
                        active = not active
                    else:
                        active = False
                    # Change the current color of the input box.
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            # Background
            self._window.blit(self._background, (0,0))

            # messages
            self.display_lost()

            # Render the current text.
            txt_surface = font.render(text, True, color)
            # Resize the box if the text is too long.
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            # Blit the text.
            self._window.blit(txt_surface, (input_box.x+5, input_box.y+5))
            # Blit the input_box rect.
            pygame.draw.rect(self._window, color, input_box, 2)

            pygame.display.flip()

        update_leaderboard(self._scoresPath, int(self._score), text)

        return "menu"


    def run_chooseAI(self):
        # Background
        self._window.blit(self._background, (0,0))

        # messages
        self.display_chooseAI()

        # copied
        # thanks https://stackoverflow.com/questions/46390231/how-to-create-a-text-input-box-with-pygame
        font = TILESFONT
        input_box = pygame.Rect(300, 200, 200, 32)
        color_inactive = RED2
        color_active = RED
        color = color_inactive
        active = False
        text = ''
        done = False
        self._clock.tick(CLOCK_TICK)

        while not done:
            for event in pygame.event.get():
                if event.type == QUIT:
                    res = -1
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if input_box.collidepoint(event.pos):
                        # Toggle the active variable.
                        active = not active
                    else:
                        active = False
                    # Change the current color of the input box.
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            # Background
            self._window.blit(self._background, (0,0))

            # messages
            self.display_chooseAI()

            # Render the current text.
            txt_surface = font.render(text, True, color)
            # Resize the box if the text is too long.
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            # Blit the text.
            self._window.blit(txt_surface, (input_box.x+5, input_box.y+5))
            # Blit the input_box rect.
            pygame.draw.rect(self._window, color, input_box, 2)

            pygame.display.flip()

        return "{}".format(text)


    def run_playAI(self, nameAI):
        # launch the game
        game = Game()

        # load the AI
        AI = ArtificialIntelligence(nameAI, warm_start=True)

        #iterate while not lost
        done = False
        c = True
        res = "menu"
        while not done:
            # draw the board
            self._clock.tick(CLOCK_TICK)
            self.display_game(game)

            # get event
            for event in pygame.event.get():
                # quit
                if event.type == QUIT:
                    res = "end"
                    done = True

                # go back to menu
                if event.type == MOUSEBUTTONDOWN and event.button == 1 \
                and event.pos[0] < 725 and event.pos[0] > 575 \
                and event.pos[1] > 330 and event.pos[1] < 370:
                    res = "menu"
                    done = True

                # restart
                if event.type == MOUSEBUTTONDOWN and event.button == 1 \
                and event.pos[0] < 725 and event.pos[0] > 575 \
                and event.pos[1] > 270 and event.pos[1] < 310:
                    res = "ai"
                    done = True

            time.sleep(0.5)
            # find best play
            a = AI.play(game._board)
            # play
            c,s = game.round(a)
            if c == False:
                self._score = game._score
                update_leaderboard(self._scoresPath, int(self._score), AI._name)
                done = True
        return res


    def run(self):
        done = False
        while not done:
            if self._state == "menu":
                self._state = self.run_menu()
            elif self._state == "game":
                self._state = self.run_game()
            elif self._state == "savedgame":
                self._state = self.run_game(saved=True)
            elif self._state == "lost":
                self._state = self.run_lost()
            elif self._state == "scores":
                self._state = self.run_scores(self._scoresPath)
            elif self._state == "ai":
                pathAI = self.run_chooseAI()
                self._state = self.run_playAI(pathAI)
            elif self._state == "end":
                done = True


## Execution ##

if __name__ == '__main__':
    pygame.init()
    i = Interface()
    i.run()
