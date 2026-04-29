# settings.py - Just colors and sizes

# Import pygame (required for some colour operations, though not strictly needed)
import pygame


# =============================================================================
# GAME WINDOW SETTINGS
# =============================================================================
# These settings control the size and frame rate of the game window.
# They are imported and used by main.py and other files.

# Screen width in pixels (1024 x 768 is a common 4:3 resolution)
WIDTH = 1024
# Screen height in pixels
HEIGHT = 768
# Frames per second (how many times the game updates per second)
# This value is used in main.py with clock.tick(FPS)
FPS = 60


# =============================================================================
# COLOUR CONSTANTS
# =============================================================================
# All colours are defined using RGB (Red, Green, Blue) values.
# Each value ranges from 0 to 255.
# These colours are imported and used by main.py, player.py, npc.py, etc.

# White - used for text on dark backgrounds
WHITE = (255, 255, 255)
# Black - used for borders, outlines, and text on light backgrounds
BLACK = (0, 0, 0)
# Gray - used for disabled elements and shadows
GRAY = (128, 128, 128)
# Light Blue - used for buttons and the player character (from player.py)
LIGHT_BLUE = (173, 216, 230)
# Green - used for success messages, correct answers, and start buttons
GREEN = (0, 255, 0)
# Brown - used for the shop counter, shelves, and wooden elements (in main.py)
BROWN = (139, 69, 19)
# Orange - used for warnings and highlight text
ORANGE = (255, 165, 0)


# =============================================================================
# API CONFIGURATION
# =============================================================================
# This API key is used by dialogue.py to authenticate with Google's Gemini API.
# The free tier allows 20 requests per day (15 per minute).
# Two keys are provided (one commented out) for manual switching if quota is exceeded.
# To switch keys, comment out the current key and uncomment the backup key.

# Primary Gemini API Key
API_KEY = "AIzaSyDt4GYLHsd21fTuPaEds_fkO0MNp7YBrlo"

# Backup API key (commented out - uncomment to use if primary key quota is exhausted)
# API_KEY = "AIzaSyCR5MSBSkmgVl1iKBdF1beaWkdOeQ0kbOU"
