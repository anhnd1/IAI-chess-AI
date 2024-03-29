import pygame
import chess

from GUI import board
from Computer_Move import get_best_move
from start_window import start_screen

pygame.init()

window_size = (800, 600)
board_size = (600, 600)
team = [-1, -1]

# start screen
screen = pygame.display.set_mode(window_size)
main_start_screen = start_screen(window_size)
def draw_start_screen(screen):
    screen.fill('white')
    main_start_screen.draw_screen(screen)
    pygame.display.update()

while True:
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                team = main_start_screen.click(mx, my)
    draw_start_screen(screen)
    if team[0] != -1:
        break

main_board = board(board_size[0], board_size[1], team)

def draw(screen):
    screen.fill('white')
    main_board.draw(screen)
    pygame.display.update()

best_move = -1

while main_board.board.is_game_over() == False:
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if main_board.player[main_board.turn]:  
                    main_board.player_click(mx, my, screen)

    if main_board.board.is_game_over():
        break

    if main_board.player[main_board.turn] == 0:
        draw(screen)
        best_move, eval = get_best_move(main_board.board, 12)
        print("\nbest move: ", best_move, " eval: ", eval)
        main_board.move(best_move.uci())
    draw(screen)

# Result handling
print(main_board.board.move_stack)
if main_board.board.is_checkmate():
    if main_board.board.turn == chess.WHITE:
        print("Black wins by checkmate!")
    else:
        print("White wins by checkmate!")
elif main_board.board.is_stalemate():
    print("Stalemate!")
elif main_board.board.is_insufficient_material():
    print("Insufficient material for checkmate.")
elif main_board.board.is_seventyfive_moves():
    print("Draw due to 75-move rule.")
elif main_board.board.is_fivefold_repetition():
    print("Draw due to fivefold repetition.")
else:
    print("Game over for some other reason.")
