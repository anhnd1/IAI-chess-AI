import chess

MATERIAL_POINT = (0, 100, 305, 305, 405, 1050, 999999)
MATE_SCORE = 999999

Midgame = 5255
Endgame = 435

BPAWN_MG = [100,  100,  100,  100,  100,  100,  100,  100,
           176,  214,  147,  194,  189,  214,  132,   77,
           82,   88,  106,  113,  150,  146,  110,   73,
           67,   93,   83,   95,   97,   92,   99,   63,
           55,   74,   80,   89,   94,   86,   90,   55,
           55,   70,   68,   69,   76,   81,  101,   66,
           52,   84,   66,   60,   69,   99,  117,   60,
           100,  100,  100,  100,  100,  100,  100,  100]

BKNIGHT_MG = [116,  228,  271,  270,  338,  213,  278,  191,
             225,  247,  353,  331,  321,  360,  300,  281,
             258,  354,  343,  362,  389,  428,  375,  347,
             300,  332,  325,  360,  349,  379,  339,  333,
             298,  322,  325,  321,  337,  332,  332,  303,
             287,  297,  316,  319,  327,  320,  327,  294,
             276,  259,  300,  304,  308,  322,  296,  292,
             208,  290,  257,  274,  296,  284,  293,  284]

BBISHOP_MG = [292,  338,  254,  283,  299,  294,  337,  323,
             316,  342,  319,  319,  360,  385,  343,  295,
             342,  377,  373,  374,  368,  392,  385,  363,
             332,  338,  356,  384,  370,  380,  337,  341,
             327,  354,  353,  366,  373,  346,  345,  341,
             335,  350,  351,  347,  352,  361,  350,  344,
             333,  354,  354,  339,  344,  353,  367,  333,
             309,  341,  342,  325,  334,  332,  302,  313]

BROOK_MG = [493,  511,  487,  515,  514,  483,  485,  495,
           493,  498,  529,  534,  546,  544,  483,  508,
           465,  490,  499,  497,  483,  519,  531,  480,
           448,  464,  476,  495,  484,  506,  467,  455,
           442,  451,  468,  470,  476,  472,  498,  454,
           441,  461,  468,  465,  478,  481,  478,  452,
           443,  472,  467,  476,  483,  500,  487,  423,
           459,  463,  470,  479,  480,  480,  446,  458]

BQUEEN_MG = [865,  902,  922,  911,  964,  948,  933,  928,
            886,  865,  903,  921,  888,  951,  923,  940,
            902,  901,  907,  919,  936,  978,  965,  966,
            881,  885,  897,  894,  898,  929,  906,  915,
            907,  884,  899,  896,  904,  906,  912,  911,
            895,  916,  900,  902,  904,  912,  924,  917,
            874,  899,  918,  908,  915,  924,  911,  906,
            906,  899,  906,  918,  898,  890,  878,  858]

BKING_MG = [-11,   70,   55,   31,  -37,  -16,   22,   22,
            37,   24,   25,   36,   16,    8,  -12,  -31,
            33,   26,   42,   11,   11,   40,   35,   -2,
             0,   -9,    1,  -21,  -20,  -22,  -15,  -60,
           -25,   16,  -27,  -67,  -81,  -58,  -40,  -62,
             7,   -2,  -37,  -77,  -79,  -60,  -23,  -26,
            12,   15,  -13,  -72,  -56,  -28,   15,   17,
            -6,   44,   29,  -58,    8,  -25,   34,   28]

WPAWN_MG = [100,  100,  100,  100,  100,  100,  100,  100,
            52,   84,   66,   60,   69,   99,  117,   60,
            55,   70,   68,   69,   76,   81,  101,   66,
            55,   74,   80,   89,   94,   86,   90,   55,
            67,   93,   83,   95,   97,   92,   99,   63,
            82,   88,  106,  113,  150,  146,  110,   73,
            176, 214,  147,  194,  189,  214,  132,   77,
           100,  100,  100,  100,  100,  100,  100,  100]

WKNIGHT_MG = [208, 290, 257, 274, 296, 284, 293, 284, 
             276, 259, 300, 304, 308, 322, 296, 292, 
             287, 297, 316, 319, 327, 320, 327, 294, 
             300, 332, 325, 360, 349, 379, 339, 333, 
             298, 322, 325, 321, 337, 332, 332, 303, 
             258, 354, 343, 362, 389, 428, 375, 347, 
             225, 247, 353, 331, 321, 360, 300, 281, 
             116, 228, 271, 270, 338, 213, 278, 191]

