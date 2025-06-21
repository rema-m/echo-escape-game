#!/usr/bin/env python3
"""
Echo Escape - Game Launcher
Simple launcher script for the Echo Escape game.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from echo_escape_main import Game
    
    if __name__ == "__main__":
        print("Starting Echo Escape...")
        print("Make sure you have pygame and numpy installed!")
        print("pip install pygame numpy")
        print("-" * 50)
        
        game = Game()
        game.run()
        
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please install required dependencies:")
    print("pip install pygame numpy")
    sys.exit(1)
except Exception as e:
    print(f"Error starting game: {e}")
    sys.exit(1)
