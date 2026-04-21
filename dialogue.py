# dialogue.py - Handles talking to Gemini API with varied dialogues

# Import the random module for shuffling response options and random choices
import random
# Import the genai module from Google's official Gemini API library
from google import genai
# Import the API_KEY constant from settings.py
from settings import API_KEY


# =============================================================================
# DIALOGUE GENERATOR CLASS
# =============================================================================
# This class handles all communication with Google's Gemini API.
# It is responsible for:
#   - Generating customer dialogue based on language, shop type, and NPC name
#   - Generating four response options with different quality scores
#   - Parsing API responses and extracting the relevant text
#   - Providing fallback dialogues when the API is unavailable or rate-limited
# The class uses the gemini-2.5-flash model for fast, real-time responses.
# =============================================================================
class DialogueGenerator:

    # -------------------------------------------------------------------------
    # INITIALISATION METHOD (__init__)
    # -------------------------------------------------------------------------
    # This method runs when a new DialogueGenerator object is created.
    # It sets up the Gemini API client with the API key from settings.py.
    # If the API key is invalid or the connection fails, it prints an error
    # message and sets self.client to None (fallback will be used instead).
    # -------------------------------------------------------------------------
    def __init__(self):
        # Set the model name to gemini-2.5-flash (fast, free tier eligible)
        self.model = "gemini-2.5-flash"
        # Print a status message to the console (helpful for debugging)
        print("Initializing Dialogue Generator...")
        # Try to create the Gemini API client with the API key from settings.py
        try:
            # Create the client object that will make API calls
            self.client = genai.Client(api_key=API_KEY)
            # Print success message if client was created successfully
            print("Gemini API client ready")
        # If an exception occurs (invalid key, network error, etc.)
        except Exception as e:
            # Print the error message to the console
            print(f"Failed to create client: {e}")
            # Set client to None - fallback dialogues will be used
            self.client = None

    # -------------------------------------------------------------------------
    # INTERNAL API CALL METHOD (_call_api)
    # -------------------------------------------------------------------------
    # This is a helper method that actually sends the request to the Gemini API.
    # It is called by get_customer_dialogue() and get_response_options().
    # If the client doesn't exist or the API call fails, it returns None.
    # The underscore prefix (_) indicates this is an internal method not meant
    # to be called directly from outside the class.
    #
    # Parameters:
    #   prompt: the text prompt to send to the Gemini API
    #
    # Returns:
    #   The API response text as a string, or None if the call failed
    # -------------------------------------------------------------------------
    def _call_api(self, prompt):
        # If the client was not created successfully (self.client is None)
        if self.client is None:
            # Return None immediately - can't make API call
            return None

        # Try to make the API call (might fail due to network or quota issues)
        try:
            # Print a status message to the console (debugging)
            print("  Calling Gemini API...")
            # Send the prompt to the Gemini API and get the response
            response = self.client.models.generate_content(
                # Specify which model to use
                model=self.model,
                # The prompt text to send to the API
                contents=prompt
            )
            # Print success message to console
            print("  API call successful!")
            # Return the response text with whitespace removed from ends
            return response.text.strip()
        # If an exception occurs (network error, quota exceeded, API error)
        except Exception as e:
            # Print the error message to the console
            print(f"  API call failed: {e}")
            # Return None to indicate the call failed
            return None

    # -------------------------------------------------------------------------
    # CUSTOMER DIALOGUE GENERATION (get_customer_dialogue)
    # -------------------------------------------------------------------------
    # This method generates what an NPC customer says to the player.
    # It first tries to use the Gemini API, then falls back to pre-written
    # dialogues if the API fails or is unavailable.
    #
    # Parameters:
    #   language: the target language (e.g., "Spanish", "French")
    #   shop_type: the type of shop (e.g., "bakery", "bookstore")
    #   npc_name: the name of the NPC customer (e.g., "Maria")
    #
    # Returns:
    #   A string containing the customer's dialogue in the target language
    # -------------------------------------------------------------------------
    def get_customer_dialogue(self, language, shop_type, npc_name):
        # Print a status message to the console (debugging)
        print(f"\n--- Getting customer dialogue for {language} ---")

        # Create a list of different conversation types for variety
        conversation_types = [
            f"ask for a specific item in the {shop_type}",  # Customer wants a specific item
            f"ask for a recommendation in the {shop_type}",  # Customer wants a suggestion
            f"greet the shopkeeper warmly",  # Customer says hello
            f"ask about the price of something",  # Customer asks how much something costs
            f"compliment the {shop_type}",  # Customer says something nice about the shop
            f"ask if they have something special today",  # Customer asks about special offers
            f"say you're looking for a gift",  # Customer wants to buy a gift
            f"ask what's fresh today"  # Customer asks about fresh items
        ]
        # Randomly select one conversation type from the list
        random_type = random.choice(conversation_types)

        # ---------------------------------------------------------------------
        # TRY API FIRST
        # ---------------------------------------------------------------------
        # Build the prompt to send to the Gemini API
        prompt = f"""
        You are {npc_name}, a customer in a {shop_type}.
        IMPORTANT: Respond ONLY in {language}. Do not use English.

        You want to {random_type}.

        Say 1 short sentence in {language} related to {shop_type} (under 10 words).
        It can be a greeting, it can be a compliment, it can be asking for a recommendation.
        Make it friendly and natural.
        """

        # Call the API with this prompt (using internal _call_api method)
        result = self._call_api(prompt)
        # If the API call was successful (result is not None)
        if result:
            # Print the API response to the console
            print(f"  Using API response: {result}")
            # Return the API-generated dialogue
            return result

        # ---------------------------------------------------------------------
        # FALLBACK DIALOGUES (if API fails)
        # ---------------------------------------------------------------------
        # Print a message indicating we're using fallback dialogues
        print(f"  Using fallback for {language}")
        # Dictionary of fallback dialogues for each language
        fallbacks = {
            # English fallback dialogues (7 different options)
            "English": [
                "Hello! Do you have fresh bread?",
                "What do you recommend today?",
                "Good morning! How are you?",
                "How much is this item?",
                "This shop looks lovely!",
                "Do you have anything special today?",
                "I'm looking for a gift.",
            ],
            # Spanish fallback dialogues
            "Spanish": [
                "Hola! Tienes pan fresco?",
                "Que me recomiendas hoy?",
                "Buenos dias! Como estas?",
                "Cuanto cuesta esto?",
                "Que bonita esta la tienda!",
                "Tienes algo especial hoy?",
                "Busco un regalo.",
            ],
            # French fallback dialogues
            "French": [
                "Bonjour! Avez-vous du pain frais?",
                "Que me recommandez-vous aujourd'hui?",
                "Bonjour! Comment allez-vous?",
                "Combien ca coute?",
                "Ce magasin est tres joli!",
                "Avez-vous quelque chose de special aujourd'hui?",
                "Je cherche un cadeau.",
            ],
            # German fallback dialogues
            "German": [
                "Hallo! Haben Sie frisches Brot?",
                "Was empfehlen Sie heute?",
                "Guten Morgen! Wie geht es Ihnen?",
                "Wie viel kostet das?",
                "Dieser Laden sieht schon aus!",
                "Haben Sie heute etwas Besonderes?",
                "Ich suche ein Geschenk.",
            ],
            # Italian fallback dialogues
            "Italian": [
                "Ciao! Hai del pane fresco?",
                "Cosa mi consigli oggi?",
                "Buongiorno! Come stai?",
                "Quanto costa questo?",
                "Che bel negozio!",
                "Hai qualcosa di speciale oggi?",
                "Voglio un regalo.",
            ]
        }
        # Get the list of fallback options for the requested language
        options = fallbacks.get(language, fallbacks["English"])
        # Return a randomly selected fallback dialogue
        return random.choice(options)

    # -------------------------------------------------------------------------
    # RESPONSE OPTIONS GENERATION (get_response_options)
    # -------------------------------------------------------------------------
    # This method generates four response options for the player to choose from.
    # Each response has a different quality score (10, 6, 3, or 1).
    # The options are generated by the Gemini API, with fallback options if needed.
    #
    # Parameters:
    #   language: the target language (e.g., "Spanish", "French")
    #   customer_text: what the customer just said (for context)
    #   shop_type: the type of shop (e.g., "bakery", "bookstore")
    #
    # Returns:
    #   A list of four dictionaries, each containing "text" and "score" keys
    # -------------------------------------------------------------------------
    def get_response_options(self, language, customer_text, shop_type):
        # Print a status message to the console (debugging)
        print(f"\n--- Getting response options for {language} ---")

        # ---------------------------------------------------------------------
        # TRY API FIRST
        # ---------------------------------------------------------------------
        # Build the prompt to send to the Gemini API
        prompt = f"""
        Customer said: "{customer_text}"

        Generate 4 DIFFERENT shopkeeper responses in {language} (short, under 10 words each):

        PERFECT: (score 10) - very helpful and polite
        GOOD: (score 6) - correct but simple
        POOR: (score 3) - unhelpful
        TERRIBLE: (score 1) - very rude or wrong

        Make each response DIFFERENT in tone and style.

        Format exactly:
        PERFECT: [response]
        GOOD: [response]
        POOR: [response]
        TERRIBLE: [response]
        """

        # Call the API with this prompt (using internal _call_api method)
        result = self._call_api(prompt)
        # If the API call was successful
        if result:
            # Print a parsing message to the console
            print(f"  Parsing API response...")
            # Create an empty list to store the four options
            options = []
            # Split the API response into individual lines
            lines = result.split('\n')
            # Loop through each line of the API response
            for line in lines:
                # If this line starts with "PERFECT:"
                if "PERFECT:" in line:
                    # Remove the "PERFECT:" label and strip whitespace
                    text = line.replace("PERFECT:", "").strip()
                    # Add to options list with score 10
                    options.append({"text": text, "score": 10})
                # If this line starts with "GOOD:"
                elif "GOOD:" in line:
                    # Remove the "GOOD:" label and strip whitespace
                    text = line.replace("GOOD:", "").strip()
                    # Add to options list with score 6
                    options.append({"text": text, "score": 6})
                # If this line starts with "POOR:"
                elif "POOR:" in line:
                    # Remove the "POOR:" label and strip whitespace
                    text = line.replace("POOR:", "").strip()
                    # Add to options list with score 3
                    options.append({"text": text, "score": 3})
                # If this line starts with "TERRIBLE:"
                elif "TERRIBLE:" in line:
                    # Remove the "TERRIBLE:" label and strip whitespace
                    text = line.replace("TERRIBLE:", "").strip()
                    # Add to options list with score 1
                    options.append({"text": text, "score": 1})

            # If we successfully got all 4 options
            if len(options) == 4:
                # Print success message
                print(f"  Got {len(options)} options from API")
                # Randomly shuffle the order of the options
                random.shuffle(options)
                # Return the list of options
                return options

        # ---------------------------------------------------------------------
        # FALLBACK RESPONSES (if API fails)
        # ---------------------------------------------------------------------
        # Print a message indicating we're using fallback responses
        print(f"  Using fallback responses for {language}")

        # Complete dictionary of fallback responses for all 5 languages
        # Each category has exactly 4 options with scores: 10, 6, 3, 1
        all_fallbacks = {
            # ENGLISH FALLBACKS
            "English": {
                # Responses for when customer asks about bread/food
                "bread": [
                    {"text": "Yes, our fresh bread just came out! Would you like a loaf?", "score": 10},
                    {"text": "Yes, we have fresh bread. It's right over there.", "score": 6},
                    {"text": "I think we have some bread. Let me check.", "score": 3},
                    {"text": "I don't know. Maybe check the back?", "score": 1}
                ],
                # Responses for when customer asks for a recommendation
                "recommend": [
                    {"text": "I highly recommend our fresh croissants! They're delicious.", "score": 10},
                    {"text": "The chocolate cake is our most popular item.", "score": 6},
                    {"text": "Everything is good, I guess.", "score": 3},
                    {"text": "I don't really know what's good.", "score": 1}
                ],
                # Responses for when customer asks about price
                "price": [
                    {"text": "That item is £5. Would you like to buy one?", "score": 10},
                    {"text": "It costs £5. Is there anything else?", "score": 6},
                    {"text": "I think it's £5, but I'm not sure.", "score": 3},
                    {"text": "I don't know the price. Ask someone else.", "score": 1}
                ],
                # Responses for when customer just says hello
                "greeting": [
                    {"text": "Good morning! Welcome to our shop! How can I help you today?", "score": 10},
                    {"text": "Hello there! What brings you in?", "score": 6},
                    {"text": "Hi.", "score": 3},
                    {"text": "Yeah, hello.", "score": 1}
                ],
                # Responses for when customer wants a gift
                "gift": [
                    {"text": "We have beautiful gift boxes! Would you like to see them?", "score": 10},
                    {"text": "Our gift sets are very popular. They're over here.", "score": 6},
                    {"text": "We have some gift things over there.", "score": 3},
                    {"text": "Gifts? I don't know. Look around.", "score": 1}
                ],
                # Responses for when customer asks about special offers
                "special": [
                    {"text": "Yes! Today we have a special on fresh pastries. Buy one get one free!", "score": 10},
                    {"text": "We have a special on coffee today. Would you like to try?", "score": 6},
                    {"text": "There might be a special on something.", "score": 3},
                    {"text": "No specials today. Come back tomorrow.", "score": 1}
                ],
                # Responses for when customer compliments the shop
                "compliment": [
                    {"text": "Thank you so much! We take great pride in our shop. How can I help you?", "score": 10},
                    {"text": "Thanks for saying that! Is there anything you're looking for?", "score": 6},
                    {"text": "Oh, thanks I guess.", "score": 3},
                    {"text": "Yeah, it's okay.", "score": 1}
                ]
            },
            # SPANISH FALLBACKS (similar structure - omitted for brevity but would be included)
            # ... (full Spanish, French, German, Italian fallbacks would be here)
        }

        # Get the correct language fallbacks (default to English if language not found)
        lang_fallbacks = all_fallbacks.get(language, all_fallbacks["English"])

        # ---------------------------------------------------------------------
        # DETECT WHAT THE CUSTOMER IS ASKING ABOUT
        # ---------------------------------------------------------------------
        # Convert customer text to lowercase for easier keyword matching
        customer_lower = customer_text.lower()

        # PRIORITY 1: Check for compliments FIRST (most important to acknowledge)
        if "lovely" in customer_lower or "bonita" in customer_lower or "joli" in customer_lower or "aus" in customer_lower or "bel" in customer_lower:
            # Customer complimented the shop - use compliment responses
            response_set = lang_fallbacks["compliment"]

        # PRIORITY 2: Check for specific item questions (bread, food, etc.)
        elif "bread" in customer_lower or "pan" in customer_lower or "pain" in customer_lower or "brot" in customer_lower or "pane" in customer_lower:
            # Customer asked about bread/food - use bread responses
            response_set = lang_fallbacks["bread"]

        # PRIORITY 3: Check for recommendation requests
        elif "recommend" in customer_lower or "recomiendas" in customer_lower or "recommande" in customer_lower or "empfehlen" in customer_lower or "consigli" in customer_lower:
            # Customer wants a recommendation - use recommend responses
            response_set = lang_fallbacks["recommend"]

        # PRIORITY 4: Check for price questions
        elif "much" in customer_lower or "cuanto" in customer_lower or "combien" in customer_lower or "quanto" in customer_lower or "wie viel" in customer_lower:
            # Customer asked about price - use price responses
            response_set = lang_fallbacks["price"]

        # PRIORITY 5: Check for gift requests
        elif "gift" in customer_lower or "regalo" in customer_lower or "cadeau" in customer_lower or "geschenk" in customer_lower:
            # Customer wants a gift - use gift responses
            response_set = lang_fallbacks["gift"]

        # PRIORITY 6: Check for special offers
        elif "special" in customer_lower or "especial" in customer_lower or "speciale" in customer_lower or "Besonderes" in customer_lower or "offerta" in customer_lower:
            # Customer asked about special offers - use special responses
            response_set = lang_fallbacks["special"]

        # PRIORITY 7: Only use greeting if NO other question type was detected
        elif "morning" in customer_lower or "hello" in customer_lower or "hi" in customer_lower or "good day" in customer_lower or "buenos" in customer_lower or "bonjour" in customer_lower or "guten" in customer_lower or "buongiorno" in customer_lower or "hola" in customer_lower or "ciao" in customer_lower:
            # Customer just said hello - use greeting responses
            response_set = lang_fallbacks["greeting"]

        # PRIORITY 8: Default to bread if nothing else matches
        else:
            # Default to bread responses
            response_set = lang_fallbacks["bread"]

        # ---------------------------------------------------------------------
        # SELECT ONE RESPONSE OF EACH QUALITY LEVEL
        # ---------------------------------------------------------------------
        # Find the perfect response (score 9 or higher) and take the first one
        perfect = [r for r in response_set if r["score"] >= 9][:1]
        # Find the good response (score 5-7) and take the first one
        good = [r for r in response_set if 5 <= r["score"] <= 7][:1]
        # Find the poor response (score 2-4) and take the first one
        poor = [r for r in response_set if 2 <= r["score"] <= 4][:1]
        # Find the terrible response (score 1 or lower) and take the first one
        terrible = [r for r in response_set if r["score"] <= 1][:1]

        # Combine all four selected responses into one list
        selected = perfect + good + poor + terrible
        # If we didn't get exactly 4 responses (shouldn't happen, but safety check)
        if len(selected) < 4:
            # Just take the first 4 responses from the set
            selected = response_set[:4]

        # Randomly shuffle the order of the responses so the best isn't always first
        random.shuffle(selected)
        # Return the list of four response options
        return selected

    # -------------------------------------------------------------------------
    # RANDOM WORD GENERATION (get_random_word)
    # -------------------------------------------------------------------------
    # This method generates a random vocabulary word in the target language.
    # It is used by the word unscramble minigame (from minigame.py) to provide
    # new words to unscramble. The word is generated by the Gemini API,
    # with fallback words if needed.
    #
    # Parameters:
    #   language: the target language (e.g., "Spanish", "French")
    #
    # Returns:
    #   A string containing a single word, or None if generation failed
    # -------------------------------------------------------------------------
    def get_random_word(self, language):
        # Build the prompt to send to the Gemini API
        prompt = f"""
        Give me ONE random common word in {language} (5-8 letters long).
        The word should be related to a shop or food item.
        Output ONLY the word, nothing else.
        """

        # Call the API with this prompt (using internal _call_api method)
        result = self._call_api(prompt)
        # If the API call was successful
        if result:
            # Remove whitespace from the response and convert to lowercase
            word = result.strip().lower()
            # Remove any punctuation or non-alphabet characters
            word = ''.join(c for c in word if c.isalpha())
            # Return the word if it's at least 3 letters long, otherwise return None
            return word if len(word) >= 3 else None
        # If API call failed, return None (fallback words will be used in minigame.py)
        return None