WBISHOP_MG = [309, 341, 342, 325, 334, 332, 302, 313, 
             333, 354, 354, 339, 344, 353, 367, 333, 
             335, 350, 351, 347, 352, 361, 350, 344, 
             332, 338, 356, 384, 370, 380, 337, 341, 
             327, 354, 353, 366, 373, 346, 345, 341, 
             342, 377, 373, 374, 368, 392, 385, 363, 
             316, 342, 319, 319, 360, 385, 343, 295, 
             292, 338, 254, 283, 299, 294, 337, 323]

WROOK_MG = [459, 463, 470, 479, 480, 480, 446, 458, 
           443, 472, 467, 476, 483, 500, 487, 423, 
           441, 461, 468, 465, 478, 481, 478, 452, 
           448, 464, 476, 495, 484, 506, 467, 455, 
           442, 451, 468, 470, 476, 472, 498, 454, 
           465, 490, 499, 497, 483, 519, 531, 480, 
           493, 498, 529, 534, 546, 544, 483, 508, 
           493, 511, 487, 515, 514, 483, 485, 495]

WQUEEN_MG = [906, 899, 906, 918, 898, 890, 878, 858, 
            874, 899, 918, 908, 915, 924, 911, 906, 
            895, 916, 900, 902, 904, 912, 924, 917, 
            881, 885, 897, 894, 898, 929, 906, 915, 
            907, 884, 899, 896, 904, 906, 912, 911, 
            902, 901, 907, 919, 936, 978, 965, 966, 
            886, 865, 903, 921, 888, 951, 923, 940, 
            865, 902, 922, 911, 964, 948, 933, 928]

WKING_MG = [-6, 44, 29, -58, 8, -25, 34, 28, 
           12, 15, -13, -72, -56, -28, 15, 17, 
           7, -2, -37, -77, -79, -60, -23, -26, 
           0, -9, 1, -21, -20, -22, -15, -60, 
           -25, 16, -27, -67, -81, -58, -40, -62, 
           33, 26, 42, 11, 11, 40, 35, -2, 
           37, 24, 25, 36, 16, 8, -12, -31, 
           -11, 70, 55, 31, -37, -16, 22, 22]

wpiece_values = {
        chess.PAWN: WPAWN_MG,
        chess.KNIGHT: WKNIGHT_MG,
        chess.BISHOP: WBISHOP_MG,
        chess.ROOK: WROOK_MG,
        chess.QUEEN: WQUEEN_MG,
        chess.KING: WKING_MG
    }
    
bpiece_values = {
        chess.PAWN: BPAWN_MG,
        chess.KNIGHT: BKNIGHT_MG,
        chess.BISHOP: BBISHOP_MG,
        chess.ROOK: BROOK_MG,
        chess.QUEEN: BQUEEN_MG,
        chess.KING: BKING_MG
    }

def score(board: chess.Board):
    value = 0
    if board.is_checkmate():
        value += MATE_SCORE * (-1 if board.turn else 1)
    value += mat_diff(board)
    value += calculate_score(board) * (1 if board.turn else -1)
    return value

def mat_diff(board: chess.Board):
    material_difference = 0
    for piece in board.piece_map():
        material_difference += MATERIAL_POINT[board.piece_type_at(piece)] * (1 if board.piece_at(piece).color else -1)
    return material_difference

def mobility(board: chess.Board):
    return len(list(board.legal_moves))

def calculate_score(board: chess.Board):
    score = 0
    for square, piece in board.piece_map().items():
        piece_type = piece.piece_type
        color = piece.color
        if color == chess.WHITE:
            score += wpiece_values[piece_type][square]
        else:
            score -= bpiece_values[piece_type][square]
            # score1 += wpiece_values[piece_type][square]
            # print(wpiece_values[piece_type][square], piece_type)
    return score

# board = chess.Board("r4rk1/pp1qppbp/2np1np1/8/4P3/2NBBN2/PPP1QPPP/R4RK1 w - - 0 1")
# print(calculate_score(board))
