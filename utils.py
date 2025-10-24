import numpy as np
import chess
import pygame

def load_pieces():
    """
    Charge les images des pièces d'échecs.
    :return: Un dictionnaire contenant les images des pièces.
    """
    pieces = {}
    for piece in chess.PIECE_TYPES:
        for color in [chess.WHITE, chess.BLACK]:
            piece_name = chess.piece_name(piece).lower()
            color_name = "white" if color == chess.WHITE else "black"
            image_path = f"images/{color_name}_{piece_name}.png"
            pieces[(piece, color)] = pygame.image.load(image_path)
    return pieces

def get_state_representation(board):
    """
    Convertit le plateau d'échecs en une représentation numérique.
    :param board: Un objet chess.Board.
    :return: Un tableau numpy représentant l'état du plateau.
    """
    state = np.zeros((8, 8))
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            state[chess.square_rank(square)][chess.square_file(square)] = piece.piece_type
    return state.flatten()

def draw_board(screen, board, pieces, selected_square=None):
    """
    Dessine le plateau d'échecs sur l'écran Pygame.
    :param screen: La surface Pygame.
    :param board: Un objet chess.Board.
    :param pieces: Un dictionnaire contenant les images des pièces.
    :param selected_square: La case sélectionnée (optionnelle).
    """
    for row in range(8):
        for col in range(8):
            color = (255, 255, 255) if (row + col) % 2 == 0 else (0, 0, 0)
            pygame.draw.rect(screen, color, (col * 75, row * 75, 75, 75))

            square = chess.square(col, 7 - row)
            piece = board.piece_at(square)
            if piece:
                screen.blit(pieces[(piece.piece_type, piece.color)], (col * 75, row * 75))

    if selected_square is not None:
        col = chess.square_file(selected_square)
        row = 7 - chess.square_rank(selected_square)
        highlight = pygame.Surface((75, 75), pygame.SRCALPHA)
        highlight.fill((255, 255, 0, 128))
        screen.blit(highlight, (col * 75, row * 75))

def get_square_from_mouse(pos):
    """
    Convertit les coordonnées de la souris en une case d'échecs.
    :param pos: Les coordonnées (x, y) de la souris.
    :return: La case d'échecs correspondante.
    """
    x, y = pos
    col = x // 75
    row = 7 - (y // 75)
    return chess.square(col, row)
	
