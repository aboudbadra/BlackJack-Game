#!/usr/bin/env python3

"""
BlackJack Game

Play against the dealer

# Game Play:

# To play a hand of Blackjack the following steps are followed:

# 1. Create a deck of 52 cards
# 2. Shuffle the deck
# 3. Ask the Player for their bet
# 4. Make sure that the Player's bet does not exceed their available chips
# 5. Deal two cards to the Dealer and two cards to the Player
# 6. Show only one of the Dealer's cards, the other remains hidden
# 7. Show both of the Player's cards
# 8. Ask the Player if they wish to Hit, and take another card
# 9. If the Player's hand doesn't Bust (go over 21), ask if they'd like to Hit again.
# 10. If a Player Stands, play the Dealer's hand. The dealer will always Hit until the Dealer's value meets or exceeds 17
# 11. Determine the winner and adjust the Player's chips accordingly
# 12. Ask the Player if they'd like to play again

"""
import random
from IPython.display import clear_output

#-------------------------------------------------------------------------------#
#                            Global Variables                                   #
#-------------------------------------------------------------------------------#
suits = ('Hearts','Diamonds','Spades','Clubs')
ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')
values = {'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':10,'Queen':10,'King':10,'Ace':11}

game_on = True

#-------------------------------------------------------------------------------#
#                                 Classes                                       #
#-------------------------------------------------------------------------------#
class Card():
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return f'{self.rank} of {self.suit}'
    
#-------------------------------------------------------------------------------#    
class Deck():
    
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks: 
                self.deck.append(Card(suit, rank))
    
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return 'The deck has: '+ deck_comp
    
    # Actions
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):       
        single_card = self.deck.pop()
        return single_card

#-------------------------------------------------------------------------------#    
class Hand:
    
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
    
    def add_card(self, card):
        
        # card passed in from Deck.deal() --> single Card(suit,rank)
        self.cards.append(card)
        self.value += values[card.rank]
        
        # track aces
        if card.rank == 'Ace':
            self.aces += 1
           
    def adjust_for_ace(self):
        # If Total Value > 21 and I still have an ace
        # Then change my Ace to be a 1 instead of an 11
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1
            
#-------------------------------------------------------------------------------#
class Chips:
    
    def __init__(self, total = 100):
        self.total = total       
        self.bet = 0
    
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet
    
#-------------------------------------------------------------------------------#

#-------------------------------------------------------------------------------#
#                                   Functions                                   #
#-------------------------------------------------------------------------------#

def take_bet(chips):
    
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
                           
        except:
            print('Type Error, you did not enter a number.')
            continue
            
        else:
            if chips.bet > chips.total:
                print(f'Funds Unavailable, Current Balance is only {chips.total} chips.\n')
                continue
            else:
                break

def hit(deck, hand):
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()

def hit_or_stand(deck, hand):
    global game_on
    
    
    ask_player = ''
    
    while ask_player.upper() != 'H' and ask_player.upper() != 'S':
        ask_player = input('Hit or Stand [H/S]?')
    
    if ask_player[0].upper() == 'H':
        hit(deck,hand)
    
    elif ask_player[0].upper() == 'S':
        print("\nPlayer Stands --> Dealer's Turn")
        game_on = False
        
            
def show_some(player,dealer):
    print("\n--------------------------------")
    print("Dealer's Hand:")
    print(" <card hidden>")
    print('',dealer.cards[1])  
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("--------------------------------\n")
    


def show_all(player, dealer):
    print("\n--------------------------------")
    print("Dealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand = ",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand = ",player.value)
    print("--------------------------------\n")

def replay():
    
    play = ''
    
    while play.upper() != 'Y' and play.upper() != 'N':
        
        play = input('\nDo you want to play again [Y/N]: ')
    
    return play.upper() == 'Y'

#                     Functions to handle end of game scenarios                 #
#-------------------------------------------------------------------------------#

def player_busts(player, dealer, chips):
    print('PLAYER BUSTED!')
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print('PLAYER WINS!')
    chips.win_bet()
    
def dealer_busts(player, dealer, chips):
    print('PLAYER WINS! DEALER BUSTED!')
    chips.win_bet()
    
def dealer_wins(player, dealer, chips):
    print('DEALER WINS! PLAYER BUSTED!')
    chips.lose_bet()
    
def push(player, dealer):
    print('Player and Dealer tie! PUSH')

    

#-------------------------------------------------------------------------------#    
#                                 GAME PLAY                                     #
#-------------------------------------------------------------------------------#

while True:
    clear_output()
    print('Welcome to BlackJack! Get as close to 21 as you can without going over!\n\
        Dealer hits until she reaches 17. Aces count as 1 or 11.')
    # Create and shuffle deck

    deck = Deck()
    deck.shuffle()

    # Deal two cards to each player
    # Player Hand
    player = Hand()
    player.add_card(deck.deal())
    player.add_card(deck.deal())


    # Dealer Hand
    dealer = Hand()
    dealer.add_card(deck.deal())
    dealer.add_card(deck.deal())

    # setup player's chips
    player_chips = Chips()

    # prompt player for their bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player, dealer)

    while game_on:
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player)
        
        # Show cards (but keep one dealer card hidden)
        show_some(player, dealer)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player.value > 21:
            player_busts(player, dealer, player_chips)
            break
    
    if player.value <= 21:
        
        while dealer.value < 17:
            hit(deck, dealer)
            
        # show all cards
        show_all(player, dealer)
        
        # Test end of game scenarios
        if dealer.value > 21:
            dealer_busts(player, dealer, player_chips)
        
        elif dealer.value > player.value:
            dealer_wins(player, dealer, player_chips)
            
        elif player.value > dealer.value:
            player_wins(player, dealer, player_chips)
        
        else:
            push(player, dealer)
    
    # Inform Player of their chips total 
    print("\nPlayer's winnings stand at",player_chips.total)

   # Ask to play again
    new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")
    
    if new_game[0].lower()=='y':
        game_on=True
        continue
    else:
        print("Thanks for playing!")
        break

