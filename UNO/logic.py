from time import time
import numpy as np
import random
from deck import get_deck
'''
# we have the 108 cards 
# 4 colors RED  , BLUE  , GREEN , YELLOW 
0-9
# number of cards 80 per color 
# action card 24 -- 2 each draw +2 , skip , reverse 
# wild card color change -- 4 color 

Game SetupPlayer Count:
The game is designed for 2 to 10 players. 
2 to 4 players (including AI bots) is ideal.
Starting Hand: Shuffle the deck and deal exactly 7 cards to each player.
Draw Pile: Place the remaining cards face-down to form the Draw Pile.
Discard Pile: Flip the top card of the Draw Pile face-up to start the Discard Pile.
If this initial card is an Action or Wild card, specific starting rules apply 
(e.g., if it is a Draw Four, it is typically shuffled back into the deck)

The game moves clockwise by default. 
On their turn, a player must match the top card of the Discard Pile by Color, Number, or Symbol.
If a match is found: The player can play that card from their hand onto the Discard Pile.

If no match is found: The player must draw one card from the Draw Pile.
If the drawn card is playable, they can choose to play it immediately.
Otherwise, their turn ends.Ending a Turn: Turn passes to the next player in the current rotation.

Winning and "Uno"Calling Uno:
When a player has only one card left in their hand, they must announce "Uno." 
If they are caught by another player before the next player begins their turn,
they must draw two penalty cards.Winning condition:
The round ends immediately when a player successfully plays their final card

'''

class UNO:
    
    def __init__(self,n_players=2,ncards=108):
       self.n_players = n_players
       self.ncards = ncards
           
    def start_game(self):
        #all displaying things 
        # game logic 
        # first shuffle then draw hands of cards  
        deck = get_deck(self.ncards)
        deck = self._shuffle(deck)
        player_hand , computer_hand = self._draw_players_cards(deck=deck)
        discard_card = random.choice(deck)
                
        discard_card_layout = f'''
        ========================
        |         {1}            |
        |    {discard_card['color']}               |
        |    {discard_card['value']}          |
        ========================
        '''
        print('discard card ')
        print(discard_card_layout)
        
        while len(player_hand) == 0 or len(computer_hand) == 0 :
            
            for i , cards in enumerate(player_hand):
                card_color = cards['color']
                card_val = cards['value']
                print(f'player card{i+1} have {card_color} and card value {card_val}',end=' ')
            
                 
    
    def _shuffle(self,deck):
        return random.shuffle(deck)
    
    def _draw_players_cards(self,deck):
        hand1 = deck[:7]
        hand2 = deck[7:14]
        return hand1 , hand2