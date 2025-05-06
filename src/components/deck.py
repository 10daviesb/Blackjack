import os
from PIL import Image, ImageTk
import random

class Deck:
    def __init__(self, num_decks=8):
        self.num_decks = num_decks  # Number of decks in the shoe
        self.cards = self.create_shoe()
        self.card_images = self.load_card_images()
        self.shuffle()

    def create_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        return [(rank, suit) for suit in suits for rank in ranks]

    def create_shoe(self):
        # Combine multiple decks into a shoe
        shoe = []
        for _ in range(self.num_decks):
            shoe.extend(self.create_deck())
        return shoe

    def load_card_images(self):
        """
        Loads all card images and the back image into a dictionary.
        """
        card_images = {}
        base_path = os.path.join(os.path.dirname(__file__), "..", "assets", "cards")
        for rank, suit in self.create_deck():
            file_name = f"{rank}_of_{suit}.png".lower()
            file_path = os.path.join(base_path, file_name)
            card_images[(rank, suit)] = ImageTk.PhotoImage(Image.open(file_path).resize((100, 150)))
        card_images["back"] = ImageTk.PhotoImage(
            Image.open(os.path.join(base_path, "card_back.png")).resize((100, 150))
        )
        return card_images

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        if not self.cards:
            return None  # Return None if the deck is empty
        return self.cards.pop()

    def reshuffle(self):
        # Recreate and shuffle the shoe
        self.cards = self.create_shoe()
        self.shuffle()