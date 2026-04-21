# npc.py - Customers that you talk to

# Import pygame for drawing shapes and text
import pygame
# Import colour constants from settings.py
from settings import BLACK, WHITE, GREEN


# =============================================================================
# NPC CLASS (Non-Player Character)
# =============================================================================
# This class represents customer NPCs (Non-Player Characters) in the shop.
# Each NPC has:
#   - A name displayed above their head
#   - A position (x, y) on the screen
#   - A colour (different for each character)
#   - A "nearby" flag that becomes True when the player is close
# The NPC is drawn as a coloured circle with simple eyes and a name label.
# When the player is within 60 pixels, a green "Z" prompt appears above the NPC.
# The proximity detection is used by main.py to trigger conversations.
# =============================================================================
class NPC:

    # -------------------------------------------------------------------------
    # INITIALISATION METHOD (__init__)
    # -------------------------------------------------------------------------
    # This method runs when a new NPC object is created (called from main.py).
    # It sets up the NPC's name, position, colour, and other properties.
    #
    # Parameters:
    #   name: the NPC's name (e.g., "Maria", "Carlos")
    #   x: the X coordinate (horizontal position) on the screen
    #   y: the Y coordinate (vertical position) on the screen
    #   color: the RGB colour tuple for the NPC's body
    # -------------------------------------------------------------------------
    def __init__(self, name, x, y, color):
        # Store the NPC's name (displayed above their head)
        self.name = name
        # Store the NPC's X position on the screen
        self.x = x
        # Store the NPC's Y position on the screen
        self.y = y
        # Store the NPC's colour (used for drawing the circle)
        self.color = color
        # Create a nearby flag (True if player is within 60 pixels)
        # This is used by main.py to check if player can talk to this NPC
        self.nearby = False
        # Create a font object for rendering the NPC's name (24 pixels)
        self.font = pygame.font.Font(None, 24)

    # -------------------------------------------------------------------------
    # DRAW METHOD (draw)
    # -------------------------------------------------------------------------
    # This method draws the NPC on the screen. It is called from main.py
    # during the shop screen drawing loop.
    # It draws:
    #   - A coloured circle for the body
    #   - A black border around the circle
    #   - Two white circles for eyes
    #   - The NPC's name below the circle
    #   - A green "Z" prompt if the player is nearby (within 60 pixels)
    # -------------------------------------------------------------------------
    def draw(self, screen):
        # Draw the NPC's body as a coloured circle at position (x, y) with radius 25
        pygame.draw.circle(screen, self.color, (self.x, self.y), 25)
        # Draw a black border around the circle (2 pixels thick)
        pygame.draw.circle(screen, BLACK, (self.x, self.y), 25, 2)

        # Draw the left eye as a white circle (radius 4)
        pygame.draw.circle(screen, WHITE, (self.x - 10, self.y - 5), 4)
        # Draw the right eye as a white circle (radius 4)
        pygame.draw.circle(screen, WHITE, (self.x + 10, self.y - 5), 4)

        # Mouth is commented out (removed because it looked like a sad face)
        # pygame.draw.arc(screen, BLACK, (self.x - 10, self.y + 5, 20, 15), 0, 3.14, 2)

        # Render the NPC's name as a text surface
        name_text = self.font.render(self.name, True, BLACK)
        # Draw the name centred above the NPC's head (20 pixels above centre)
        screen.blit(name_text, (self.x - 20, self.y - 40))

        # If the player is nearby (within 60 pixels) - set by check_nearby() method
        if self.nearby:
            # Create a larger font for the interaction prompt (36 pixels)
            z_font = pygame.font.Font(None, 36)
            # Render the letter "Z" in green (prompt to press Z key)
            z_text = z_font.render("Z", True, GREEN)
            # Draw the "Z" centred above the NPC's head
            screen.blit(z_text, (self.x - 8, self.y - 35))

    # -------------------------------------------------------------------------
    # PROXIMITY DETECTION METHOD (check_nearby)
    # -------------------------------------------------------------------------
    # This method checks how far the player is from the NPC.
    # It uses the Pythagorean theorem to calculate Euclidean distance.
    # If the distance is less than 60 pixels, the NPC is considered "nearby".
    # This method is called every frame (60 times per second) from the update()
    # method in main.py.
    #
    # Parameters:
    #   player_x: the X coordinate of the player character (from player.py)
    #   player_y: the Y coordinate of the player character (from player.py)
    #
    # Returns:
    #   True if the player is within 60 pixels, False otherwise
    # -------------------------------------------------------------------------
    def check_nearby(self, player_x, player_y):
        # Calculate Euclidean distance between player and NPC
        # Formula: sqrt((x2 - x1)^2 + (y2 - y1)^2)
        distance = ((player_x - self.x) ** 2 + (player_y - self.y) ** 2) ** 0.5
        # Set nearby to True if distance is less than 60 pixels
        self.nearby = distance < 60
        # Return the nearby status (True/False) back to main.py
        return self.nearby