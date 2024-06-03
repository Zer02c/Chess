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
bg_color = white

# Figuren laden
piece_images = {}
pieces = ['King', 'Queen', 'Rook', 'Bishop', 'Knight', 'pawn']
for piece in pieces:
    piece_images[f'w{piece}'] = pygame.transform.scale(pygame.image.load(f'icons/White/{piece}.png'),
                                                       (square_size, square_size))
    piece_images[f'b{piece}'] = pygame.transform.scale(pygame.image.load(f'icons/Black/{piece}.png'),
                                                       (square_size, square_size))

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

# Musik laden und abspielen
pygame.mixer.music.load('music/Checkmate.mp3')  # Pfad zur Musikdatei
pygame.mixer.music.play(-1)  # Musik in Schleife abspielen
music_volume = 0.5
pygame.mixer.music.set_volume(music_volume)

# Menü-Status
menu_active = True
brightness_menu_active = False
sound_menu_active = False


# Zeichnen des Startmenüs
def draw_start_menu():
    screen.fill(bg_color)
    font = pygame.font.Font(None, 74)
    text_start = font.render('Spiel starten', True, (0, 0, 0))
    text_brightness = font.render('Helligkeit', True, (0, 0, 0))
    text_sound = font.render('Sound', True, (0, 0, 0))
    text_start_rect = text_start.get_rect(center=(screen_size // 2, screen_size // 3))
    text_brightness_rect = text_brightness.get_rect(center=(screen_size // 2, screen_size // 2))
    text_sound_rect = text_sound.get_rect(center=(screen_size // 2, 2 * screen_size // 3))
    screen.blit(text_start, text_start_rect)
    screen.blit(text_brightness, text_brightness_rect)
    screen.blit(text_sound, text_sound_rect)
    pygame.display.flip()


# Zeichnen des Helligkeitsmenüs
def draw_brightness_menu():
    screen.fill(bg_color)
    font = pygame.font.Font(None, 74)
    text = font.render('Helligkeit anpassen', True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen_size // 2, screen_size // 4))
    screen.blit(text, text_rect)

    # Schieberegler zeichnen
    slider_rect = pygame.Rect(screen_size // 4, screen_size // 2, screen_size // 2, 50)
    pygame.draw.rect(screen, (200, 200, 200), slider_rect)
    handle_rect = pygame.Rect(slider_rect.x + (slider_rect.width * brightness) - 15, slider_rect.y - 10, 30, 70)
    pygame.draw.rect(screen, (100, 100, 100), handle_rect)

    pygame.display.flip()


# Zeichnen des Soundmenüs
def draw_sound_menu():
    screen.fill(bg_color)
    font = pygame.font.Font(None, 74)
    text = font.render('Lautstärke anpassen', True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen_size // 2, screen_size // 4))
    screen.blit(text, text_rect)

    # Schieberegler zeichnen
    slider_rect = pygame.Rect(screen_size // 4, screen_size // 2, screen_size // 2, 50)
    pygame.draw.rect(screen, (200, 200, 200), slider_rect)
    handle_rect = pygame.Rect(slider_rect.x + (slider_rect.width * music_volume) - 15, slider_rect.y - 10, 30, 70)
    pygame.draw.rect(screen, (100, 100, 100), handle_rect)

    pygame.display.flip()


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
                screen.blit(piece_images[piece],
                            pygame.Rect(col * square_size, row * square_size, square_size, square_size))


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
def is_valid_move(board, start_pos, end_pos, en_passant_target):
    piece = board[start_pos[1]][start_pos[0]]
    target = board[end_pos[1]][end_pos[0]]

    if (piece.startswith('w') and target.startswith('w')) or (piece.startswith('b') and target.startswith('b')):
        return False

    if piece == 'wpawn':  # Weißer Bauer
        if (start_pos[0] == end_pos[0] and start_pos[1] - end_pos[1] == 1 and target == '--') or \
                (start_pos[0] == end_pos[0] and start_pos[1] == 6 and start_pos[1] - end_pos[
                    1] == 2 and target == '--' and board[start_pos[1] - 1][start_pos[0]] == '--') or \
                (abs(start_pos[0] - end_pos[0]) == 1 and start_pos[1] - end_pos[1] == 1 and (
                        target.startswith('b') or (end_pos == en_passant_target))):
            return True
    if piece == 'bpawn':  # Schwarzer Bauer
        if (start_pos[0] == end_pos[0] and end_pos[1] - start_pos[1] == 1 and target == '--') or \
                (start_pos[0] == end_pos[0] and start_pos[1] == 1 and end_pos[1] - start_pos[
                    1] == 2 and target == '--' and board[start_pos[1] + 1][start_pos[0]] == '--') or \
                (abs(start_pos[0] - end_pos[0]) == 1 and end_pos[1] - start_pos[1] == 1 and (
                        target.startswith('w') or (end_pos == en_passant_target))):
            return True
    if piece == 'wRook' or piece == 'bRook':  # Turm
        return (start_pos[0] == end_pos[0] or start_pos[1] == end_pos[1]) and path_is_clear(board, start_pos, end_pos)
    if piece == 'wBishop' or piece == 'bBishop':  # Läufer
        return abs(start_pos[0] - end_pos[0]) == abs(start_pos[1] - end_pos[1]) and path_is_clear(board, start_pos,
                                                                                                  end_pos)
    if piece == 'wQueen' or piece == 'bQueen':  # Dame
        return (abs(start_pos[0] - end_pos[0]) == abs(start_pos[1] - end_pos[1]) or \
                start_pos[0] == end_pos[0] or start_pos[1] == end_pos[1]) and path_is_clear(board, start_pos, end_pos)
    if piece == 'wKnight' or piece == 'bKnight':  # Springer
        return abs(start_pos[0] - end_pos[0]) * abs(start_pos[1] - end_pos[1]) == 2
    if piece == 'wKing' or piece == 'bKing':  # König
        return max(abs(start_pos[0] - end_pos[0]), abs(start_pos[1] - end_pos[1])) == 1

    return False


# Mögliche Züge für eine Figur berechnen
def get_valid_moves(board, start_pos, en_passant_target):
    valid_moves = []
    for row in range(8):
        for col in range(8):
            if is_valid_move(board, start_pos, (col, row), en_passant_target):
                valid_moves.append((col, row))
    return valid_moves


# Figur bewegen
def move_piece(board, start_pos, end_pos, en_passant_target):
    if is_valid_move(board, start_pos, end_pos, en_passant_target):
        piece = board[start_pos[1]][start_pos[0]]
        board[start_pos[1]][start_pos[0]] = '--'
        board[end_pos[1]][end_pos[0]] = piece
        # En Passant-Fang
        if piece == 'wpawn' and start_pos[1] - end_pos[1] == 1 and end_pos == en_passant_target:
            board[end_pos[1] + 1][end_pos[0]] = '--'
        elif piece == 'bpawn' and end_pos[1] - start_pos[1] == 1 and end_pos == en_passant_target:
            board[end_pos[1] - 1][end_pos[0]] = '--'
        return True
    return False


selected_piece = None
valid_moves = []
en_passant_target = None


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
brightness = 0.5

while True:
    if menu_active:
        draw_start_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Linke Maustaste
                    mouse_pos = pygame.mouse.get_pos()
                    if screen_size // 4 <= mouse_pos[0] <= 3 * screen_size // 4 and screen_size // 3 <= mouse_pos[
                        1] <= screen_size // 2:
                        menu_active = False
                        pygame.mixer.music.stop()  # Musik stoppen
                    elif screen_size // 4 <= mouse_pos[0] <= 3 * screen_size // 4 and screen_size // 2 <= mouse_pos[
                        1] <= 2 * screen_size // 3:
                        brightness_menu_active = True
                        sound_menu_active = False
                    elif screen_size // 4 <= mouse_pos[0] <= 3 * screen_size // 4 and 2 * screen_size // 3 <= mouse_pos[
                        1] <= 5 * screen_size // 6:
                        sound_menu_active = True
                        brightness_menu_active = False
    elif brightness_menu_active:
        draw_brightness_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Linke Maustaste
                    mouse_pos = pygame.mouse.get_pos()
                    slider_rect = pygame.Rect(screen_size // 4, screen_size // 2, screen_size // 2, 50)
                    if slider_rect.collidepoint(mouse_pos):
                        brightness = (mouse_pos[0] - slider_rect.x) / slider_rect.width
                        bg_color = (int(255 * brightness), int(255 * brightness), int(255 * brightness))
                        brightness_menu_active = False
    elif sound_menu_active:
        draw_sound_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Linke Maustaste
                    mouse_pos = pygame.mouse.get_pos()
                    slider_rect = pygame.Rect(screen_size // 4, screen_size // 2, screen_size // 2, 50)
                    if slider_rect.collidepoint(mouse_pos):
                        music_volume = (mouse_pos[0] - slider_rect.x) / slider_rect.width
                        pygame.mixer.music.set_volume(music_volume)
                        sound_menu_active = False
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = get_square_under_mouse()
                if selected_piece:
                    if (x, y) in valid_moves:
                        if move_piece(board, selected_piece, (x, y), en_passant_target):
                            # En Passant Ziel aktualisieren
                            piece = board[y][x]
                            if piece == 'wpawn' and selected_piece[1] == 6 and y == 4:
                                en_passant_target = (x, y + 1)
                            elif piece == 'bpawn' and selected_piece[1] == 1 and y == 3:
                                en_passant_target = (x, y - 1)
                            else:
                                en_passant_target = None
                            # Spielerwechsel nach gültigem Zug
                            current_player = 'white' if current_player == 'black' else 'black'
                        selected_piece = None
                        valid_moves = []
                elif board[y][x].startswith(
                        current_player[0]):  # Überprüfen, ob die ausgewählte Figur dem aktuellen Spieler gehört
                    selected_piece = (x, y)
                    valid_moves = get_valid_moves(board, selected_piece, en_passant_target)
            elif event.type == clock_tick:
                clock.update()

        draw_board()
        clock.draw()

        # Mögliche Züge hervorheben
        for move in valid_moves:
            pygame.draw.rect(screen, blue,
                             pygame.Rect(move[0] * square_size, move[1] * square_size, square_size, square_size), 5)

        draw_pieces(board)
        pygame.display.flip()
