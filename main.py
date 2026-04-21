# main.py - The main game with improved visuals and minigame

# Import the pygame library for game development (handles graphics, input, sound)
import pygame
# Import the sys library for clean program exit (sys.exit())
import sys
# Import the random library for shuffling response options randomly
import random
# Import all constants from settings.py (WIDTH, HEIGHT, colours, FPS, API_KEY)
from settings import *
# Import the Button class from button.py for clickable UI elements (buttons, menus)
from button import Button
# Import the Player class from player.py for the shopkeeper character (movement, drawing)
from player import Player
# Import the NPC class from npc.py for customer characters (proximity, drawing)
from npc import NPC
# Import the DialogueGenerator class from dialogue.py for Gemini API calls (dialogue generation)
from dialogue import DialogueGenerator
# Import the UnscrambleGame class from minigame.py for the word unscramble minigame
from minigame import UnscrambleGame

# =============================================================================
# PYGAME INITIALISATION SECTION
# =============================================================================
# This section initialises pygame and sets up the game window, display settings,
# clock, and fonts. These settings remain constant throughout the entire game.
# =============================================================================

# Initialise all pygame modules (must be called before any other pygame functions)
pygame.init()
# Create the game window with width and height imported from settings.py
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Set the title that appears on the window's title bar
pygame.display.set_caption("Language Learning Shop")
# Create a clock object to control the game's frame rate (60 FPS)
clock = pygame.time.Clock()
# Create a font object for normal-sized text (36 pixels)
font = pygame.font.Font(None, 36)
# Create a font object for small text (24 pixels) for buttons and labels
small_font = pygame.font.Font(None, 24)
# Create a font object for large text (48 pixels) for titles and headings
big_font = pygame.font.Font(None, 48)


