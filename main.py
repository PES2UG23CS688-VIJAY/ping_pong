import pygame
import time 
from game.game_engine import GameEngine

# Initialize pygame/Start application
pygame.init()
# Initialize the mixer for sound (Task 4 setup)
pygame.mixer.init() 

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game loop
# Start with a default winning score of 5
engine = GameEngine(WIDTH, HEIGHT, winning_score=5) 

def main():
    global engine
    running = True
    while running:
        
        # --- 1. Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle Replay Input on key press when game is over (Task 3)
            if engine.game_over and event.type == pygame.KEYDOWN:
                new_score_limit = None
                
                # Check for Best-of-N options
                if event.key == pygame.K_3:
                    new_score_limit = 3
                elif event.key == pygame.K_5:
                    new_score_limit = 5
                elif event.key == pygame.K_7:
                    new_score_limit = 7
                elif event.key == pygame.K_ESCAPE:
                    running = False
                
                if new_score_limit is not None:
                    # Restart the game with the new score limit
                    # Recreate the GameEngine instance
                    engine = GameEngine(WIDTH, HEIGHT, winning_score=new_score_limit) 
        
        # --- 2. Game Logic (Update/Render) ---
        # Only run physics and input when the game is not over
        if not engine.game_over:
            engine.handle_input()
            engine.update()
                
        # --- 3. Drawing ---
        SCREEN.fill(BLACK)
        engine.render(SCREEN)

        # --- 4. Display Update ---
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
