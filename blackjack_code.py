import random
# Variables
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

# Card class - initializes each card
class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return self.rank + ' of ' + self.suit

# Deck class - shuffles and creates the deck of cards
class Deck:
    
    def __init__(self):
        self.deck = []

        for suit in suits:
            for rank in ranks:
                created_card = Card(suit,rank)
                self.deck.append(created_card)

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        dealt_card = self.deck.pop()
        return dealt_card

# Hand class - calculate value of cards
class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]

        if card.rank == 'Ace':
            self.aces += 1

    def adjust_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

# Chips class - balance of chips, bets, and winnings/losses
class Chips:

    def __init__(self):
        self.total = 100
        self.bet = 0

    def bet_won(self):
        self.total += self.bet

    def bet_loss(self):
        self.total -= self.bet

# Making a bet
def make_bet(chips):
    while True:

        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except ValueError:
            print('Please enter a correct amount')
        else:
            if chips.bet > chips.total:
                print(f'Sorry, that bet exceeds your amount of chips you have: {chips.total}')
            else:
                break

# Taking a hit
def hit(deck,hand):
    
    hand.add_card(deck.deal())
    hand.adjust_ace()
    
# Whether to hit or stand
def hit_or_stand(deck,hand):
    global playing

    while True:

        response = input('Hit or Stand? Enter h or s: ')

        if response[0].lower() == 'h':
            hit(deck,hand)
        elif response[0].lower() == 's':
            print("Player stands, it is the dealer's turn.")
            playing = False
        else:
            print('Please enter a correct command.')
            continue
        break

# Display the cards and values
def some_shown(player,dealer):
    print("\n - Dealer's hand - ")
    print('First card hidden')
    print(dealer.cards[1])

    print("\n - Player's hand - ")
    for card in player.cards:
        print(card)
   
def all_shown(player,dealer):
    print("\n - Player's hand - ")
    for card in player.cards:
        print(card)
    print(f"Value of Player's hand: {player.value}")

    print("\n - Dealer's hand - ")
    for card in dealer.cards:
        print(card)
        print(f"Value of Dealer's hand: {dealer.value}")

# End game scenarios
def player_busts(player,dealer,chips):
    print('Player BUST!')
    chips.bet_loss()

def player_wins(player,dealer,chips):
    print('Player wins!')
    chips.bet_won()

def dealer_busts(player,dealer,chips):
    print('Player wins! Dealer BUST!')
    chips.bet_won()
    
def dealer_wins(player,dealer,chips):
    print('Dealer wins!')
    chips.bet_loss()
    
def push(player,dealer):
    print('Player and Dealer tie, PUSH!')

# Actual Game
while True:
    #Opening statement
    print('Welcome to Blackjack!')

    # Create & shuffle the deck, deal two cards to Player and Dealer
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Set up the Player's chips
    players_chips = Chips()

    # Prompt the Player for their bet
    make_bet(players_chips)
    
    # Display cards
    some_shown(player_hand,dealer_hand)
    
    while playing:
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player_hand)
        
        # Show Player's cards but only one of the dealers
        some_shown(player_hand, dealer_hand)
 
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,players_chips)
            break 

    # If Player hasn't busted, play Dealer's hand until Soft 17 rule
    if player_hand.value <=21:

        while dealer_hand.value < 17:
            hit(deck, dealer_hand)
    
        # Show all cards
        all_shown(player_hand,dealer_hand)
    
        # Winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,players_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,players_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,players_chips)
        else:
            push(player_hand,dealer_hand)
    
    # Show Player's chips total 
    print(f"\n Player's total chips are {players_chips.total}")

    # Ask to play again
    new_game = input('Would you like to play another hand? y/n: ')
    if new_game[0].lower() == 'y':
        player = True
    else:
        print('Thank you for playing. Come again.')
        break
