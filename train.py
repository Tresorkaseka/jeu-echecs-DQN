from agent import DQNAgent
from environment import ChessEnvironment
from utils import get_state_representation

def train():
    env = ChessEnvironment()
    state_size = env.get_state_size()
    agent = DQNAgent(state_size, action_size=4672)  # Taille maximale de l'action

    episodes = 500
    for episode in range(episodes):
        state = env.reset()
        state = get_state_representation(state)
        done = False
        while not done:
            # Mettre à jour la taille de l'action en fonction des mouvements légaux actuels
            action_size = env.get_action_size()
            agent.action_size = action_size

            action = agent.act(state)
            move = env.agent_action_to_move(action)
            next_state, reward, done = env.step(move)
            next_state = get_state_representation(next_state)
            agent.remember(state, action, reward, next_state, done)
            state = next_state
        agent.replay(32)  # Entraînement sur un batch de 32 expériences
        print(f"Episode {episode + 1}/{episodes} terminé.")

    # Sauvegarder le modèle après l'entraînement
    agent.model.save("models/dqn_model.h5")
    print("Modèle sauvegardé dans models/dqn_model.h5")

if __name__ == "__main__":
    train()