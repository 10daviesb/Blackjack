# 🃏 Blackjack Game

![Build Status](https://img.shields.io/github/actions/workflow/status/10daviesb/Blackjack/main.yml?branch=main)
![License](https://img.shields.io/github/license/10daviesb/Blackjack)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)

A Python-based Blackjack game with a graphical user interface (GUI) built using `tkinter`. The game includes features like betting, splitting hands, insurance, and animations for card movements.

## 🎮 Overview
This project is an interactive GUI Blackjack game. The game allows users to play against a dealer, with a focus on an engaging user interface and smooth animations for drawing cards.

## 📂 Project Structure
```
blackjack-game
├── src
│   ├── main.py          # 🎯 Entry point of the application
│   ├── assets           # 🎨 Contains assets for the game
│   │   ├── cards        # 🃏 Image files for playing cards
│   │   ├── sounds       # 🔊 Sound effects for the game
│   │   └── styles       # 🎨 Style files for the user interface
│   └── components       # 🛠️ Contains game logic components
│       ├── deck.py      # 🃏 Manages the deck of cards
│       ├── hand.py      # ✋ Represents player's and dealer's hands
│       └── animations.py # 🎥 Handles animations for card draws
├── requirements.txt     # 📦 Lists dependencies for the project
├── README.md            # 📖 Documentation for the project
└── .gitignore           # 🚫 Specifies files to ignore in version control
```

## ⚙️ Setup Instructions
1. Clone the repository:
   ```
   git clone https://github.com/10daviesb/blackjack-game.git
   cd blackjack-game
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the game:
   ```
   python src/main.py
   ```

## 🃏 Gameplay Rules
- 🎯 The objective of Blackjack is to beat the dealer by having a hand value closer to 21 without exceeding it.
- 🃏 Each player is dealt two cards, and they can choose to "hit" (draw another card) or "stand" (keep their current hand).
- 🤖 The dealer must hit until their hand value is 17 or higher.
- 🂡 Aces can count as 1 or 11, and face cards (Kings, Queens, Jacks) count as 10.
- 💥 If the player's hand exceeds 21, they bust and lose the round.

## ✨ Features
- 💰 **Betting System**: Place bets before starting the game.
- ✂️ **Splitting Hands**: Split your hand into two if the first two cards are of the same rank.
- 🛡️ **Insurance**: Place an insurance bet if the dealer's face-up card is an Ace.
- 🎥 **Smooth Animations**: Cards are animated as they are drawn from the deck to the player's or dealer's hand.
- 🔊 **Sound Effects**: Includes card draw sound effects.
- ⚙️ **Settings Menu**: Adjust the volume of the sound effects using a slider in the settings menu.
- 🔄 **Deck Reshuffling**: The game uses a shoe with 8 decks, and the deck is reshuffled automatically when it runs out of cards.
- 🤖 **Dealer AI**: Dealer follows standard Blackjack rules (hits until 17 or higher).

## Requirements

- 🐍 Python 3.11 or higher
- 🎵 `pygame` library for sound effects

## 🚀 Future Enhancements
- 👥 Add multiplayer support for multiple players at the same table.
- 💰 Implement betting mechanics with virtual chips.
- 🎵 Add more sound effects for winning, losing, and other game events.

## 🐛 Known Bugs
- ✂️ Split function isn't UI/UX friendly at the moment. Second hand currently unplayable
- ✌️ Missing features like double down

Enjoy the game! 🎉
