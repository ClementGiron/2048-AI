## Libraries ##

import pygame


## Game ##

INT_TO_ACT = {
0: "up",
1: "right",
2: "down",
3: "left"
}

 ## PyGame constants ##

# Fonts
pygame.init()
BUTTONFONT = pygame.font.SysFont("monospace", 25)
SMALLBUTTONFONT = pygame.font.SysFont("monospace", 15)
TILESFONT = pygame.font.SysFont("courier", 20, bold=True)
FONT2048 = pygame.font.SysFont("courier", 30, bold=True)
LEADERBOARDFONT = pygame.font.SysFont("courier", 20, bold=True)

# CPU iterations per second
CLOCK_TICK = 10

# Colors
RED = (163, 29, 69)
RED2 = (210, 70, 120)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACK = (224, 224, 224)
C0 = (255, 255, 255)
C2 = (255, 204, 153)
C4 = (255, 178, 102)
C8 = (255, 255, 153)
C16 = (255, 255, 102)
C32 = (204, 255, 153)
C64 = (178, 255, 102)
C128 = (153, 255, 153)
C256 = (102, 255, 102)
C512 = (153, 255, 204)
C1024 = (102, 255, 178)
C2048 = (153, 255, 255)
C4096 = (102, 255, 255)
C8192 = (153, 204, 255)
C16384 = (102, 178, 255)

TILES_COLORS = {
0: C0,
2: C2,
4: C4,
8: C8,
16: C16,
32: C32,
64: C64,
128: C128,
256: C256,
512: C512,
1024: C1024,
2048: C2048,
4096: C4096,
8192: C8192,
16384: C16384
}

## AI constants ##

# learning parameter
ALPHA = 0.0025

# number of possible values for a tile
B = 15

# hex encoding of the values
HEX_DICT = {
0: '0',
1: '1',
2: '2',
3: '3',
4: '4',
5: '5',
6: '6',
7: '7',
8: '8',
9: '9',
10: 'a',
11: 'b',
12: 'c',
13: 'd',
14: 'e',
15: 'f'
}

# tuple networks coordinates
TUPLE_NETWORKS = {
'sq1': [(0, 0), (0, 1), (1, 1), (1, 0)],
'sq2': [(0, 1), (0, 2), (1, 2), (1, 1)],
'sq3': [(0, 2), (0, 3), (1, 3), (1, 2)],
'sq4': [(1, 0), (1, 1), (2, 1), (2, 0)],
'sq5': [(1, 1), (1, 2), (2, 2), (2, 1)],
'sq6': [(1, 2), (1, 3), (2, 3), (2, 2)],
'sq7': [(2, 0), (2, 1), (3, 1), (3, 0)],
'sq8': [(2, 1), (2, 2), (3, 2), (3, 1)],
'sq9': [(2, 2), (2, 3), (3, 3), (3, 2)],
'h1': [(0, 0), (0, 1), (0, 2), (0, 3)],
'h2': [(1, 0), (1, 1), (1, 2), (1, 3)],
'h3': [(2, 0), (2, 1), (2, 2), (2, 3)],
'h4': [(3, 0), (3, 1), (3, 2), (3, 3)],
'v1': [(0, 0), (1, 0), (2, 0), (3, 0)],
'v2': [(0, 1), (1, 1), (2, 1), (3, 1)],
'v3': [(0, 2), (1, 2), (2, 2), (3, 2)],
'v4': [(0, 3), (1, 3), (2, 3), (3, 3)]
}

# names of the networks
NETWORKS_NAMES = ['sq1', 'sq2', 'sq3', 'sq4', 'sq5', 'sq6', 'sq7', 'sq8', 'sq9',
'h1', 'h2', 'h3', 'h4', 'v1', 'v2', 'v3', 'v4']
