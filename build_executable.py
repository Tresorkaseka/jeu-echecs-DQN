#!/usr/bin/env python
# Script pour créer un exécutable de l'application de jeu d'échecs avec IA

import os
import subprocess
import sys

def install_pyinstaller():
    """Installe PyInstaller si ce n'est pas déjà fait."""
    try:
        import PyInstaller
        print("PyInstaller est déjà installé.")
    except ImportError:
        print("Installation de PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller installé avec succès.")

def create_executable():
    """Crée l'exécutable pour le jeu d'échecs avec IA."""
    # Vérifier que les dossiers nécessaires existent
    if not os.path.exists("models") or not os.path.exists("images"):
        print("ERREUR: Les dossiers 'models' et 'images' doivent être présents dans le répertoire courant.")
        return False
    
    # Installer PyInstaller si nécessaire
    install_pyinstaller()
    
    # Commande PyInstaller pour créer l'exécutable
    cmd = [
        "pyinstaller",
        "--onefile",           # Crée un seul fichier exécutable
        "--windowed",          # Application graphique (pas de console)
        "--add-data", "images;images",  # Inclure le dossier images
        "--add-data", "models;models",  # Inclure le dossier models
        "--name", "ChessAI",   # Nom de l'exécutable
        "play.py"              # Fichier principal à convertir
    ]
    
    # Sur macOS et Linux, le séparateur pour --add-data est ":"
    if os.name != 'nt':  # Si ce n'est pas Windows
        cmd[4] = "images:images"
        cmd[6] = "models:models"
    
    print("Création de l'exécutable...")
    print("Commande exécutée : " + " ".join(cmd))
    
    try:
        subprocess.check_call(cmd)
        print("\nExécutable créé avec succès dans le dossier 'dist'!")
        print("L'exécutable se trouve dans : dist/ChessAI.exe (Windows) ou dist/ChessAI (Linux/Mac)")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la création de l'exécutable : {e}")
        return False

if __name__ == "__main__":
    create_executable()