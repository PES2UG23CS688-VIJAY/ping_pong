import pygame
from .paddle import Paddle
from .ball import Ball
from .sound_manager import SoundManager 
import time 

WHITE = (255, 255, 255)

class GameEngine:
    # FIX: Added winning_score parameter (Task 2 & 3)
    def __init__(self, width, height, winning_score=5): 
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        # Initialize Sound Manager (Task 4)
        self.sound_manager = SoundManager()

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        # PASS: Pass the sound_manager instance to the Ball
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height, sound_manager=self.sound_manager) 

        self.player_score = 0
        self.ai_score = 0
        self.font_size = 30
        self.font = pygame.font.SysFont("Arial", self.font_size)
        
        # New state variables (Task 2 & 3)
        self.game_over = False
        self.winning_score = winning_score 
        

    def handle_input(self):
        keys = pygame.key.get_pressed()
        player_movement_speed = 10 
        
        if keys[pygame.K_w]:
            self.player.move(-player_movement_speed, self.height)
        if keys[pygame.K_s]:
            self.player.move(player_movement_speed, self.height)

    def update(self):
        if self.game_over:
            return 

        # Enforce max speed cap on the ball's horizontal velocity
        # Note: ball.max_velocity must be defined in ball.py
        self.ball.velocity_x = max(-self.ball.max_velocity, min(self.ball.velocity_x, self.ball.max_velocity))
        
        self.ball.move()
        # Ball's check_collision now handles sound playback (Task 4)
        self.ball.check_collision(self.player, self.ai)

        # Scoring logic
        scored = False
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
            scored = True
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()
            scored = True
            
        if scored:
            self.sound_manager.play_score() # Play score sound (Task 4)
            # Use a slightly longer sleep or a non-blocking timer in a real game
            time.sleep(0.5) 

        self.ai.auto_track(self.ball, self.height)
        
        # AI speed adjustment (makes AI more challenging as ball speeds up)
        # It's based on the absolute current ball velocity for responsiveness
        self.ai.speed = min(abs(self.ball.velocity_x) + 2, 10) 
        
        # Check for game end condition (Task 2)
        if self.player_score >= self.winning_score or self.ai_score >= self.winning_score:
            self.game_over = True
            
    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        # Draw center line
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))
        
        # Game Over Screen (Task 2 & 3)
        if self.game_over:
            self._draw_game_over(screen)

    def _draw_game_over(self, screen):
        
        # Determine the winner
        if self.player_score >= self.winning_score:
            winner = "Player"
        else:
            winner = "AI"
            
        # Render the text
        end_font_large = pygame.font.SysFont("Arial", 50, bold=True)
        end_font_small = pygame.font.SysFont("Arial", 25)
        
        winner_surface = end_font_large.render(f"{winner} Wins!", True, WHITE)
        replay_surface = end_font_small.render("Press 3, 5, or 7 for Best-of-N, or ESC to Exit", True, WHITE)
        
        # Center the large text
        winner_rect = winner_surface.get_rect(center=(self.width // 2, self.height // 2 - 30))
        # Center the small text below the large text
        replay_rect = replay_surface.get_rect(center=(self.width // 2, self.height // 2 + 30))
        
        screen.blit(winner_surface, winner_rect)
        screen.blit(replay_surface, replay_rect)
