class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def calculate_total(self):
        total = 0
        aces = 0
        for card in self.cards:
            if card.rank in ['J', 'Q', 'K']:
                total += 10
            elif card.rank == 'A':
                aces += 1
                total += 11
            else:
                total += card.rank

        while total > 21 and aces:
            total -= 10
            aces -= 1

        return total

    def clear_hand(self):
        self.cards = []