# minigame.py - Word Unscramble Minigame

# Import pygame for drawing and input handling
import pygame
# Import random for scrambling letters and selecting fallback words
import random
# Import all constants from settings.py
from settings import *
# Import the Button class from button.py (used for button rectangles)
from button import Button


# =============================================================================
# UNSCRAMBLE GAME CLASS
# =============================================================================
# This class manages the word unscramble minigame.
# The player is shown a scrambled word and must type the correct unscrambled version.
# Features:
#   - Generates random words using the Gemini API (via dialogue.py)
#   - Scrambles letters randomly while ensuring it's different from original
#   - Tracks score (10 points per correct answer)
#   - Ends game when player gets a word wrong
#   - Shows "Game Over" screen with final score
# This class is used by main.py when the player clicks the Minigame button.
# =============================================================================
class UnscrambleGame:

    # -------------------------------------------------------------------------
    # INITIALISATION METHOD (__init__)
    # -------------------------------------------------------------------------
    # This method runs when a new UnscrambleGame object is created.
    # It is called from main.py when the Minigame button is clicked.
    # It sets up all the game state variables but does not start the game.
    #
    # Parameters:
    #   language: the target language for vocabulary words (from main.py)
    #   dialogue_gen: the DialogueGenerator object from dialogue.py for API calls
    # -------------------------------------------------------------------------
    def __init__(self, language, dialogue_gen):
        # Store the target language (e.g., "Spanish")
        self.language = language
        # Store the dialogue generator (from dialogue.py for API calls)
        self.dialogue_gen = dialogue_gen
        # Set active to False (game hasn't started yet)
        self.active = False
        # Store the current word (the correct unscrambled word)
        self.current_word = ""
        # Store the scrambled version of the current word
        self.scrambled_word = ""
        # Store what the player has typed so far
        self.player_input = ""
        # Store the player's current score
        self.score = 0
        # Store any message to display (e.g., "Correct! +10 points!")
        self.message = ""
        # Set message colour to green (for correct answers)
        self.message_color = (0, 255, 0)
        # Set game_over to False (game is still active)
        self.game_over = False

    # -------------------------------------------------------------------------
    # START GAME METHOD (start_game)
    # -------------------------------------------------------------------------
    # This method starts a new game of word unscramble.
    # It is called from main.py after creating the UnscrambleGame object.
    # It resets all game state variables and gets the first word.
    # -------------------------------------------------------------------------
    def start_game(self):
        # Set active to True (game is now running)
        self.active = True
        # Set game_over to False (player hasn't lost yet)
        self.game_over = False
        # Reset score to 0
        self.score = 0
        # Clear the player's input
        self.player_input = ""
        # Clear any existing message
        self.message = ""
        # Get the first word from API (calls get_random_word() from dialogue.py) or fallback
        self.next_word()

    # -------------------------------------------------------------------------
    # NEXT WORD METHOD (next_word)
    # -------------------------------------------------------------------------
    # This method gets a new word from the API (or fallback list).
    # It calls get_random_word() from dialogue.py to generate a word.
    # It scrambles the word and prepares for the next round.
    # If the game is over, this method does nothing.
    # -------------------------------------------------------------------------
    def next_word(self):
        # If the game is already over, don't get a new word
        if self.game_over:
            return

        # Try to get a word from the Gemini API (calls get_random_word() in dialogue.py)
        word = self.dialogue_gen.get_random_word(self.language)
        # If API returned a valid word
        if word:
            # Store the word in lowercase
            self.current_word = word.lower()
            # Scramble the letters of the word (calls scramble_word method)
            self.scrambled_word = self.scramble_word(self.current_word)
            # Clear the player's input
            self.player_input = ""
            # Clear any existing message
            self.message = ""
        else:
            # API failed - use fallback word list (pre-defined words)
            fallback_words = {
                # English fallback words (food and shop related)
                "English": ["bread", "coffee", "apple", "cheese", "milk", "sugar", "flour", "butter"],
                # Spanish fallback words
                "Spanish": ["pan", "cafe", "manzana", "queso", "leche", "azucar", "harina", "mantequilla"],
                # French fallback words
                "French": ["pain", "cafe", "pomme", "fromage", "lait", "sucre", "farine", "beurre"],
                # German fallback words
                "German": ["brot", "kaffee", "apfel", "kase", "milch", "zucker", "mehl", "butter"],
                # Italian fallback words
                "Italian": ["pane", "caffe", "mela", "formaggio", "latte", "zucchero", "farina", "burro"]
            }
            # Get the list for the current language (default to English)
            words = fallback_words.get(self.language, fallback_words["English"])
            # Pick a random word from the fallback list
            self.current_word = random.choice(words)
            # Scramble the letters of the word (calls scramble_word method)
            self.scrambled_word = self.scramble_word(self.current_word)
            # Clear the player's input
            self.player_input = ""
            # Clear any existing message
            self.message = ""

    # -------------------------------------------------------------------------
    # SCRAMBLE WORD METHOD (scramble_word)
    # -------------------------------------------------------------------------
    # This method takes a word and scrambles its letters randomly.
    # It uses random.shuffle() to rearrange the letters.
    # If the scrambled word is identical to the original (rare), it swaps the
    # first two letters to ensure it's actually scrambled.
    #
    # Parameters:
    #   word: the word to scramble
    #
    # Returns:
    #   A string containing the scrambled word
    # -------------------------------------------------------------------------
    def scramble_word(self, word):
        # Convert the word into a list of individual letters
        letters = list(word)
        # Randomly shuffle the order of the letters
        random.shuffle(letters)
        # Join the shuffled letters back into a string
        scrambled = ''.join(letters)
        # If the scrambled word is identical to the original AND word has >1 letter
        if scrambled == word and len(word) > 1:
            # Swap the first and second letters to make it different
            letters[0], letters[1] = letters[1], letters[0]
            # Join the letters back into a string
            scrambled = ''.join(letters)
        # Return the scrambled word
        return scrambled

    # -------------------------------------------------------------------------
    # CHECK ANSWER METHOD (check_answer)
    # -------------------------------------------------------------------------
    # This method checks if the player's typed answer is correct.
    # If correct: adds 10 points, shows success message, gets next word
    # If wrong: ends the game, shows "Game Over" and reveals the correct word
    # This method is called from main.py when the player submits an answer.
    #
    # Returns:
    #   True if answer was correct, False if wrong
    # -------------------------------------------------------------------------
    def check_answer(self):
        # Compare player's input (lowercase, no spaces) with the current word
        if self.player_input.lower().strip() == self.current_word:
            # CORRECT ANSWER
            # Add 10 points to the player's score
            self.score += 10
            # Set success message
            self.message = "Correct! +10 points!"
            # Set message colour to green
            self.message_color = (0, 255, 0)
            # Get the next word (calls next_word method which continues game)
            self.next_word()
            # Return True to indicate correct answer
            return True
        else:
            # WRONG ANSWER - GAME OVER
            # Set game over message showing the correct word
            self.message = f"Game Over! The word was: {self.current_word}"
            # Set message colour to red
            self.message_color = (255, 0, 0)
            # Set active to False (game no longer active)
            self.active = False
            # Set game_over to True
            self.game_over = True
            # Return False to indicate wrong answer
            return False

    # -------------------------------------------------------------------------
    # GET BUTTON RECTS METHOD (get_button_rects)
    # -------------------------------------------------------------------------
    # This method returns the rectangle areas of the submit and quit buttons.
    # These rectangles are used for mouse click detection in the main game loop
    # in main.py. The buttons themselves are drawn by this class, but click
    # detection is handled by main.py using these rectangles.
    #
    # Returns:
    #   A tuple containing (submit_button_rect, quit_button_rect)
    # -------------------------------------------------------------------------
    def get_button_rects(self):
        # Create a temporary submit button using Button class from button.py
        # This is only to get the rectangle area, not to draw the button
        submit_btn = Button(WIDTH // 2 - 100, 480, 200, 50, "Submit Answer", (100, 200, 100))
        # Create a temporary quit button using Button class from button.py
        quit_btn = Button(WIDTH // 2 - 100, 550, 200, 50, "Back to Shop", (173, 216, 230))
        # Return both rectangles as a tuple (used by main.py for click detection)
        return submit_btn.rect, quit_btn.rect

    # -------------------------------------------------------------------------
    # DRAW METHOD (draw)
    # -------------------------------------------------------------------------
    # This method draws the entire minigame screen.
    # It is called from the draw() method in main.py.
    # It draws:
    #   - Title panel with "Word Unscramble"
    #   - Current score display
    #   - Either the active game screen OR the game over screen
    #   - Message (correct/incorrect feedback)
    #   - Submit button (only if game is active)
    #   - Quit button (always visible)
    #
    # Parameters:
    #   screen: the pygame screen surface to draw on (from main.py)
    #   font: normal font (36px) from main.py
    #   small_font: small font (24px) from main.py
    #   big_font: big font (48px) from main.py
    # -------------------------------------------------------------------------
    def draw(self, screen, font, small_font, big_font):
        # Fill the entire screen with dark blue-grey colour
        screen.fill((50, 50, 80))

        # Draw the title panel (brown rectangle at top)
        title_bg = pygame.Rect(50, 30, WIDTH - 100, 60)
        pygame.draw.rect(screen, (80, 60, 40), title_bg)
        pygame.draw.rect(screen, (120, 90, 60), title_bg, 2)
        # Render and draw the "Word Unscramble" title
        title = big_font.render("Word Unscramble", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 45))

        # Draw the score display in gold colour at top right
        score_text = font.render(f"Score: {self.score}", True, (255, 215, 0))
        screen.blit(score_text, (WIDTH - 150, 45))

        # ---------------------------------------------------------------------
        # GAME OVER SCREEN
        # ---------------------------------------------------------------------
        if self.game_over and not self.active:
            # Draw "GAME OVER" in large red text
            game_over_text = big_font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 200))
            # Draw final score text in white
            final_score_text = font.render(f"Final Score: {self.score}", True, WHITE)
            screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, 280))

        # ---------------------------------------------------------------------
        # ACTIVE GAME SCREEN
        # ---------------------------------------------------------------------
        else:
            # Draw the white background box for the scrambled word
            word_bg = pygame.Rect(WIDTH // 2 - 200, 150, 400, 80)
            pygame.draw.rect(screen, (240, 240, 255), word_bg)
            pygame.draw.rect(screen, BLACK, word_bg, 3)
            # Render and draw the scrambled word in large text
            scrambled_text = big_font.render(self.scrambled_word.upper(), True, (80, 60, 40))
            screen.blit(scrambled_text, (WIDTH // 2 - scrambled_text.get_width() // 2, 165))

            # Draw instruction text
            inst_text = font.render(f"Unscramble the word in {self.language}:", True, WHITE)
            screen.blit(inst_text, (WIDTH // 2 - inst_text.get_width() // 2, 270))

            # Draw the white input box for player's answer
            input_bg = pygame.Rect(WIDTH // 2 - 200, 320, 400, 50)
            pygame.draw.rect(screen, WHITE, input_bg)
            pygame.draw.rect(screen, BLACK, input_bg, 2)

            # Draw the player's typed input centred in the box
            input_surface = font.render(self.player_input, True, BLACK)
            screen.blit(input_surface, (WIDTH // 2 - input_surface.get_width() // 2, 332))

            # Draw a blinking cursor (alternates every 500 milliseconds)
            if (pygame.time.get_ticks() // 500) % 2:
                cursor_x = WIDTH // 2 + input_surface.get_width() // 2 + 5
                cursor_y = 332
                pygame.draw.line(screen, BLACK, (cursor_x, cursor_y), (cursor_x, cursor_y + 30), 2)

        # ---------------------------------------------------------------------
        # MESSAGE DISPLAY
        # ---------------------------------------------------------------------
        # Draw any message (e.g., "Correct! +10 points!") centred on screen
        if self.message:
            msg_text = font.render(self.message, True, self.message_color)
            screen.blit(msg_text, (WIDTH // 2 - msg_text.get_width() // 2, 400))

        # ---------------------------------------------------------------------
        # SUBMIT BUTTON (only if game is active)
        # ---------------------------------------------------------------------
        if not self.game_over and self.active:
            # Draw the submit button rectangle
            submit_rect = pygame.Rect(WIDTH // 2 - 100, 480, 200, 50)
            pygame.draw.rect(screen, (100, 200, 100), submit_rect)
            pygame.draw.rect(screen, BLACK, submit_rect, 2)
            # Draw the "Submit Answer" text on the button
            submit_text = small_font.render("Submit Answer", True, BLACK)
            submit_text_rect = submit_text.get_rect(center=submit_rect.center)
            screen.blit(submit_text, submit_text_rect)

        # ---------------------------------------------------------------------
        # QUIT BUTTON (always visible)
        # ---------------------------------------------------------------------
        # Draw the quit button rectangle
        quit_rect = pygame.Rect(WIDTH // 2 - 100, 550, 200, 50)
        pygame.draw.rect(screen, (173, 216, 230), quit_rect)
        pygame.draw.rect(screen, BLACK, quit_rect, 2)
        # Draw the "Back to Shop" text on the button
        quit_text = small_font.render("Back to Shop", True, BLACK)
        quit_text_rect = quit_text.get_rect(center=quit_rect.center)
        screen.blit(quit_text, quit_text_rect)