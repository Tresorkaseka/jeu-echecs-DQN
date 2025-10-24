# Jeu d'échecs avec IA

Ce projet est une implémentation d'un jeu d'échecs avec une intelligence artificielle basée sur l'apprentissage par renforcement (Deep Q-Network). Le jeu permet à un joueur humain de s'opposer à une IA qui a été entraînée pour jouer aux échecs.

## Fonctionnalités

- Interface graphique Pygame pour jouer aux échecs
- IA basée sur un réseau de neurones DQN (Deep Q-Network)
- Système d'entraînement pour améliorer l'IA
- Évaluation des performances de l'IA

## Structure du projet

- `main.py` - Version de base du jeu d'échecs avec interface Pygame
- `agent.py` - Implémentation de l'agent DQN
- `environment.py` - Environnement du jeu d'échecs
- `utils.py` - Fonctions utilitaires pour l'affichage et la gestion du plateau
- `train.py` - Script d'entraînement de l'IA
- `play.py` - Version finale du jeu avec l'IA chargée depuis un modèle sauvegardé
- `requirements.txt` - Dépendances du projet
- `models/dqn_model.h5` - Modèle entraîné de l'IA
- `images/` - Images des pièces d'échecs

## Installation

1. Clonez ce dépôt
2. Installez les dépendances : `pip install -r requirements.txt`
3. Lancez le jeu : `python play.py`
