import pygame
import chess
import chess.svg
import random
from tensorflow.keras.models import load_model
from agent import DQNAgent
from environment import ChessEnvironment
from utils import get_state_representation

# Initialiser Pygame
pygame.init()
WIDTH, HEIGHT = 600, 600
SQUARE_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Échecs IA - Pygame")

# Charger et redimensionner les images des pièces
piece_images = {}
piece_names = {
    'p': 'black_pawn', 'r': 'black_rook', 'n': 'black_knight', 'b': 'black_bishop', 'q': 'black_queen', 'k': 'black_king',
    'P': 'white_pawn', 'R': 'white_rook', 'N': 'white_knight', 'B': 'white_bishop', 'Q': 'white_queen', 'K': 'white_king'
}

for piece, name in piece_names.items():
    image_path = f"images/{name}.png"
    image = pygame.image.load(image_path)
    piece_images[piece] = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))

# Dessiner l’échiquier
def draw_board():
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Placer les pièces sur l’échiquier
def draw_pieces(board):
    for row in range(8):
        for col in range(8):
            square = chess.square(col, 7 - row)
            piece = board.piece_at(square)
            if piece:
                screen.blit(piece_images[piece.symbol()], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def play():
    env = ChessEnvironment()
    state_size = env.get_state_size()
    agent = DQNAgent(state_size, action_size=4672)

    # Charger le modèle sauvegardé
    agent.model = load_model("models/dqn_model.h5", compile=False)
    print("Modèle chargé depuis models/dqn_model.h5")

    board = chess.Board()
    running = True
    selected_square = None

    while running:
        screen.fill(pygame.Color("black"))
        draw_board()
        draw_pieces(board)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Gestion des clics pour le tour du joueur
            if event.type == pygame.MOUSEBUTTONDOWN and board.turn == chess.WHITE:
                x, y = event.pos
                col = x // SQUARE_SIZE
                row = 7 - (y // SQUARE_SIZE)
                clicked_square = chess.square(col, row)

                if selected_square is None:
                    # Sélectionne une pièce blanche
                    if board.piece_at(clicked_square) and board.piece_at(clicked_square).color == chess.WHITE:
                        selected_square = clicked_square
                        print(f"Pièce sélectionnée : {selected_square}")
                    else:
                        print("Sélection invalide.")
                else:
                    # Déplace la pièce sélectionnée
                    move = chess.Move(selected_square, clicked_square)
                    print(f"Tentative de coup : {move}")

                    if move in board.legal_moves:
                        board.push(move)
                        print(f"Joueur joue : {move}")
                        selected_square = None  # Réinitialiser la sélection
                    else:
                        print("Coup invalide.")
                        selected_square = None

        # Tour de l'IA (joue seulement après le joueur)
        if board.turn == chess.BLACK and not board.is_game_over():
            pygame.time.delay(500)  
            state = get_state_representation(board)
            action = agent.act(state)
            ai_move = env.agent_action_to_move(action)

            print(f"L'IA choisit l'action : {action} → Coup traduit : {ai_move}")

            if ai_move in board.legal_moves:
                board.push(ai_move)
                print(f"L'agent joue : {ai_move}")
            else:
                print(f"L'IA a essayé un coup illégal : {ai_move}")
                ai_move = random.choice(list(board.legal_moves))  # Prendre un coup valide au hasard
                board.push(ai_move)
                print(f"L'IA joue finalement : {ai_move}")

    pygame.quit()
import chess
import random
import numpy as np
from tensorflow.keras.models import load_model
from agent import DQNAgent
from environment import ChessEnvironment
from utils import get_state_representation

def evaluate_agent(num_episodes=100):
    env = ChessEnvironment()
    state_size = env.get_state_size()
    agent = DQNAgent(state_size, action_size=4672)

    # Charger le modèle entraîné
    agent.model = load_model("models/dqn_model.h5", compile=False)
    print("Modèle chargé pour l'évaluation.")

    victories = 0
    total_rewards = []
    moves_per_game = []

    for episode in range(num_episodes):
        board = chess.Board()
        total_reward = 0
        num_moves = 0

        while not board.is_game_over():
            state = get_state_representation(board)
            action = agent.act(state)
            ai_move = env.agent_action_to_move(action)

            if ai_move in board.legal_moves:
                board.push(ai_move)
                num_moves += 1
            else:
                # Si l'IA propose un coup illégal, choisir un coup valide au hasard
                ai_move = random.choice(list(board.legal_moves))
                board.push(ai_move)
                num_moves += 1

            # Calculer la récompense (ex: +1 pour victoire, -1 pour défaite)
            if board.is_checkmate():
                reward = 1  # Victoire
            elif board.is_stalemate() or board.is_insufficient_material():
                reward = 0  # Partie nulle
            else:
                reward = -0.01  # Pénalité légère pour éviter les longues parties

            total_reward += reward

        total_rewards.append(total_reward)
        moves_per_game.append(num_moves)

        # Vérifier si l'IA a gagné
        result = board.result()
        if result == "1-0":  # Victoire des Blancs (IA)
            victories += 1

        print(f"Épisode {episode + 1}/{num_episodes} - Résultat: {result} - Coups: {num_moves}")

    # Résumé des performances
    win_rate = (victories / num_episodes) * 100
    avg_reward = np.mean(total_rewards)
    avg_moves = np.mean(moves_per_game)

    print("\n📊 **Évaluation de l'IA après", num_episodes, "parties:**")
    print(f"✅ Taux de victoire : {win_rate:.2f}%")
    print(f"✅ Récompense moyenne : {avg_reward:.2f}")
    print(f"✅ Nombre moyen de coups par partie : {avg_moves:.2f}")

# Lancer l'évaluation
evaluate_agent(100)  # Teste sur 100 parties


if __name__ == "__main__":
    play()
