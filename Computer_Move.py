import chess
import chess.polyglot
import timeit
import random

from heuristic import *
from TranspositionTable import *

#KILLER MOVE & HISTORY HEURISTIC
killer_move = [[0, 0] for i in range(10)] # killer_move[0/1][ply]
move = []

#MVV-LVA TABLE
MVV_LVA = [
    [0, 0 , 0 , 0 , 0 , 0 , 0 ],    # victim None, attacker None, P, N, B, R, Q, K
    [0, 15, 14, 13, 12, 11, 10],    # victim P, attacker None, P, N, B, R, Q, K
    [0, 25, 24, 23, 22, 21, 20],    # victim N, attacker None, P, N, B, R, Q, K
    [0, 35, 34, 33, 32, 31, 30],    # victim B, attacker None, P, N, B, R, Q, K
    [0, 45, 44, 43, 42, 41, 40],    # victim R, attacker None, P, N, B, R, Q, K
    [0, 55, 54, 53, 52, 51, 50],    # victim Q, attacker None, P, N, B, R, Q, K
    [0, 0 , 0 , 0 , 0 , 0 , 0 ],    # victim K, attacker None, P, N, B, R, Q, K
]

def mvv_lva_ordering(board: chess.Board, move: chess.Move, depth):
    move_score = 0
    if board.is_capture(move):
        move_score += 100
        to_square = move.to_square
        from_square = move.from_square   

        if board.is_en_passant(move):
            victim = 1
        else:
            victim = board.piece_at(to_square).piece_type

        attacker = board.piece_at(from_square).piece_type
        move_score += MVV_LVA[victim][attacker]

    else:
        if move == killer_move[depth][0]:
            move_score += 90
        elif move == killer_move[depth][1]:
            move_score += 80

    return move_score
    
#Transposition Table Consts
EXACT = 0
LOWER = 1
UPPER = 2

zobrist_keys = {
    piece: {color: {square: random.getrandbits(64) for square in range(64)} for color in range(2)}
    for piece in range(1, 7)
}
initial_zobrist_key = random.getrandbits(64)
current_key = random.getrandbits(64)
 
def update_key(board: chess.Board, move: chess.Move, cur_key):
    from_square, to_square = move.from_square, move.to_square
    from_piece = board.piece_at(from_square)
    to_piece = board.piece_at(to_square)

    if from_piece is not None:
        pieceF = from_piece.piece_type
        colorF = from_piece.color
        new_key = cur_key ^ zobrist_keys[pieceF][colorF][from_square] ^ zobrist_keys[pieceF][colorF][to_square]
        if to_piece is not None:
            pieceT = to_piece.piece_type
            colorT = to_piece.color
            new_key ^= zobrist_keys[pieceT][colorT][to_square]
    
    else:
        new_key = cur_key
    
    return new_key

transposition_table = TranspositionTable()

def next_move(board: chess.Board):
    legal_moves = list(board.legal_moves)
    return legal_moves

def negamax(board: chess.Board, depth, alpha, beta, turn, do_null, key):
    tt_flag = LOWER

    cur_entry = transposition_table.lookup(key)
    if cur_entry is not None and cur_entry.depth >= depth:
        if cur_entry.flag == EXACT:
            return cur_entry.score
        elif cur_entry.flag == LOWER:
            return max(alpha, cur_entry.score)
        elif cur_entry.flag == UPPER and cur_entry.score >= beta:
            return min(beta, cur_entry.score)
        
        if alpha >= beta:
            return cur_entry.score
        
    if depth == 0 or board.outcome() != None:
        return turn * score(board)
    
    if board.is_check():
        depth += 1

    if do_null and not board.is_check() and depth >= 3:
        new_key = update_key(board, chess.Move.null(), key)
        board.push(chess.Move.null())
        null_score = -negamax(board, depth - 3, -beta, -beta + 1, -turn, False, new_key)
        board.pop()
        if null_score >= beta:
            return beta

    max_value = -1000000
    best_move =  None

    n = next_move(board)
    n.sort(key = lambda move: mvv_lva_ordering(board, move, depth), reverse = True)

    for move in n:
        new_key = update_key(board, move, key)

        board.push(move)
        value = -negamax(board, depth - 1, -beta, -alpha, -turn, True, new_key)

        board.pop()
        if value > max_value:
            max_value = value
            best_move = move
            if value > alpha:
                alpha = value
                tt_flag = EXACT
                if value >= beta:
                    if not board.is_capture(move):
                        killer_move[depth][1] = killer_move[depth][0]
                        killer_move[depth][0] = move

                    new_entry = Entry(new_key, depth, max_value, UPPER, best_move)
                    transposition_table.store(new_entry)
                    return max_value

        if alpha >= beta:
            break

    new_entry = Entry(key, depth, max_value, tt_flag, best_move)
    transposition_table.store(new_entry)

    return max_value

def get_best_move(board: chess.Board, depth):
    start = timeit.default_timer()
    # Looking for opening move
    best_move = None
    with chess.polyglot.open_reader("data/opening_book.bin") as reader:
        root = list(reader.find_all(board))
        print(root)
        if len(root) != 0: 
            op_move = root[0]
            best_move = op_move.move
            return best_move, "opening"
        
    # Not in opening theory
    legal_moves = list(board.legal_moves)
    n = legal_moves
    n.sort(key = lambda move: mvv_lva_ordering(board, move, depth), reverse = True)
    best_eval = -1000000
    alpha = -1000000
    beta = 1000000
    global current_key
    for move in n:   
        new_key = update_key(board, move, current_key)
        board.push(move)
        print("move: ", move)
        eval = -negamax(board, depth - 1, -beta, -alpha, 1 if board.turn else -1, True, new_key)
        print("eval: ", eval, "\n")
        if(eval > best_eval):
            best_eval = eval
            best_move = move
            current_key = new_key
        board.pop()
        alpha = max(alpha, best_eval)
    end = timeit.default_timer()
    print("time: ", end - start)
    return best_move, best_eval

# board = chess.Board()

# Puzzle 1: 2-move checkmate (Rook Sac)
# board = chess.Board("6k1/pp4p1/2p5/2bp4/8/P5Pb/1P3rrP/2BRRN1K b - - 0 1")
"""
With MVV-LVA & depth = 8
(Move.from_uci('g2h2'), 1000000)
time:  10.824232299928553
"""

# Puzzle 2: 3-move checkmate
# board = chess.Board("3r4/pR2N3/2pkb3/5p2/8/2B5/qP3PPP/4R1K1 w - - 1 0")
"""
With MVV-LVA & depth = 6
(Move.from_uci('c3e5'), 999999)
time:  39.19258919998538

With MVV-LVA & depth = 7
(Move.from_uci('c3e5'), 999999)
time:  535.30205259996 ????
"""

# start = timeit.default_timer()
# print(get_best_move(board, 6))
# end = timeit.default_timer()
# print("time: ", end - start)