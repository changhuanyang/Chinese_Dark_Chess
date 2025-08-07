import pygame
from pygame.locals import *
from chinese_dark_chess import *

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1000

# Board dimensions (Chinese Dark Chess is 8x4)
SQUARE_SIZE = 100 # Size of each square

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (0, 255, 200)
DARK_GREEN = (25, 95, 25)


# Calculate board offset to center it
BOARD_WIDTH = BOARD_COLS * SQUARE_SIZE
BOARD_HEIGHT = BOARD_ROWS * SQUARE_SIZE
OFFSET_X = (SCREEN_WIDTH - BOARD_WIDTH) // 2
OFFSET_Y = (SCREEN_HEIGHT - BOARD_HEIGHT) // 2

# 
current_player_index = 1
selected_piece_pos = None # To store the position of the currently selected piece
current_status_text = None

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def draw_board(board_state):
    """Draws the Chinese Dark Chess board."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            x = col * SQUARE_SIZE + OFFSET_X
            y = row * SQUARE_SIZE + OFFSET_Y
            pygame.draw.rect(screen, BLACK, (x, y, SQUARE_SIZE, SQUARE_SIZE), 1) # Draw grid lines

            piece = board_state[row][col]
            if piece == EMPTY_SPACE:
                pass
            elif piece == FACE_DOWN_PIECE:
                pygame.draw.circle(screen, DARK_GREEN, (x+SQUARE_SIZE/2, y+SQUARE_SIZE/2),SQUARE_SIZE/2 -10) # Draw a face-down piece
                pygame.draw.circle(screen, BLACK, (x+SQUARE_SIZE/2, y+SQUARE_SIZE/2),SQUARE_SIZE/2 -10 , 2 ) 
            else: 
                text_color = RED
                if 2 <= piece <= 8: 
                    text_color = BLACK
                # For face-down pieces, just show '?'
                display_text = INDEX_TO_CHINESE_MAP[piece]
                font = pygame.font.Font("SourceHanSansTC-VF.ttf", 36)
                text_surface = font.render(display_text, True, text_color)
                text_rect = text_surface.get_rect(center=(x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2))
                screen.blit(text_surface, text_rect)




def handle_click(game, mouse_x, mouse_y):
    """Handles a mouse click on the board."""
    global selected_piece_pos, current_player_index, current_status_text
    cur_col = (mouse_x - OFFSET_X) // SQUARE_SIZE
    cur_row = (mouse_y - OFFSET_Y) // SQUARE_SIZE
    # Check if click is within board boundaries
    if not (0 <= cur_row < BOARD_ROWS and 0 <= cur_col < BOARD_COLS):
        return
    current_board = game.get_board_state()
    clicked_piece = current_board[cur_row][cur_col]
    
    if not selected_piece_pos:  # No piece selected yet, this click is for selecting a piece
        if clicked_piece != EMPTY_SPACE: 
            selected_piece_pos = (cur_row, cur_col)
    else: # A piece has been selected:
        prev_row, prev_col = selected_piece_pos
        # Check if clicking on the same piece: flip
        if (cur_row, cur_col) == (prev_row, prev_col):
            if clicked_piece == FACE_DOWN_PIECE:
                if not game.flip(cur_row, cur_col):
                    raise RuntimeError("Failed to flip")
                selected_piece_pos = None
                if not game.change_player():
                    raise RuntimeError("Failed to Change Player")
        else: #(cur_row, cur_col) != (prev_row, prev_col):
            if game.move(prev_row, prev_col, cur_row, cur_col):
                if not game.change_player():
                    raise RuntimeError("Failed to Change Player")
                selected_piece_pos = None
            else:
                current_status_text
                selected_piece_pos = (cur_row, cur_col)
    if game.current_player_color == RED_PLAYER:
        player_color = "RED" 
    elif game.current_player_color == BLACK_PLAYER:
        player_color = "BLACK"
    else:
        player_color = "UNKNOWN"
    current_status_text = f"Current Turn Player: {game.current_player} with color: {player_color}"


end_game = False
if __name__ == "__main__" :
    # Initialize Pygame
    pygame.init()

    # Screen dimensions
    pygame.display.set_caption("Chinese Dark Chess")

    running = True
    game = ChineseDarkGame()
    current_status_text = "Game start!"
    screen.fill(WHITE) # Clear screen
    draw_board(game.get_board_state())
    pygame.display.flip() # Update the full display Surface to the screen
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if end_game:
                    screen.fill(WHITE) # Clear screen
                    game.restart()
                    draw_board(game.get_board_state())
                    pygame.display.flip()
                handle_click(game, event.pos[0], event.pos[1])
                
                who_win = game.who_win()
                if who_win == DRAW:
                    current_status_text = "DRAW! Click to restart"
                    end_game= True
                elif who_win == BLACK_WIN:
                    current_status_text = "BLACK WIN! Click to restart"
                    end_game = True
                elif who_win == RED_WIN:
                    current_status_text = "RED WIN! Click to restart"
                    end_game = True
                
                # Drawing
                screen.fill(WHITE) # Clear screen
                draw_board(game.get_board_state())
                font = pygame.font.Font(None, 28)
                text_color = RED if game.current_player_color == RED_PLAYER else BLACK
                turn_text = font.render(f"{current_status_text}", True, text_color)
                screen.blit(turn_text, (10, 10))
                if selected_piece_pos:
                    row, col = selected_piece_pos
                    x = col * SQUARE_SIZE + OFFSET_X
                    y = row * SQUARE_SIZE + OFFSET_Y
                    pygame.draw.rect(screen, (255, 255, 0), (x, y, SQUARE_SIZE, SQUARE_SIZE), 3) # Yellow border
                pygame.display.flip() # Update the full display Surface to the screen

    
    pygame.quit()