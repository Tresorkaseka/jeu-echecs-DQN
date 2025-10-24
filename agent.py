import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = []
        self.gamma = 0.95  # Facteur de discount
        self.epsilon = 1.0  # Taux d'exploration
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential()
        model.add(Dense(128, input_dim=self.state_size, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(optimizer='adam', loss='mse')
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            # Choisir une action aléatoire parmi les mouvements légaux
            return np.random.choice(range(self.action_size))
        state = np.array(state)  # Convertir en numpy array
        state = state.reshape(1, -1)  # S'assurer que la forme correspond bien à (1, 64)
        q_values = self.model.predict(state)

        return np.argmax(q_values[0])

    def replay(self, batch_size):
        minibatch = np.random.choice(len(self.memory), batch_size, replace=False)
        for index in minibatch:
            state, action, reward, next_state, done = self.memory[index]
            target = reward
            if not done:
                next_state = next_state.reshape(1, -1)  # Assurer une entrée correcte pour le modèle
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])

            state = np.array(state)  # Convertir en numpy array si ce n'est pas déjà fait
            state = state.reshape(1, -1)  # Ajouter une dimension pour correspondre à l'entrée du modèle
            target_f = self.model.predict(state)

            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay