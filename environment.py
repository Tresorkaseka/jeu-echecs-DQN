import chess
import numpy as np

class ChessEnvironment:
    def __init__(self):
        self.board = chess.Board()

    def reset(self):
        self.board.reset()
        return self.board

    def step(self, move):
        if isinstance(move, chess.Move):  # Vérifier si move est un objet Move
          move = self.board.san(move)   # Convertir en SAN

        self.board.push_san(move)  # Maintenant, move est bien une chaîne
        reward = self._calculate_reward()
        done = self.board.is_game_over()
        return self.board, reward, done


    def _calculate_reward(self):
        if self.board.is_checkmate():
            return 1 if self.board.turn == chess.BLACK else -1
        return 0

    def get_state_size(self):
        return 64  # Taille de la représentation de l'état

    def get_action_size(self):
        return len(list(self.board.legal_moves))  # Nombre de mouvements légaux actuels

    def get_state_representation(self):
        state = np.zeros((8, 8))
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                state[chess.square_rank(square)][chess.square_file(square)] = piece.piece_type
        return state.flatten()

    def agent_action_to_move(self, action):
        legal_moves = list(self.board.legal_moves)
        if action >= len(legal_moves):
            # Si l'action est invalide, choisir un mouvement aléatoire
            return np.random.choice(legal_moves)
        return legal_moves[action]