import pygame
import os

class SoundManager:
    """Manages all game sound effects"""
    
    def __init__(self):
        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        # Dictionary to store sound objects
        self.sounds = {}
        
        # Try to load sound files (gracefully handle missing files)
        self._load_sound('paddle_hit', 'sounds/paddle_hit.wav')
        self._load_sound('wall_bounce', 'sounds/wall_bounce.wav')
        self._load_sound('score', 'sounds/score.wav')
    
    def _load_sound(self, name, filepath):
        """Load a sound file, or create a silent placeholder if file doesn't exist"""
        try:
            if os.path.exists(filepath):
                self.sounds[name] = pygame.mixer.Sound(filepath)
            else:
                # Create a minimal silent sound as placeholder
                # This prevents crashes if sound files are missing
                print(f"Warning: Sound file '{filepath}' not found. Using silent placeholder.")
                # Create a very short silent sound buffer
                import numpy as np
                silent = np.zeros((100, 2), dtype=np.int16)
                self.sounds[name] = pygame.sndarray.make_sound(silent)
        except Exception as e:
            print(f"Error loading sound '{name}': {e}")
            # Create silent placeholder on any error
            try:
                import numpy as np
                silent = np.zeros((100, 2), dtype=np.int16)
                self.sounds[name] = pygame.sndarray.make_sound(silent)
            except:
                self.sounds[name] = None
    
    def play_paddle_hit(self):
        """Play paddle hit sound"""
        if self.sounds.get('paddle_hit'):
            self.sounds['paddle_hit'].play()
    
    def play_wall_bounce(self):
        """Play wall bounce sound"""
        if self.sounds.get('wall_bounce'):
            self.sounds['wall_bounce'].play()
    
    def play_score(self):
        """Play scoring sound"""
        if self.sounds.get('score'):
            self.sounds['score'].play()