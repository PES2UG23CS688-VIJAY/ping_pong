import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height, sound_manager=None):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])
        
        # Sound manager reference
        self.sound_manager = sound_manager
        
        # Max velocity cap to prevent ball from becoming too fast
        self.max_velocity = 15

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Check wall collision (top and bottom)
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            # Play wall bounce sound
            if self.sound_manager:
                self.sound_manager.play_wall_bounce()

    def check_collision(self, player, ai):
        # Check collision with paddles
        if self.rect().colliderect(player.rect()) or self.rect().colliderect(ai.rect()):
            self.velocity_x *= -1
            
            # Slightly increase ball speed on each paddle hit (up to max_velocity)
            if abs(self.velocity_x) < self.max_velocity:
                if self.velocity_x > 0:
                    self.velocity_x += 0.5
                else:
                    self.velocity_x -= 0.5
            
            # Play paddle hit sound
            if self.sound_manager:
                self.sound_manager.play_paddle_hit()

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)