# =============================================================================
# GAME CLASS
# =============================================================================
# This is the main class that controls the entire game application.
# It manages game state (which screen is showing), player statistics,
# NPC creation, dialogue generation, minigame integration, button creation,
# and all drawing operations. The game has 5 possible states:
#   - "menu": Main menu where player selects language
#   - "shop": Main gameplay where player moves and talks to NPCs
#   - "talk": Conversation screen with response options
#   - "feedback": Shows score after answering a question
#   - "minigame": Word unscramble minigame screen
# =============================================================================
class Game:

    # -------------------------------------------------------------------------
    # INITIALISATION METHOD (__init__)
    # -------------------------------------------------------------------------
    # This method runs automatically when a new Game object is created.
    # It sets up all starting values including game state, player statistics,
    # player character, NPCs, dialogue system, and empty button list.
    # No parameters are required.
    # -------------------------------------------------------------------------
    def __init__(self):
        # Set running to True so the main game loop continues to run
        self.running = True
        # Set initial game state to "menu" (the main menu screen)
        self.state = "menu"

        # Create a list of all available languages for the player to choose from
        self.languages = ["English", "Spanish", "French", "German", "Italian"]
        # Set the default language to English (easiest for initial testing)
        self.language = "English"

        # Set the shop type to bakery (currently fixed, could be expanded later)
        self.shop_type = "bakery"

        # Set starting money to 100 (earned by selecting good response options)
        self.money = 100
        # Set starting total score to 0 (accumulates points from all conversations)
        self.total_score = 0
        # Set starting day to 1 (increases by 0.5 after each conversation)
        self.day = 1
        # Set starting customer count to 0 (increases by 1 after each conversation)
        self.customers = 0

        # Create the player character using the Player class from player.py
        # Position: centre of the screen, near the bottom (behind the counter)
        self.player = Player(WIDTH // 2, HEIGHT - 100)
        # Create a list of three NPC customers using the NPC class from npc.py
        # Each NPC has a name, position (x, y), and colour
        self.npcs = [
            # Maria: pink customer on the left side of the shop (x=200)
            NPC("Maria", 200, 300, (255, 200, 200)),
            # Carlos: blue customer on the right side of the shop (x=800)
            NPC("Carlos", 800, 400, (180, 200, 255)),
            # Sofia: purple customer in the middle of the shop (x=500)
            NPC("Sofia", 500, 550, (200, 180, 255)),
        ]

        # Create the dialogue generator object from dialogue.py (handles all Gemini API communication)
        self.dialogue = DialogueGenerator()
        # Set talking_to to None (no NPC is currently being talked to)
        self.talking_to = None
        # Set customer_text to empty string (will be filled by API response from dialogue.py)
        self.customer_text = ""
        # Set response_options to empty list (will be filled by API response from dialogue.py)
        self.response_options = []
        # Set last_score to 0 (will be set when player selects a response option)
        self.last_score = 0

        # Set minigame to None (will be created using UnscrambleGame class from minigame.py)
        self.minigame = None

        # Create an empty list for buttons (buttons are created dynamically per screen)
        self.buttons = []

    # -------------------------------------------------------------------------
    # TEXT WRAPPING METHOD (wrap_text)
    # -------------------------------------------------------------------------
    # This function takes a long string of text and breaks it into multiple lines
    # so it fits within a specified pixel width. It is used for long dialogue
    # options that would otherwise overflow the button width. The function splits
    # the text at word boundaries (spaces) to avoid breaking words in half.
    #
    # Parameters:
    #   text: the string of text to be wrapped
    #   max_width: the maximum pixel width allowed for a single line
    #
    # Returns:
    #   A list of strings, where each string is one line of wrapped text
    # -------------------------------------------------------------------------
    def wrap_text(self, text, max_width):
        # Split the text into individual words using spaces as separators
        words = text.split()
        # Create an empty list to store completed lines of text
        lines = []
        # Create an empty list to store words in the current line being built
        current_line = []

        # Loop through each word in the text one by one
        for word in words:
            # Create a test line by joining current words plus the new word
            test_line = ' '.join(current_line + [word])
            # Check if the test line would fit within the maximum pixel width
            if font.size(test_line)[0] <= max_width:
                # If it fits, add the word to the current line
                current_line.append(word)
            else:
                # If it doesn't fit and there are words in the current line
                if current_line:
                    # Join the current line into a string and add to lines list
                    lines.append(' '.join(current_line))
                # Start a new line with the current word
                current_line = [word]

        # After the loop finishes, if there are still words in the current line
        if current_line:
            # Join them into a string and add to lines list
            lines.append(' '.join(current_line))

        # Return the list of wrapped text lines
        return lines

    # -------------------------------------------------------------------------
    # MAIN MENU BUTTON CREATION (create_menu_buttons)
    # -------------------------------------------------------------------------
    # This method creates all buttons that appear on the main menu screen.
    # It creates a Start Game button (green, centred) and language selection
    # buttons for each supported language (arranged vertically). The currently
    # selected language button is highlighted in green for visual feedback.
    # All buttons are created using the Button class from button.py
    # -------------------------------------------------------------------------
    def create_menu_buttons(self):
        # Clear the existing buttons list to start fresh
        self.buttons = []

        # Create the Start Game button using Button class from button.py
        # Position: (x=412, y=300) with size 200x50 pixels
        self.buttons.append(Button(WIDTH // 2 - 100, 300, 200, 50, "Start Game", (100, 200, 100)))

        # Loop through each language in the languages list with its index number
        for i, lang in enumerate(self.languages):
            # Create a button for this language using Button class from button.py
            btn = Button(WIDTH // 2 - 80, 400 + i * 40, 160, 30, lang, (173, 216, 230))
            # If this button's language matches the currently selected language
            if lang == self.language:
                # Set the button's selected property to True (will show as green)
                btn.selected = True
            # Add the newly created button to the buttons list
            self.buttons.append(btn)

    # -------------------------------------------------------------------------
    # SHOP SCREEN BUTTON CREATION (create_shop_buttons)
    # -------------------------------------------------------------------------
    # This method creates buttons that appear on the main shop screen.
    # It creates a Main Menu button (bottom left) to return to language selection,
    # and a Minigame button (bottom right) to launch the word unscramble minigame.
    # All buttons are created using the Button class from button.py
    # -------------------------------------------------------------------------
    def create_shop_buttons(self):
        # Clear the existing buttons list to start fresh
        self.buttons = []

        # Create Main Menu button using Button class from button.py
        # Position: bottom left (20px from left, 60px from bottom)
        self.buttons.append(Button(20, HEIGHT - 60, 120, 40, "Main Menu", (100, 200, 100)))

        # Create Minigame button using Button class from button.py
        # Position: bottom right (140px from right, 60px from bottom)
        self.buttons.append(Button(WIDTH - 140, HEIGHT - 60, 120, 40, "Minigame", (100, 200, 100)))

    # -------------------------------------------------------------------------
    # CONVERSATION BUTTON CREATION (create_talk_buttons)
    # -------------------------------------------------------------------------
    # This method creates buttons for the conversation screen where the player
    # chooses a response. It creates four large buttons, one for each response
    # option, stacked vertically. The buttons are tall enough to accommodate
    # wrapped text (multiple lines). It also creates a Back button to exit the
    # conversation without answering. Each response button stores its score
    # value so the game knows how many points to award when clicked.
    # All buttons are created using the Button class from button.py
    # -------------------------------------------------------------------------
    def create_talk_buttons(self):
        # Clear the existing buttons list to start fresh
        self.buttons = []

        # Set the Y position where the first response button will appear
        start_y = 320
        # Set the width of each response button (wide for long text)
        button_width = 900
        # Set the height of each response button (tall for wrapped text)
        button_height = 65

        # Loop through each response option with its index number
        for i, option in enumerate(self.response_options):
            # Create a new button for this response option using Button class from button.py
            button = Button(
                # X position: centred horizontally on screen
                WIDTH // 2 - button_width // 2,
                # Y position: stacked vertically with 8px gap between buttons
                start_y + i * (button_height + 8),
                # Width of the button in pixels
                button_width,
                # Height of the button in pixels
                button_height,
                # Text to display on the button (the response option)
                option["text"],
                # Light grey-blue colour for the button background
                (220, 220, 250)
            )
            # Store the score value for this response option on the button object
            button.score = option["score"]
            # Store pre-wrapped text lines for this button (to avoid recalculating)
            button.wrapped_lines = self.wrap_text(option["text"], button_width - 40)
            # Add the newly created button to the buttons list
            self.buttons.append(button)

        # Add a Back button using Button class from button.py at bottom left
        self.buttons.append(Button(20, HEIGHT - 60, 120, 40, "Back", (173, 216, 230)))

    # -------------------------------------------------------------------------
    # FEEDBACK BUTTON CREATION (create_feedback_buttons)
    # -------------------------------------------------------------------------
    # This method creates the Continue button for the feedback screen.
    # After seeing their score and feedback message, the player clicks Continue
    # to return to the shop screen and continue playing.
    # The button is created using the Button class from button.py
    # -------------------------------------------------------------------------
    def create_feedback_buttons(self):
        # Create a single Continue button using Button class from button.py
        # Position: centred horizontally near the bottom
        self.buttons = [Button(WIDTH // 2 - 100, 600, 200, 50, "Continue", (100, 200, 100))]

    # -------------------------------------------------------------------------
    # EVENT HANDLING METHOD (handle_events)
    # -------------------------------------------------------------------------
    # This method processes all user input including window closing, keyboard
    # presses (Z to talk, Enter to submit, Backspace to delete, ESC to go back),
    # and mouse clicks on buttons. Different screens handle different inputs.
    # For example, the shop screen listens for Z key to talk to nearby NPCs,
    # while the minigame screen listens for typing letters and Enter to submit.
    # Button clicks are detected using the is_clicked() method from button.py
    # -------------------------------------------------------------------------
    def handle_events(self):
        # Loop through all events in pygame's event queue
        for event in pygame.event.get():
            # Check if the player clicked the window's close button (X)
            if event.type == pygame.QUIT:
                # Set running to False to exit the main game loop
                self.running = False

            # Check if a keyboard key was pressed down
            elif event.type == pygame.KEYDOWN:
                # SHOP SCREEN: Check if we're in shop and Z key was pressed
                if self.state == "shop" and event.key == pygame.K_z:
                    # Loop through each NPC to check if any are nearby
                    for npc in self.npcs:
                        # If this NPC is nearby (within 60 pixels) - uses check_nearby() from npc.py
                        if npc.nearby:
                            # Start a conversation with this NPC (calls start_talking method)
                            self.start_talking(npc)
                            # Exit the loop (only talk to the first nearby NPC)
                            break

                # MINIGAME SCREEN: Check if we're in minigame and minigame exists
                elif self.state == "minigame" and self.minigame:
                    # Check if the minigame is still active (not game over)
                    if self.minigame.active:
                        # If Enter/Return key was pressed
                        if event.key == pygame.K_RETURN:
                            # If the player has typed something (not empty)
                            if self.minigame.player_input.strip():
                                # Call check_answer() from minigame.py to verify the answer
                                self.minigame.check_answer()
                        # If Backspace key was pressed
                        elif event.key == pygame.K_BACKSPACE:
                            # Remove the last character from the player's input
                            self.minigame.player_input = self.minigame.player_input[:-1]
                        # If Escape key was pressed
                        elif event.key == pygame.K_ESCAPE:
                            # Deactivate the minigame
                            self.minigame.active = False
                            # Return to shop screen
                            self.state = "shop"
                            # Recreate shop buttons
                            self.create_shop_buttons()
                        # For any other key (letters, numbers)
                        else:
                            # If input is less than 20 characters long
                            if len(self.minigame.player_input) < 20:
                                # Add the typed character to the input string
                                self.minigame.player_input += event.unicode
                    else:
                        # Game over screen - only ESC key works
                        if event.key == pygame.K_ESCAPE:
                            # Return to shop screen
                            self.state = "shop"
                            # Recreate shop buttons
                            self.create_shop_buttons()

            # Check if the mouse button was clicked (pressed and released)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the current position of the mouse cursor
                mouse_pos = pygame.mouse.get_pos()

                # MINIGAME SCREEN: Check minigame buttons first (priority)
                if self.state == "minigame" and self.minigame:
                    # Call get_button_rects() from minigame.py to get button areas
                    submit_rect, quit_rect = self.minigame.get_button_rects()
                    # If submit button exists and mouse clicked on it
                    if submit_rect and submit_rect.collidepoint(mouse_pos):
                        # If minigame is active and player typed something
                        if self.minigame.active and self.minigame.player_input.strip():
                            # Call check_answer() from minigame.py to verify the answer
                            self.minigame.check_answer()
                    # If quit button exists and mouse clicked on it
                    elif quit_rect and quit_rect.collidepoint(mouse_pos):
                        # Deactivate the minigame
                        self.minigame.active = False
                        # Return to shop screen
                        self.state = "shop"
                        # Recreate shop buttons
                        self.create_shop_buttons()
                    # Exit the method early (don't check other buttons)
                    return

                # OTHER SCREENS: Loop through all regular buttons
                for button in self.buttons:
                    # Call is_clicked() from button.py to check if button was clicked
                    if button.is_clicked(mouse_pos):
                        # Call handle_button to process what this button does
                        self.handle_button(button)
                        # Exit the loop (only process the first clicked button)
                        break

    # -------------------------------------------------------------------------
    # BUTTON ACTION HANDLER (handle_button)
    # -------------------------------------------------------------------------
    # This method determines what happens when a button is clicked.
    # Different screens have different buttons that do different things:
    #   - Menu screen: Start Game starts the game, language buttons change language
    #   - Shop screen: Main Menu goes back, Minigame launches the minigame
    #   - Talk screen: Response buttons award points, Back exits conversation
    #   - Feedback screen: Continue returns to shop
    # The button's text determines which action to take.
    # The Minigame button creates a new UnscrambleGame object from minigame.py
    # -------------------------------------------------------------------------
    def handle_button(self, button):
        # ---------- MAIN MENU SCREEN ----------
        if self.state == "menu":
            # If the clicked button is "Start Game"
            if button.text == "Start Game":
                # Change game state to shop screen
                self.state = "shop"
                # Create buttons for the shop screen
                self.create_shop_buttons()
            # If the clicked button text matches any language name
            elif button.text in self.languages:
                # Set the current language to the button's text
                self.language = button.text
                # Recreate menu buttons (updates which button is highlighted)
                self.create_menu_buttons()

        # ---------- SHOP SCREEN ----------
        elif self.state == "shop":
            # If the clicked button is "Main Menu"
            if button.text == "Main Menu":
                # Change game state back to main menu
                self.state = "menu"
                # Create buttons for the main menu
                self.create_menu_buttons()
            # If the clicked button is "Minigame"
            elif button.text == "Minigame":
                # Create a new minigame object using UnscrambleGame class from minigame.py
                # Pass current language and dialogue generator (from dialogue.py)
                self.minigame = UnscrambleGame(self.language, self.dialogue)
                # Call start_game() from minigame.py to begin the minigame
                self.minigame.start_game()
                # Change game state to minigame screen
                self.state = "minigame"

        # ---------- CONVERSATION SCREEN ----------
        elif self.state == "talk":
            # If the clicked button is "Back"
            if button.text == "Back":
                # Return to shop screen without answering
                self.state = "shop"
                # Recreate shop buttons
                self.create_shop_buttons()
            else:
                # Player selected a response option button
                # Get the score stored on the button (default to 5 if missing)
                self.last_score = getattr(button, 'score', 5)
                # Add money: each point earned = $2
                self.money += self.last_score * 2
                # Add points to total score
                self.total_score += self.last_score
                # Increase customer count by 1
                self.customers += 1
                # Change game state to feedback screen
                self.state = "feedback"
                # Create buttons for the feedback screen
                self.create_feedback_buttons()

        # ---------- FEEDBACK SCREEN ----------
        elif self.state == "feedback":
            # If the clicked button is "Continue"
            if button.text == "Continue":
                # Return to shop screen
                self.state = "shop"
                # Increase day by 0.5 (half day passes per conversation)
                self.day += 0.5
                # Recreate shop buttons
                self.create_shop_buttons()

    # -------------------------------------------------------------------------
    # START CONVERSATION METHOD (start_talking)
    # -------------------------------------------------------------------------
    # This method starts a conversation with an NPC when the player presses Z
    # while standing close to them. It performs three main actions:
    #   1. Calls get_customer_dialogue() from dialogue.py to generate what customer says
    #   2. Calls get_response_options() from dialogue.py to generate four response options
    #   3. Randomises the order of the response options so the player can't
    #      memorise which position has the best answer
    # The method then switches to the conversation screen.
    # -------------------------------------------------------------------------
    def start_talking(self, npc):
        # Store the NPC being talked to for later reference
        self.talking_to = npc

        # Call get_customer_dialogue() from dialogue.py to get what the customer says
        # Pass the current language, shop type, and NPC's name
        self.customer_text = self.dialogue.get_customer_dialogue(
            self.language, self.shop_type, npc.name
        )

        # Call get_response_options() from dialogue.py to get four response options
        # Pass the current language, what the customer said, and shop type
        self.response_options = self.dialogue.get_response_options(
            self.language, self.customer_text, self.shop_type
        )
        # Randomly shuffle the response options so the best isn't always first
        random.shuffle(self.response_options)

        # Change game state to conversation screen
        self.state = "talk"
        # Create the buttons for the conversation screen (response options)
        self.create_talk_buttons()

    # -------------------------------------------------------------------------
    # UPDATE METHOD (update)
    # -------------------------------------------------------------------------
    # This method updates game logic every frame (60 times per second).
    # It handles:
    #   - Player movement (calls move() from player.py)
    #   - NPC proximity detection (calls check_nearby() from npc.py)
    # The proximity detection runs every frame so the "Z" prompt appears
    # and disappears instantly as the player moves around the shop.
    # -------------------------------------------------------------------------
    def update(self):
        # Only update if we're on the shop screen
        if self.state == "shop":
            # Get a list of all currently pressed keyboard keys
            keys = pygame.key.get_pressed()
            # Call move() from player.py to move the player based on which keys are pressed
            self.player.move(keys)

            # Loop through each NPC to check proximity to the player
            for npc in self.npcs:
                # Call check_nearby() from npc.py to update NPC's nearby status
                # Pass the player's X and Y coordinates
                npc.check_nearby(self.player.x, self.player.y)

    # -------------------------------------------------------------------------
    # DRAW METHOD (draw)
    # -------------------------------------------------------------------------
    # This is the main drawing method called 60 times per second.
    # It clears the screen and draws everything based on the current state.
    # Different states call different drawing methods:
    #   - "menu": calls draw_menu()
    #   - "shop": calls draw_shop()
    #   - "talk": calls draw_talk()
    #   - "feedback": calls draw_feedback()
    #   - "minigame": calls minigame.draw() from minigame.py
    # After drawing the screen content, it draws all buttons on top.
    # Buttons are drawn using the draw() method from button.py
    # -------------------------------------------------------------------------
    def draw(self):
        # Clear the entire screen with light blue-grey background colour
        screen.fill((240, 240, 255))

        # Call the appropriate drawing method based on current game state
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "shop":
            self.draw_shop()
        elif self.state == "talk":
            self.draw_talk()
        elif self.state == "feedback":
            self.draw_feedback()
        elif self.state == "minigame" and self.minigame:
            # Call draw() from minigame.py to draw the minigame screen
            # Pass the screen surface and font objects
            self.minigame.draw(screen, font, small_font, big_font)
            # Update the display and exit early (buttons drawn by minigame)
            pygame.display.flip()
            return

        # Loop through all buttons and draw them on screen
        for button in self.buttons:
            # If we're in talk screen and button has wrapped text
            if self.state == "talk" and hasattr(button, 'wrapped_lines'):
                # Draw the button with wrapped text (multiple lines)
                self.draw_wrapped_button(button)
            else:
                # Call draw() from button.py to draw the button normally (single line)
                button.draw(screen)

        # Update the display to show everything that was drawn
        pygame.display.flip()

    # -------------------------------------------------------------------------
    # WRAPPED BUTTON DRAWING (draw_wrapped_button)
    # -------------------------------------------------------------------------
    # This method draws buttons that have wrapped text (multiple lines).
    # It is used specifically for the response option buttons in the
    # conversation screen where text might be too long for one line.
    # The text is centred vertically within the button and each line is
    # drawn separately. If the button is selected, it appears green.
    # -------------------------------------------------------------------------
    def draw_wrapped_button(self, button):
        # Start with the button's normal colour
        draw_color = button.color
        # If the button is marked as selected, change to green
        if button.selected:
            draw_color = (100, 200, 100)

        # Draw the button's background rectangle
        pygame.draw.rect(screen, draw_color, button.rect)
        # Draw the button's black border outline
        pygame.draw.rect(screen, BLACK, button.rect, 2)

        # Set the height of each line of text in pixels
        line_height = 30
        # Calculate total height of all wrapped text lines
        total_height = len(button.wrapped_lines) * line_height
        # Calculate starting Y position to centre text vertically
        start_y = button.rect.centery - (total_height // 2) + 13

        # Loop through each line of wrapped text with its index
        for i, line in enumerate(button.wrapped_lines):
            # Render the text line onto a surface
            text_surface = button.font.render(line, True, BLACK)
            # Create rectangle to centre this line horizontally and vertically
            text_rect = text_surface.get_rect(center=(button.rect.centerx, start_y + i * line_height))
            # Draw the text line on the screen
            screen.blit(text_surface, text_rect)

    # -------------------------------------------------------------------------
    # MAIN MENU DRAWING (draw_menu)
    # -------------------------------------------------------------------------
    # This method draws the main menu screen including:
    #   - Brown top bar decoration
    #   - "LingoMarket" title text (white on brown background)
    #   - "Select Language" instruction text
    #   - Instructions at the bottom of the screen
    # The buttons are drawn separately by the main draw() method.
    # -------------------------------------------------------------------------
    def draw_menu(self):
        # Draw brown top bar decoration across the full width of the screen
        pygame.draw.rect(screen, (80, 60, 40), (0, 0, WIDTH, 120))

        # Render the shop name "LingoMarket" as white text
        shop_text = font.render("LingoMarket", True, WHITE)
        # Draw the shop name centred horizontally at Y=50
        screen.blit(shop_text, (WIDTH // 2 - shop_text.get_width() // 2, 50))

        # Render the language selection instruction text in black
        lang_title = small_font.render("Select Language:", True, BLACK)
        # Draw the instruction centred horizontally at Y=260
        screen.blit(lang_title, (WIDTH // 2 - lang_title.get_width() // 2, 260))

        # Render the control instructions in grey text
        inst = small_font.render("WASD or Arrow Keys to move | Press Z to talk", True, GRAY)
        # Draw the instructions centred horizontally near the bottom of the screen
        screen.blit(inst, (WIDTH // 2 - inst.get_width() // 2, HEIGHT - 50))

    # -------------------------------------------------------------------------
    # SHOP SCREEN DRAWING (draw_shop)
    # -------------------------------------------------------------------------
    # This method draws the main shop screen including:
    #   - Wooden floor and wall line (wainscoting effect)
    #   - Decorative shelves with circular items
    #   - "LingoMarket" title with brown background box
    #   - Stats panel (Money, Score, Day, Customers) in dark blue
    #   - Brown counter at the bottom where player stands
    #   - All NPC customers (drawn using draw() from npc.py)
    #   - Player character (drawn using draw() from player.py)
    #   - Instructions at the bottom
    # -------------------------------------------------------------------------
    def draw_shop(self):
        # Draw wooden floor (bottom 180 pixels of screen)
        pygame.draw.rect(screen, (210, 180, 140), (0, HEIGHT - 180, WIDTH, 180))

        # Draw wall line separating wall from floor (wainscoting effect)
        pygame.draw.rect(screen, (180, 150, 110), (0, HEIGHT - 180, WIDTH, 10))

        # DECORATIVE SHELVES with items
        shelf_y = 120  # Y position of the shelves
        shelf_colors = [(160, 100, 50), (150, 90, 45), (170, 110, 55)]  # Wood colours
        # Loop to create 3 shelves across the screen
        for i in range(3):
            # Calculate X position for this shelf (spaced every 320 pixels)
            x = 30 + i * 320
            # Draw the shelf rectangle
            pygame.draw.rect(screen, shelf_colors[i % 3], (x, shelf_y, 280, 12))
            # Draw black border around the shelf
            pygame.draw.rect(screen, (100, 60, 20), (x, shelf_y, 280, 12), 2)

            # Draw 3 circular items on each shelf
            for j in range(3):
                # Calculate X position for each item
                item_x = x + 40 + j * 90
                # Draw the item as a circle
                pygame.draw.circle(screen, (200, 150, 100), (item_x, shelf_y - 12), 8)
                # Draw border around the item
                pygame.draw.circle(screen, (150, 100, 60), (item_x, shelf_y - 12), 8, 1)

        # TITLE with brown background box
        title_bg = pygame.Rect(WIDTH // 2 - 200, 10, 400, 40)
        pygame.draw.rect(screen, (80, 60, 40), title_bg)
        pygame.draw.rect(screen, (120, 90, 60), title_bg, 2)
        title = font.render("LingoMarket", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 18))

        # STATS PANEL - dark blue box showing player progress
        stats_rect = pygame.Rect(WIDTH - 230, 60, 170, 130)
        pygame.draw.rect(screen, (50, 50, 80), stats_rect)
        pygame.draw.rect(screen, (100, 100, 150), stats_rect, 2)

        # Draw each stat line (Money, Score, Day, Customers)
        screen.blit(small_font.render(f"Money: ${self.money}", True, (255, 215, 0)), (WIDTH - 220, 70))
        screen.blit(small_font.render(f"Score: {self.total_score}", True, WHITE), (WIDTH - 220, 100))
        screen.blit(small_font.render(f"Day: {self.day}", True, WHITE), (WIDTH - 220, 130))
        screen.blit(small_font.render(f"Customers: {self.customers}", True, WHITE), (WIDTH - 220, 160))

        # COUNTER - brown rectangle at bottom where player stands
        counter_rect = pygame.Rect(WIDTH // 2 - 180, HEIGHT - 130, 360, 70)
        pygame.draw.rect(screen, (139, 90, 43), counter_rect)
        pygame.draw.rect(screen, (100, 60, 20), counter_rect, 3)
        pygame.draw.rect(screen, (180, 130, 70), (WIDTH // 2 - 180, HEIGHT - 135, 360, 10))

        # Loop through all NPCs and draw each one using draw() from npc.py
        for npc in self.npcs:
            npc.draw(screen)

        # Draw the player character using draw() from player.py
        self.player.draw(screen)

        # Draw control instructions at the bottom of the screen
        inst = small_font.render("WASD to move | Press Z to talk to customers", True, (80, 80, 80))
        screen.blit(inst, (WIDTH // 2 - inst.get_width() // 2, HEIGHT - 35))

    # -------------------------------------------------------------------------
    # CONVERSATION SCREEN DRAWING (draw_talk)
    # -------------------------------------------------------------------------
    # This method draws the conversation screen including:
    #   - Dark overlay to dim the background and focus on conversation
    #   - Conversation panel (dark blue-grey box)
    #   - Title showing which NPC the player is talking to
    #   - White speech bubble with the customer's dialogue text
    #   - Instruction to choose a response
    # The response buttons are drawn separately by the main draw() method.
    # -------------------------------------------------------------------------
    def draw_talk(self):
        # Create a dark overlay surface the size of the screen
        overlay = pygame.Surface((WIDTH, HEIGHT))
        # Set transparency level (180 out of 255 = semi-transparent)
        overlay.set_alpha(180)
        # Fill the overlay with black colour
        overlay.fill((0, 0, 0))
        # Draw the overlay on the screen (dims the background)
        screen.blit(overlay, (0, 0))

        # Draw the conversation panel (dark blue-grey box)
        panel = pygame.Rect(50, 50, WIDTH - 100, HEIGHT - 100)
        pygame.draw.rect(screen, (50, 50, 70), panel)
        pygame.draw.rect(screen, (100, 100, 130), panel, 3)

        # Draw the title showing which NPC the player is talking to
        title = font.render(f"Talking to {self.talking_to.name}", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 65))

        # Draw the white speech bubble rectangle
        bubble = pygame.Rect(70, 90, WIDTH - 140, 80)
        pygame.draw.rect(screen, WHITE, bubble)
        pygame.draw.rect(screen, BLACK, bubble, 2)

        # Wrap the customer's dialogue text to fit in the speech bubble
        wrapped_customer = self.wrap_text(self.customer_text, WIDTH - 200)
        # Loop through each line of wrapped text
        for i, line in enumerate(wrapped_customer):
            # Draw each line of customer dialogue in the speech bubble
            screen.blit(font.render(line, True, BLACK), (90, 105 + i * 35))

        # Draw the instruction text for the player
        inst = font.render("Choose the best response:", True, WHITE)
        screen.blit(inst, (WIDTH // 2 - inst.get_width() // 2, 200))

    # -------------------------------------------------------------------------
    # FEEDBACK SCREEN DRAWING (draw_feedback)
    # -------------------------------------------------------------------------
    # This method draws the feedback screen after a conversation including:
    #   - Dark background
    #   - White panel in the centre
    #   - Score display with colour-coded bar (green for good, red for poor)
    #   - Feedback message based on the score (e.g., "Excellent!")
    #   - What the customer said (for context)
    #   - Points earned (coins) in this conversation
    # The score determines the message, bar colour, and overall feedback.
    # -------------------------------------------------------------------------
    def draw_feedback(self):
        # Fill the entire screen with dark blue-grey colour
        screen.fill((50, 50, 70))

        # Draw the white feedback panel in the centre
        panel = pygame.Rect(50, 50, WIDTH - 100, HEIGHT - 100)
        pygame.draw.rect(screen, (240, 240, 255), panel)
        pygame.draw.rect(screen, BLACK, panel, 3)

        # Draw the "Feedback" title text
        title = font.render("Feedback", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 70))

        # Determine score colour and message based on last_score value
        # Score 9-10: Excellent (green)
        if self.last_score >= 9:
            score_color = (0, 200, 0)
            msg = "Excellent! The customer loved your service!"
        # Score 5-8: Good (yellow/gold)
        elif self.last_score >= 5:
            score_color = (255, 200, 0)
            msg = "Good job! Happy customer!"
        # Score 3-4: Not bad (orange)
        elif self.last_score >= 3:
            score_color = (255, 150, 0)
            msg = "Not bad! Keep practicing!"
        # Score 0-2: Keep trying (red)
        else:
            score_color = (255, 50, 0)
            msg = "Keep trying! Try to be more helpful!"

        # Display the score as large text in the determined colour
        score_text = big_font.render(f"{self.last_score}/10", True, score_color)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 120))

        # Draw the visual score bar
        bar_width = 400  # Total width of the bar in pixels
        bar_height = 30  # Height of the bar in pixels
        # Calculate fill width based on score percentage
        fill = (self.last_score / 10) * bar_width
        # Draw the grey background of the bar
        pygame.draw.rect(screen, GRAY, (WIDTH // 2 - bar_width // 2, 170, bar_width, bar_height))
        # Draw the coloured fill portion of the bar
        pygame.draw.rect(screen, score_color, (WIDTH // 2 - bar_width // 2, 170, fill, bar_height))
        # Draw black border around the bar
        pygame.draw.rect(screen, BLACK, (WIDTH // 2 - bar_width // 2, 170, bar_width, bar_height), 2)

        # Draw the feedback message text
        msg_text = font.render(msg, True, BLACK)
        screen.blit(msg_text, (WIDTH // 2 - msg_text.get_width() // 2, 220))

        # Draw what the customer said (for context)
        screen.blit(small_font.render(f"{self.talking_to.name} said:", True, BLACK), (70, 300))
        wrapped_customer = self.wrap_text(self.customer_text, WIDTH - 200)
        # Loop through up to 2 lines of customer dialogue
        for i, line in enumerate(wrapped_customer[:2]):
            screen.blit(small_font.render(line, True, GRAY), (70, 330 + i * 25))

        # Calculate points earned (each score point = $2)
        points = self.last_score * 2
        # Draw the points earned message in green
        points_text = small_font.render(f"+{points} coins!", True, (0, 150, 0))
        screen.blit(points_text, (WIDTH // 2 - points_text.get_width() // 2, 450))


# =============================================================================
# GAME EXECUTION SECTION
# =============================================================================
# This section creates a Game object and runs the main game loop.
# The game loop runs 60 times per second and processes:
#   - Events (keyboard presses, mouse clicks, window close)
#   - Updates (player movement, NPC proximity detection)
#   - Drawing (all visual elements on screen)
# The loop continues until game.running is set to False.
# =============================================================================

# Create a new instance of the Game class (initialises everything)
game = Game()
# Create the buttons for the main menu using create_menu_buttons() method
game.create_menu_buttons()

# MAIN GAME LOOP - runs repeatedly until game.running becomes False
while game.running:
    # Call handle_events() to process all user input (keyboard, mouse, window events)
    game.handle_events()
    # Call update() to update game logic (player movement, NPC proximity detection)
    game.update()
    # Call draw() to draw everything on the screen (based on current game state)
    game.draw()
    # Wait to maintain 60 frames per second (1/60 = 0.0167 seconds per frame)
    clock.tick(FPS)

# Clean up and exit pygame properly when the game loop ends
pygame.quit()
# Exit the Python program completely
sys.exit()