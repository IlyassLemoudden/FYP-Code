# player.py - The character you control

# Import pygame for drawing and input handling
import pygame
# Import constants from settings.py (screen dimensions, colours)
from settings import WIDTH, HEIGHT, LIGHT_BLUE, BLACK, WHITE


# =============================================================================
# PLAYER CLASS
# =============================================================================
# This class represents the player character (the shopkeeper).
# The player can move around the shop using WASD or arrow keys.
# The player is drawn as a light blue square with simple eyes and a "You" label.
# Movement is restricted to stay within the screen boundaries.
# This class is used by main.py to create and control the player.
# =============================================================================
class Player:

    # -------------------------------------------------------------------------
    # INITIALISATION METHOD (__init__)
    # -------------------------------------------------------------------------
    # This method runs when a new Player object is created (called from main.py).
    # It sets up the player's starting position and movement speed.
    #
    # Parameters:
    #   x: the starting X coordinate (horizontal position)
    #   y: the starting Y coordinate (vertical position)
    # -------------------------------------------------------------------------
    def __init__(self, x, y):
        # Store the player's X position on the screen
        self.x = x
        # Store the player's Y position on the screen
        self.y = y
        # Set the player's movement speed (pixels per frame)
        self.speed = 5

    # -------------------------------------------------------------------------
    # MOVEMENT METHOD (move)
    # -------------------------------------------------------------------------
    # This method moves the player based on which keys are pressed.
    # It supports both arrow keys and WASD keys for movement.
    # The method also prevents the player from moving off the screen edges.
    # This method is called every frame from the update() method in main.py.
    #
    # Parameters:
    #   keys: a list of booleans representing which keys are currently pressed
    #         (obtained from pygame.key.get_pressed() in main.py)
    # -------------------------------------------------------------------------
    def move(self, keys):
        # MOVE LEFT: Left arrow key OR A key
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            # Decrease X coordinate (move left)
            self.x -= self.speed
        # MOVE RIGHT: Right arrow key OR D key
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            # Increase X coordinate (move right)
            self.x += self.speed
        # MOVE UP: Up arrow key OR W key
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            # Decrease Y coordinate (move up)
            self.y -= self.speed
        # MOVE DOWN: Down arrow key OR S key
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            # Increase Y coordinate (move down)
            self.y += self.speed

        # BOUNDARY DETECTION - prevent player from leaving the screen
        # Check if player has moved past the left edge (X < 50)
        if self.x < 50:
            # Stop at the left edge
            self.x = 50
        # Check if player has moved past the right edge (X > WIDTH - 50)
        if self.x > WIDTH - 50:
            # Stop at the right edge
            self.x = WIDTH - 50
        # Check if player has moved past the top edge (Y < 50)
        if self.y < 50:
            # Stop at the top edge
            self.y = 50
        # Check if player has moved past the bottom edge (Y > HEIGHT - 100)
        if self.y > HEIGHT - 100:
            # Stop at the bottom edge (above the counter)
            self.y = HEIGHT - 100

    # -------------------------------------------------------------------------
    # DRAW METHOD (draw)
    # -------------------------------------------------------------------------
    # This method draws the player character on the screen.
    # It is called from the draw() method in main.py.
    # It draws:
    #   - A light blue square (40x40 pixels) for the body
    #   - A black border around the square
    #   - Two white circles for eyes
    #   - A "You" label above the player's head
    # -------------------------------------------------------------------------
    def draw(self, screen):
        # Draw the player's body as a light blue square
        # The square is 40x40 pixels, centred on the player's position
        pygame.draw.rect(screen, LIGHT_BLUE, (self.x - 20, self.y - 20, 40, 40))
        # Draw a black border around the square (2 pixels thick)
        pygame.draw.rect(screen, BLACK, (self.x - 20, self.y - 20, 40, 40), 2)

        # Draw the left eye as a white circle (radius 5)
        pygame.draw.circle(screen, WHITE, (self.x - 10, self.y - 10), 5)
        # Draw the right eye as a white circle (radius 5)
        pygame.draw.circle(screen, WHITE, (self.x + 10, self.y - 10), 5)

        # Create a font for the "You" label (24 pixels)
        font = pygame.font.Font(None, 24)
        # Render the word "You" as a text surface
        name = font.render("You", True, BLACK)
        # Draw the "You" label centred above the player's head
        screen.blit(name, (self.x - 15, self.y - 45))