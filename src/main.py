import tkinter as tk
from tkinter import Toplevel, Scale
from components.deck import Deck
from components.hand import Hand
import time
import pygame  # For playing sound effects

class BlackjackGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Blackjack Game")
        self.master.geometry("800x700")

        # Set the window icon
        self.master.iconbitmap("src/assets/msc/icon.ico")

        # Initialize balance, bet, and insurance
        self.balance = 1000  # Starting balance
        self.bet = 0  # Current bet
        self.insurance_bet = 0  # Insurance bet

        # Variables for splitting
        self.second_hand = None
        self.second_hand_bet = 0
        self.playing_second_hand = False

        # Initialize pygame mixer for sound effects
        pygame.mixer.init()
        self.card_draw_sound = pygame.mixer.Sound("src/assets/sounds/card_draw.wav")
        self.card_draw_sound.set_volume(0.2)  # Default volume (20%)

        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()

        self.setup_ui()

    def setup_ui(self):
        # Setup menu bar
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        # Add "Game" menu
        game_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="Start Game", command=self.start_game)

        # Add "Settings" menu
        settings_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Volume", command=self.open_settings)

        # Setup canvas for cards
        self.canvas = tk.Canvas(self.master, width=800, height=400, bg='green')
        self.canvas.pack()

        # Initialize the deck image (card back)
        self.deck_image = self.deck.card_images["back"]  # Ensure this is set correctly

        # Frame for betting and balance
        betting_frame = tk.Frame(self.master)
        betting_frame.pack(pady=10)

        # Balance label
        self.balance_label = tk.Label(betting_frame, text=f"Balance: {self.balance}", font=("Arial", 14))
        self.balance_label.pack(side=tk.LEFT, padx=10)

        # Bet entry
        self.bet_entry = tk.Entry(betting_frame, width=10)
        self.bet_entry.pack(side=tk.LEFT, padx=10)

        # Place Bet button
        self.place_bet_button = tk.Button(betting_frame, text="Place Bet", command=self.place_bet)
        self.place_bet_button.pack(side=tk.LEFT, padx=10)

        # Frame for action buttons
        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=10)
        
        # Add Hit, Stand, and Fold buttons (centered)
        self.hit_button = tk.Button(button_frame, text="Hit", command=self.hit, state=tk.DISABLED)
        self.hit_button.pack(side=tk.LEFT, padx=10)
        
        self.stand_button = tk.Button(button_frame, text="Stand", command=self.stand, state=tk.DISABLED)
        self.stand_button.pack(side=tk.LEFT, padx=10)
        
        self.fold_button = tk.Button(button_frame, text="Fold", command=self.fold, state=tk.DISABLED)
        self.fold_button.pack(side=tk.LEFT, padx=10)
        
        # Create a new frame for the Insurance and Split buttons
        bottom_button_frame = tk.Frame(self.master)
        bottom_button_frame.pack(pady=10)
        
        # Add Insurance button
        self.insurance_button = tk.Button(bottom_button_frame, text="Insurance", command=self.place_insurance, state=tk.DISABLED)
        self.insurance_button.pack(side=tk.LEFT, padx=10)
        
        # Add Split button
        self.split_button = tk.Button(bottom_button_frame, text="Split", command=self.split_hand, state=tk.DISABLED)
        self.split_button.pack(side=tk.LEFT, padx=10)


        # Frame for totals
        totals_frame = tk.Frame(self.master)
        totals_frame.pack(pady=10)

        # Label to display the player's total (centered)
        self.player_total_label = tk.Label(totals_frame, text="Player Total: 0", font=("Arial", 14))
        self.player_total_label.pack()

        # Label to display the dealer's total (centered)
        self.dealer_total_label = tk.Label(totals_frame, text="Dealer Total: ?", font=("Arial", 14))
        self.dealer_total_label.pack()

        # Label to display game messages (centered)
        self.message_label = tk.Label(self.master, text="", font=("Arial", 14), fg="red")
        self.message_label.pack(pady=10)

    def open_settings(self):
        """
        Opens a settings window with a volume slider.
        """
        settings_window = Toplevel(self.master)
        settings_window.title("Settings")
        settings_window.geometry("300x100")

        # Set the icon for the settings window
        settings_window.iconbitmap("src/assets/msc/icon.ico")

        tk.Label(settings_window, text="Volume", font=("Arial", 12)).pack(pady=5)

        # Volume slider
        volume_slider = Scale(
            settings_window,
            from_=0,
            to=100,
            orient="horizontal",
            command=self.set_volume
        )
        volume_slider.set(int(self.card_draw_sound.get_volume() * 100))  # Set slider to current volume
        volume_slider.pack()

    def set_volume(self, volume):
        """
        Sets the volume for the card draw sound effect.
        """
        self.card_draw_sound.set_volume(int(volume) / 100)

    def draw_card_with_reshuffle(self):
        """
        Draws a card from the deck. If the deck is empty, reshuffles the shoe and continues.
        """
        card = self.deck.draw_card()
        if card is None:  # Deck is empty
            self.message_label.config(text="Deck is empty! Reshuffling...")
            self.master.update()  # Update the UI to show the reshuffle message
            self.deck.reshuffle()
            card = self.deck.draw_card()  # Draw a card after reshuffling
        return card

    def start_game(self):
        self.deck.shuffle()

        # Reset hands and UI
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.canvas.delete("all")
        self.canvas.create_image(50, 200, image=self.deck_image, anchor=tk.NW)
        self.message_label.config(text="")
        self.player_total_label.config(text="Player Total: 0")
        self.dealer_total_label.config(text="Dealer Total: ?")

        # Deal cards like real blackjack
        player_card1 = self.draw_card_with_reshuffle()
        self.animate_card(player_card1, (50, 200), (200, 300), overlap_offset=0)  # Player's first card
        self.player_hand.add_card(player_card1)

        dealer_card1 = self.draw_card_with_reshuffle()
        self.animate_card(dealer_card1, (50, 200), (200, 100), overlap_offset=0)  # Dealer's first card
        self.dealer_hand.add_card(dealer_card1)

        player_card2 = self.draw_card_with_reshuffle()
        self.animate_card(player_card2, (50, 200), (200, 300), overlap_offset=50)  # Player's second card
        self.player_hand.add_card(player_card2)

        dealer_card2 = self.draw_card_with_reshuffle()
        self.animate_card("back", (50, 200), (200, 100), overlap_offset=50)  # Dealer's second card (face down)
        self.dealer_hand.add_card(dealer_card2)  # Add the face-down card to the dealer's hand

        # Update player's total
        self.update_player_total()

        # Check if the dealer's face-up card is an Ace
        if dealer_card1[0] == "Ace":
            self.message_label.config(text="Dealer shows an Ace! Place insurance?")
            self.insurance_button.config(state=tk.NORMAL)  # Enable the insurance button

        # Enable Split button if the first two cards are of the same rank
        if self.player_hand.cards[0][0] == self.player_hand.cards[1][0]:
            self.split_button.config(state=tk.NORMAL)

        # Enable Hit, Stand, and Fold buttons
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        self.fold_button.config(state=tk.NORMAL)

    def animate_card(self, card, start_pos, end_pos, overlap_offset=50):
        """
        Animates a card moving from start_pos to end_pos on the canvas.

        Args:
            card (tuple or str): The card to animate (e.g., ('Ace', 'Spades')) or "back" for face-down.
            start_pos (tuple): Starting position (x, y) of the card.
            end_pos (tuple): Ending position (x, y) of the card.
            overlap_offset (int): Offset for overlapping cards within the same hand.
        """
        # Play the card draw sound effect
        self.card_draw_sound.play()

        # Adjust the end position for overlapping cards
        end_pos = (end_pos[0] + overlap_offset, end_pos[1])

        card_image = self.deck.card_images[card]
        card_id = self.canvas.create_image(start_pos[0], start_pos[1], image=card_image, anchor=tk.NW)

        # Animation loop
        steps = 20
        dx = (end_pos[0] - start_pos[0]) / steps
        dy = (end_pos[1] - start_pos[1]) / steps

        for i in range(steps):
            self.canvas.move(card_id, dx, dy)
            self.master.update()
            time.sleep(0.02)  # 20ms delay for smooth animation

        # Keep a reference to the card image to prevent garbage collection
        if end_pos[1] > 200:  # Player's hand
            self.player_card_image = card_image
        else:  # Dealer's hand
            self.dealer_card_image = card_image

    def hit(self):
        """
        Player chooses to draw another card.
        """
        new_card = self.draw_card_with_reshuffle()

        if self.playing_second_hand:
            # Hits for the second hand (offset by 25px)
            x_offset = 150 + len(self.second_hand.cards) * 50  # Offset for new card
            self.animate_card(new_card, (50, 200), (x_offset, 325))  # Push down by 25px
            self.second_hand.add_card(new_card)
        else:
            # Hits for the first hand
            x_offset = 150 + len(self.player_hand.cards) * 50  # Offset for new card
            self.animate_card(new_card, (50, 200), (x_offset, 300))
            self.player_hand.add_card(new_card)

        # Update player's total and check for bust
        self.update_player_total()
        if self.calculate_hand_total(self.player_hand if not self.playing_second_hand else self.second_hand) > 21:
            self.declare_bust()

    def stand(self):
        """
        Player chooses to stand. Dealer reveals the face-down card and plays.
        """
        if self.playing_second_hand:
            # Finish the second hand and proceed to the dealer's turn
            self.playing_second_hand = False
            self.message_label.config(text="Now playing the dealer's turn.")
        elif self.second_hand:
            # Switch to the second hand
            self.playing_second_hand = True
            self.player_hand = self.second_hand
            self.second_hand = None
            self.message_label.config(text="Now playing your second hand.")
            self.update_player_total()
            return

        # Reveal dealer's face-down card
        face_down_card = self.dealer_hand.cards[1]
        self.animate_card(face_down_card, (250, 100), (250, 100), overlap_offset=0)  # Adjusted for overlap

        # Update dealer's total immediately after revealing the card
        self.update_dealer_total()

        # Dealer's turn: follow standard casino rules
        while self.calculate_hand_total(self.dealer_hand) < 17:
            new_card = self.draw_card_with_reshuffle()
            x_offset = 150 + len(self.dealer_hand.cards) * 50  # Offset for new card
            self.animate_card(new_card, (50, 200), (x_offset, 100))
            self.dealer_hand.add_card(new_card)
            self.update_dealer_total()

        # Determine the winner for both hands
        self.determine_winner()

        # Disable buttons after the game ends
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.fold_button.config(state=tk.DISABLED)

    def fold(self):
        """
        Player chooses to fold. End the game.
        """
        # Disable buttons after folding
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.fold_button.config(state=tk.DISABLED)

        # Display a message or reset the game
        self.message_label.config(text="Player folded. Game over.")

    def update_player_total(self):
        """
        Updates the player's total and displays it.
        """
        total = self.calculate_hand_total(self.player_hand)
        self.player_total_label.config(text=f"Player Total: {total}")

    def update_dealer_total(self):
        """
        Updates the dealer's total and displays it.
        """
        total = self.calculate_hand_total(self.dealer_hand)
        self.dealer_total_label.config(text=f"Dealer Total: {total}")

    def calculate_hand_total(self, hand):
        """
        Calculates the total value of a hand.

        Args:
            hand (Hand): The hand to calculate the total for.

        Returns:
            int: The total value of the hand.
        """
        total = 0
        aces = 0
        for card in hand.cards:
            rank, _ = card
            if rank in ['Jack', 'Queen', 'King']:
                total += 10
            elif rank == 'Ace':
                aces += 1
                total += 11  # Count Ace as 11 initially
            else:
                total += int(rank)

        # Adjust for Aces if total exceeds 21
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total

    def declare_bust(self):
        """
        Declares the player has busted and transitions to the next hand or dealer's turn.
        """
        self.message_label.config(text="Bust! You went over 21.")
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.fold_button.config(state=tk.DISABLED)

        if self.playing_second_hand:
            # Finish the second hand and proceed to the dealer's turn
            self.playing_second_hand = False
            self.message_label.config(text="Now playing the dealer's turn.")
            self.stand()  # Transition to the dealer's turn
        elif self.second_hand:
            # Switch to the second hand
            self.playing_second_hand = True
            self.player_hand = self.second_hand
            self.second_hand = None
            self.message_label.config(text="Now playing your second hand.")
            self.update_player_total()
            self.hit_button.config(state=tk.NORMAL)
            self.stand_button.config(state=tk.NORMAL)

    def determine_winner(self):
        """
        Determines the winner of the game and displays the result.
        """
        def resolve_hand(hand, bet, hand_name):
            player_total = self.calculate_hand_total(hand)
            dealer_total = self.calculate_hand_total(self.dealer_hand)

            if dealer_total > 21:
                result = f"{hand_name}: Dealer busts! You win!"
                self.balance += bet * 2  # Player wins double the bet
            elif player_total > dealer_total:
                result = f"{hand_name}: You win!"
                self.balance += bet * 2  # Player wins double the bet
            elif player_total < dealer_total:
                result = f"{hand_name}: Dealer wins!"
                # Player loses the bet (balance already deducted)
            else:
                result = f"{hand_name}: It's a tie!"
                self.balance += bet  # Return the bet on a tie

            return result

        # Resolve the first hand
        first_hand_result = resolve_hand(self.player_hand, self.bet, "First Hand")

        # Resolve the second hand if it exists
        second_hand_result = ""
        if self.second_hand:
            second_hand_result = resolve_hand(self.second_hand, self.second_hand_bet, "Second Hand")

        # Display results
        self.message_label.config(text=f"{first_hand_result}\n{second_hand_result}")

        # Update balance label
        self.balance_label.config(text=f"Balance: {self.balance}")

    def place_bet(self):
        """
        Places a bet and updates the balance.
        """
        try:
            bet = int(self.bet_entry.get())
            if bet <= 0:
                self.message_label.config(text="Bet must be greater than 0.")
                return
            if bet > self.balance:
                self.message_label.config(text="Insufficient balance!")
                return

            self.bet = bet
            self.balance -= bet
            self.balance_label.config(text=f"Balance: {self.balance}")
            self.message_label.config(text=f"Bet placed: {self.bet}")
            self.start_game()  # Start the game after placing the bet
        except ValueError:
            self.message_label.config(text="Invalid bet amount.")

    def place_insurance(self):
        """
        Allows the player to place an insurance bet.
        """
        try:
            insurance_bet = self.bet // 2  # Insurance bet is up to half of the original bet
            if insurance_bet > self.balance:
                self.message_label.config(text="Insufficient balance for insurance!")
                return

            self.insurance_bet = insurance_bet
            self.balance -= insurance_bet
            self.balance_label.config(text=f"Balance: {self.balance}")
            self.message_label.config(text=f"Insurance bet placed: {self.insurance_bet}")
            self.insurance_button.config(state=tk.DISABLED)  # Disable the button after placing the bet
        except ValueError:
            self.message_label.config(text="Error placing insurance bet.")

    def split_hand(self):
        """
        Splits the player's hand into two hands if the first two cards are of the same rank.
        """
        if self.player_hand.cards[0][0] != self.player_hand.cards[1][0]:
            self.message_label.config(text="Cannot split: Cards must be of the same rank.")
            return

        if self.bet > self.balance:
            self.message_label.config(text="Insufficient balance to split!")
            return

        # Deduct the bet for the second hand
        self.second_hand_bet = self.bet
        self.balance -= self.second_hand_bet
        self.balance_label.config(text=f"Balance: {self.balance}")

        # Create the second hand
        self.second_hand = Hand()
        split_card = self.player_hand.cards.pop()  # Move one card to the second hand
        self.second_hand.add_card(split_card)

        # Animate the split card to the second hand's position (pushed down by 25px)
        self.animate_card(split_card, (300, 300), (200, 325), overlap_offset=50)

        # Update the UI
        self.message_label.config(text="Hand split! Play your first hand.")
        self.split_button.config(state=tk.DISABLED)  # Disable the split button
        self.update_player_total()

if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()