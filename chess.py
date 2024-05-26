import pygame
import sys

from chess_clock import ChessClock

# Pygame initialisieren
pygame.init()

# Bildschirmgröße festlegen
screen_size = 800
square_size = screen_size // 8
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption('Schach')

# Schriftart und Farbe für die Uhr
clock_font = pygame.font.Font(None, 36)
clock_color = (255, 255, 255)
clock_pos = (10, 10)

# Schach Uhr erstellen
clock = ChessClock(screen, clock_font, clock_color, clock_pos)

# Farben definieren
white = (255, 255, 255)
gray = (128, 128, 128)
blue = (0, 0, 255, 128)

# Figuren laden
piece_images = {}
pieces = ['King', 'Queen', 'Rook', 'Bishop', 'Knight', 'pawn']
for piece in pieces:
    piece_images[f'w{piece}'] = pygame.transform.scale(pygame.image.load(f'icons/White/{piece}.png'), (square_size, square_size))
    piece_images[f'b{piece}'] = pygame.transform.scale(pygame.image.load(f'icons/Black/{piece}.png'), (square_size, square_size))

# Beispielbrett
board = [
    ['bRook', 'bKnight', 'bBishop', 'bQueen', 'bKing', 'bBishop', 'bKnight', 'bRook'],
    ['bpawn', 'bpawn', 'bpawn', 'bpawn', 'bpawn', 'bpawn', 'bpawn', 'bpawn'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['wpawn', 'wpawn', 'wpawn', 'wpawn', 'wpawn', 'wpawn', 'wpawn', 'wpawn'],
    ['wRook', 'wKnight', 'wBishop', 'wQueen', 'wKing', 'wBishop', 'wKnight', 'wRook']
]

# Zeichnen des Schachbretts
def draw_board():
    colors = [white, gray]
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(col * square_size, row * square_size, square_size, square_size))

# Zeichnen der Figuren
def draw_pieces(board):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '--':
                screen.blit(piece_images[piece], pygame.Rect(col * square_size, row * square_size, square_size, square_size))

# Überprüfen, ob der Pfad frei ist
def path_is_clear(board, start_pos, end_pos):
    direction_x = end_pos[0] - start_pos[0]
    direction_y = end_pos[1] - start_pos[1]

    step_x = (direction_x > 0) - (direction_x < 0)
    step_y = (direction_y > 0) - (direction_y < 0)

    x, y = start_pos
    x += step_x
    y += step_y

    while (x, y) != end_pos:
        if board[y][x] != '--':
            return False
        x += step_x
        y += step_y

    return True

# Überprüfen, ob ein Zug gültig ist
def is_valid_move(board, start_pos, end_pos):
    piece = board[start_pos[1]][start_pos[0]]
    target = board[end_pos[1]][end_pos[0]]
    
    if (piece.startswith('w') and target.startswith('w')) or (piece.startswith('b') and target.startswith('b')):
        return False

    if piece == 'wpawn':  # Weißer Bauer
        return (start_pos[0] == end_pos[0] and start_pos[1] - end_pos[1] == 1 and target == '--') or \
               (start_pos[0] == end_pos[0] and start_pos[1] == 6 and start_pos[1] - end_pos[1] == 2 and target == '--' and board[start_pos[1] - 1][start_pos[0]] == '--') or \
               (abs(start_pos[0] - end_pos[0]) == 1 and start_pos[1] - end_pos[1] == 1 and target.startswith('b'))
    if piece == 'bpawn':  # Schwarzer Bauer
        return (start_pos[0] == end_pos[0] and end_pos[1] - start_pos[1] == 1 and target == '--') or \
               (start_pos[0] == end_pos[0] and start_pos[1] == 1 and end_pos[1] - start_pos[1] == 2 and target == '--' and board[start_pos[1] + 1][start_pos[0]] == '--') or \
               (abs(start_pos[0] - end_pos[0]) == 1 and end_pos[1] - start_pos[1] == 1 and target.startswith('w'))
    if piece == 'wRook' or piece == 'bRook':  # Turm
        return (start_pos[0] == end_pos[0] or start_pos[1] == end_pos[1]) and path_is_clear(board, start_pos, end_pos)
    if piece == 'wBishop' or piece == 'bBishop':  # Läufer
        return abs(start_pos[0] - end_pos[0]) == abs(start_pos[1] - end_pos[1]) and path_is_clear(board, start_pos, end_pos)
    if piece == 'wQueen' or piece == 'bQueen':  # Dame
        return (abs(start_pos[0] - end_pos[0]) == abs(start_pos[1] - end_pos[1]) or \
               start_pos[0] == end_pos[0] or start_pos[1] == end_pos[1]) and path_is_clear(board, start_pos, end_pos)
    if piece == 'wKnight' or piece == 'bKnight':  # Springer
        return abs(start_pos[0] - end_pos[0]) * abs(start_pos[1] - end_pos[1]) == 2
    if piece == 'wKing' or piece == 'bKing':  # König
        return max(abs(start_pos[0] - end_pos[0]), abs(start_pos[1] - end_pos[1])) == 1

    return False

# Mögliche Züge für eine Figur berechnen
def get_valid_moves(board, start_pos):
    valid_moves = []
    for row in range(8):
        for col in range(8):
            if is_valid_move(board, start_pos, (col, row)):
                valid_moves.append((col, row))
    return valid_moves

# Figur bewegen
def move_piece(board, start_pos, end_pos):
    if is_valid_move(board, start_pos, end_pos):
        piece = board[start_pos[1]][start_pos[0]]
        board[start_pos[1]][start_pos[0]] = '--'
        board[end_pos[1]][end_pos[0]] = piece

selected_piece = None
valid_moves = []

def get_square_under_mouse():
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    x, y = [int(v // square_size) for v in mouse_pos]
    if 0 <= x < 8 and 0 <= y < 8:
        return x, y
    return None, None

# Hauptspiel-Schleife
clock_tick = pygame.USEREVENT + 1
pygame.time.set_timer(clock_tick, 1000)
current_player = 'white'  # Startspieler
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = get_square_under_mouse()
            if selected_piece:
                if (x, y) in valid_moves:
                    move_piece(board, selected_piece, (x, y))
                    # Spielerwechsel nach gültigem Zug
                    current_player = 'white' if current_player == 'black' else 'black'
                selected_piece = None
                valid_moves = []
            elif board[y][x].startswith(current_player[0]):  # Überprüfen, ob die ausgewählte Figur dem aktuellen Spieler gehört
                selected_piece = (x, y)
                valid_moves = get_valid_moves(board, selected_piece)
        elif event.type == clock_tick:
            clock.update()
    
    draw_board()
    clock.draw()
    
    # Mögliche Züge hervorheben
    for move in valid_moves:
        pygame.draw.rect(screen, blue, pygame.Rect(move[0] * square_size, move[1] * square_size, square_size, square_size), 5)
    
    draw_pieces(board)
    pygame.display.flip()
    

