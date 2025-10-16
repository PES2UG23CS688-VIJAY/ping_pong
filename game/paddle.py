import pygame

class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 7  # Base speed, adjusted dynamically by GameEngine for AI

    def move(self, dy, screen_height):
        """Moves the paddle vertically, clamping its position to the screen boundaries."""
        self.y += dy
        self.y = max(0, min(self.y, screen_height - self.height))

    def rect(self):
        """Returns the Pygame Rect object for collision detection and drawing."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def auto_track(self, ball, screen_height):
        """Simple AI logic: moves the paddle toward the ball's center."""
        # Use the current self.speed (set by GameEngine) for movement
        if ball.y < self.y:
            self.move(-self.speed, screen_height)
        elif ball.y > self.y + self.height:
            self.move(self.speed, screen_height)
