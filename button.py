# button.py - A simple button you can click

# Import pygame for drawing
import pygame
# Import BLACK colour constant from settings.py
from settings import BLACK


# =============================================================================
# BUTTON CLASS
# =============================================================================
# This class represents a clickable button in the game interface.
# Each button has:
#   - A position (x, y) on the screen
#   - A width and height
#   - Text displayed on the button
#   - A colour (changes when selected/highlighted)
#   - A shadow effect for visual depth
# The button can detect when it is clicked using its rectangle area.
# This class is used extensively throughout main.py to create all UI buttons.
# =============================================================================
class Button:

    # -------------------------------------------------------------------------
    # INITIALISATION METHOD (__init__)
    # -------------------------------------------------------------------------
    # This method runs when a new Button object is created (called from main.py).
    # It sets up the button's position, size, text, and colours.
    #
    # Parameters:
    #   x: the X coordinate of the button's top-left corner
    #   y: the Y coordinate of the button's top-left corner
    #   width: the width of the button in pixels
    #   height: the height of the button in pixels
    #   text: the text to display on the button
    #   color: the RGB colour of the button's background
    # -------------------------------------------------------------------------
    def __init__(self, x, y, width, height, text, color):
        # Create a rectangle object for the button (used for positioning and clicks)
        self.rect = pygame.Rect(x, y, width, height)
        # Store the text that appears on the button
        self.text = text
        # Store the button's background colour
        self.color = color
        # Store the original colour (used when resetting)
        self.original_color = color
        # Create a font for the button text (32 pixels)
        self.font = pygame.font.Font(None, 32)
        # Create a selected flag (True if this button is currently highlighted)
        # This is used for language buttons to show which language is selected
        self.selected = False

    # -------------------------------------------------------------------------
    # DRAW METHOD (draw)
    # -------------------------------------------------------------------------
    # This method draws the button on the screen.
    # It is called from the draw() method in main.py.
    # It draws:
    #   - A grey shadow offset 3 pixels down and right
    #   - The button's background rectangle
    #   - A black border around the button
    #   - The button's text centred in the middle
    # If the button is selected, its colour changes to green.
    # -------------------------------------------------------------------------
    def draw(self, screen):
        # Create a copy of the button's rectangle for the shadow
        shadow_rect = self.rect.copy()
        # Move the shadow rectangle 3 pixels right and 3 pixels down
        shadow_rect.x += 3
        shadow_rect.y += 3
        # Draw the grey shadow rectangle
        pygame.draw.rect(screen, (80, 80, 80), shadow_rect)

        # Determine the button's colour (green if selected, otherwise normal colour)
        draw_color = (100, 200, 100) if self.selected else self.color
        # Draw the button's background rectangle
        pygame.draw.rect(screen, draw_color, self.rect)
        # Draw a black border around the button (2 pixels thick)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        # Render the button's text as a surface
        text_surface = self.font.render(self.text, True, BLACK)
        # Get a rectangle that centres the text within the button
        text_rect = text_surface.get_rect(center=self.rect.center)
        # Draw the text on the screen
        screen.blit(text_surface, text_rect)

    # -------------------------------------------------------------------------
    # CLICK DETECTION METHOD (is_clicked)
    # -------------------------------------------------------------------------
    # This method checks whether the mouse was clicked on this button.
    # It uses the button's rectangle to test if the mouse position is inside.
    # This method is called from the handle_events() method in main.py.
    #
    # Parameters:
    #   mouse_pos: a tuple (x, y) containing the mouse cursor position
    #
    # Returns:
    #   True if the mouse position is inside the button's rectangle
    # -------------------------------------------------------------------------
    def is_clicked(self, mouse_pos):
        # Check if the mouse position collides with the button's rectangle
        return self.rect.collidepoint(mouse_pos)