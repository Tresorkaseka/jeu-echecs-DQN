import pygame
import chess
from environment import ChessEnvironment
from agent import DQNAgent
from utils import load_pieces, draw_board, get_square_from_mouse

# Initialisation de Pygame
pygame.init()

# Constantes
WIDTH, HEIGHT = 600, 600  # Taille de la fenêtre
SQUARE_SIZE = WIDTH // 8  # Taille d'une case
FPS = 30  # Images par seconde

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
HIGHLIGHT_COLOR = (255, 255, 0, 128)  # Couleur de surbrillance (jaune)

# Fonction principale
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jeu d'échecs avec Pygame")
    clock = pygame.time.Clock()

    # Initialisation de l'environnement et de l'agent
    env = ChessEnvironment()
    state_size = env.get_state_size()
    action_size = env.get_action_size()
    agent = DQNAgent(state_size, action_size)

    # Charger les images des pièces
    pieces = load_pieces()

    selected_square = None  # Case sélectionnée par l'utilisateur
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                square = get_square_from_mouse(pos)

                if selected_square is None:
                    # Sélectionner une pièce
                    if env.board.piece_at(square):
                        selected_square = square
                else:
                    # Déplacer la pièce
                    move = chess.Move(selected_square, square)
                    if move in env.board.legal_moves:
                        env.board.push(move)
                        # Tour de l'agent
                        state = env.get_state_representation()
                        action = agent.act(state)
                        move = env.agent_action_to_move(action)
                        env.board.push(move)
                    selected_square = None

        # Dessiner le plateau
        screen.fill(GRAY)
        draw_board(screen, env.board, pieces, selected_square)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()