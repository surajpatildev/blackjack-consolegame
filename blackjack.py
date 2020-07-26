import random
from typing import List
import os
import time
from prettytable import PrettyTable
import numpy as np
# Classes required for BlackJack

# Card class that will represent each single card.


class Card:
    CLUB = "\u2663"
    HEART = "\u2665"
    DIAMOND = "\u2666"
    SPADE = "\u2660"

    def __init__(self, pip, suit, value):
        self.pip = pip
        self.suit = suit
        self.value = value

    def show(self):
        print(f"{self.pip} {self.showSuit(self.suit)}", end='')

    def __str__(self):
        return f"{self.pip} {self.showSuit(self.suit)}"

    def showSuit(self, suit):
        if suit == 'CLUB':
            return Card.CLUB
        elif suit == 'SPADE':
            return Card.SPADE
        elif suit == 'DIAMOND':
            return Card.DIAMOND
        elif suit == 'HEART':
            return Card.HEART

# Deck Class that will contain a deck of complete 52 cards i.e 52 objects of Card class.


class Deck:

    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        PIPS = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")
        VALUES = (11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10)
        SUITS = ('CLUB', 'SPADE', 'DIAMOND', 'HEART')
        for s in SUITS:
            for pip, v in zip(PIPS, VALUES):
                self.cards.append(Card(pip, s, v))

    def show(self):
        print('Deck Includes : ')
        for c in self.cards:
            print(c)

    def shuffle(self):
        random.shuffle(self.cards)

    def drawCard(self):
        return self.cards.pop()


class Player:
    def __init__(self, name: str, bet_value=20, chips: int = 100):
        self.name = name
        self.hands = []
        self.handsValue = 0
        self.stand = False
        self.aces = 0
        self.chips = chips
        self.bet_value = bet_value
        self.results = {'wins': 0, 'losses': 0, 'busts': 0}

    def hit(self, deck: Deck):
        card = deck.drawCard()
        self.hands.append(card)
        self.handsValue += card.value
        if card.value == 11:
            self.aces += 1
        self.adjust_for_aces()

    def show_hand(self) -> None:
        print(f'{self.name} Hand : ')
        for card in self.hands:
            print(card)

    def adjust_for_aces(self):
        while self.handsValue > 21 and self.aces:
            self.handsValue -= 10
            self.aces -= 1

    def display_results(self):
        print(f"\n{self.name} : WINS -> {self.results.get('wins')}, LOSSES -> {self.results.get('losses')} & BUSTS -> {self.results.get('busts')}")

    def reset_hand(self):
        self.hands = []
        self.handsValue = 0
        self.stand = False
        self.aces = 0
        self.bet_value = 20


class Dealer:
    def __init__(self, players: List[Player]):
        self.name = "DEALER"
        self.hands = []
        self.handsValue = 0
        self.aces = 0
        self.players = players

    def show_some(self) -> None:
        print(f'{self.name} Hand : ')
        print('1 dealer card hidden!')
        print(self.hands[1])

    def show_hand(self) -> None:
        print(f'{self.name} Hand : ')
        for card in self.hands:
            print(card)

    def hit(self, deck: Deck):
        card = deck.drawCard()
        self.hands.append(card)
        self.handsValue += card.value
        if card.value == 11:
            self.aces += 1
        self.adjust_for_aces()
        return self

    def adjust_for_aces(self):
        while self.handsValue > 21 and self.aces:
            self.handsValue -= 10
            self.aces -= 1

    # def settle(self, players: List[Player]):

    #     for player in players:
    #         if player.hand.winningHand:
    #             player.chips += BET_VALUE


class BlackJack:
    def __init__(self, players: List[Player]):
        self.players = players
        self.dealer = Dealer(players)
        self.gameOn = False

        os.system('cls')
        # Starting the Game
        self.start_game()

    def start_game(self):
        # Create & shuffle the deck, deal two cards to each player
        deck = Deck()
        deck.shuffle()
        player = self.players[0]
        player.hit(deck)
        player.hit(deck)
        self.dealer.hit(deck)
        self.dealer.hit(deck)
        self.player_bet(player)
        # Show cards (but keep one dealer card hidden)
        # self.display_board_partial(self.players, self.dealer)
        self.game_screen(player, partial=True)

        if player.handsValue == 21:
            self.player_wins(player, self.dealer)
        else:
            while not player.stand:  # We will continue untill player decides to stand or busts

                # Prompt for Player to Hit or Stand
                self.hit_or_stand(player, deck)
                # #Show cards (but keep one dealer card hidden)
                # self.display_board(self.players, self.dealer)
                self.game_screen(player, partial=True)
                # If player's hand exceeds 21, run player_busts() and break out of loop
                if player.handsValue > 21:
                    self.player_busts(player, self.dealer)
                    # Resseting player game attributes
                    player.reset_hand()
                    # Inform Player of their chips total
                    player.display_results()
                    print(f"\n{player.name}'s winnings stand at : {player.chips}")
                    return None
                elif player.handsValue == 21:

                    self.player_wins(player, self.dealer)
                    # Resseting player game attributes
                    player.reset_hand()
                    # Inform Player of their chips total
                    player.display_results()
                    print(f"\n{player.name}'s winnings stand at : {player.chips}")
                    return
                # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
            os.system('cls')
            print(f"Player standing on {player.handsValue}. Its Dealers Turn!")
            time.sleep(0.50)
            print("Dealer's hand will be continued until Dealer reaches 17")
            time.sleep(2.5)
            if player.handsValue <= 21:
                while self.dealer.handsValue < 17:
                    self.game_screen_dealer()
                    print(f'{self.dealer.name} : Drawing the CARD from DECK . . . ')
                    self.dealer.hit(deck)  # hit() function defined above
                    time.sleep(1)
                    print(f'{self.dealer.name} : The card drawn is - ', end='', flush=True)
                    time.sleep(0.75)
                    print(f' {self.dealer.hands[-1]}')
                    time.sleep(2)

            # Show all cards
            self.game_summary()
            print("This is the Final Scorecard ...")
            time.sleep(3)
            # Run different winning scenarios
            if self.dealer.handsValue > 21:
                self.dealer_busts(player, self.dealer)

            elif self.dealer.handsValue > player.handsValue:
                self.dealer_wins(player, self.dealer)

            elif self.dealer.handsValue < player.handsValue:
                self.player_wins(player, self.dealer)

            else:
                self.push(player, self.dealer)

        # Resseting player game attributes
        player.reset_hand()
        # Inform Player of their chips total
        player.display_results()
        print(f"\n{player.name}'s winnings stand at : {player.chips}")

    def player_bet(self, player: Player):
        print(f'{player.name}, you have got {player.chips} Chips')
        while True:
            try:
                player.bet_value = int(input('Enter the amount of chips you want to bet : '))
            except Exception:
                print('Please enter a valid integer chips amount!')
            else:
                if player.bet_value < 1:
                    print(f'Bet should be at lease 1!')
                    continue
                if player.bet_value > player.chips:
                    print(f'Insufficient Chips! Your chips : {player.chips}')
                    continue
                else:
                    break

    def hit_or_stand(self, player: Player, deck: Deck):
        while True:
            x = input(f"{player.name} :Would you like to Hit or Stand? Enter 'h' or 's' ")

            if x[0].lower() == 'h':
                print(f'{player.name} : Drawing the CARD from DECK . . . ')
                player.hit(deck)  # hit() function defined above
                time.sleep(1)
                print(f'{player.name} : The card drawn is - ', end='', flush=True)
                time.sleep(0.75)
                print(f' {player.hands[-1]}')
                time.sleep(1.75)

            elif x[0].lower() == 's':
                print(f"{player.name} will STAND on {player.handsValue}")
                time.sleep(2)
                player.stand = True

            else:
                print("Sorry, please try again.")
                continue
            break

    def player_wins(self, player: Player, dealer: Dealer):
        self.game_summary()
        if player.handsValue == 21:
            print("!!!!--CONGRATS! YOU'VE HIT A BLACKJACK--!!!!")
        print(f"!!!--------------{player.name} WINS!--------------!!!")
        print(f"!!!------------ WINNER : {player.name} -----------!!!")
        player.results['wins'] += 1
        player.chips += player.bet_value

    def player_busts(self, player: Player, dealer: Dealer):
        self.game_summary()
        print(f"!!!--------------{player.name} BUSTS!--------------!!!")
        print(f"!!!------------ WINNER : {dealer.name} -----------!!!")
        player.results['busts'] += 1
        player.chips -= player.bet_value

    def dealer_busts(self, player: Player, dealer: Dealer):
        self.game_summary()
        print(f"!!!--------------{dealer.name} BUSTS!--------------!!!")
        print(f"!!!------------ WINNER : {player.name} -----------!!!")
        player.results['wins'] += 1
        player.chips += player.bet_value

    def dealer_wins(self, player: Player, dealer: Dealer):
        self.game_summary()
        if dealer.handsValue == 21:
            print("!!!!--DEALER HAS HIT A BLACKJACK--!!!!")
        print(f"!!!--------------{dealer.name} WINS!--------------!!!")
        print(f"!!!------------ WINNER : {dealer.name} -----------!!!")
        player.results['losses'] += 1
        player.chips -= player.bet_value

    def push(self, player: Player, dealer: Dealer):
        self.game_summary()
        print("Dealer and Player tie! It's a push.")

    def display_board(self, players: List[Player], dealer: Dealer):
        headers = [dealer.name]
        lens = [len(dealer.hands)]

        for player in players:
            lens.append(len(player.hands))
            headers.append(player.name)

        max_len = max(lens)
        delear_hand_arr = ['' for i in range(max_len)]
        for i, card in enumerate(dealer.hands):
            delear_hand_arr[i] = card

        arr = np.array([delear_hand_arr])

        for player in players:
            player_hand_arr = ['' for i in range(max_len)]
            for i, card in enumerate(player.hands):
                player_hand_arr[i] = card
            arr = np.append(arr, [player_hand_arr], axis=0)

        arr = arr.T
        t = PrettyTable(headers)
        for row in arr:
            t.add_row(row)
        print(t)

    def display_board_partial(self, players: List[Player], dealer: Dealer):

        headers = [dealer.name]
        lens = [len(dealer.hands)]

        for player in players:
            lens.append(len(player.hands))
            headers.append(player.name)

        max_len = max(lens)
        delear_hand_arr = ['' for i in range(max_len)]
        for i, card in enumerate(dealer.hands):
            if i == 0:
                delear_hand_arr[i] = 'HIDDEN'
            else:
                delear_hand_arr[i] = card

        arr = np.array([delear_hand_arr])

        for player in players:
            player_hand_arr = ['' for i in range(max_len)]
            for i, card in enumerate(player.hands):
                player_hand_arr[i] = card
            arr = np.append(arr, [player_hand_arr], axis=0)

        arr = arr.T
        t = PrettyTable(headers)
        for row in arr:
            t.add_row(row)
        print(t)

    def display_summary_board(self):
        headers = [self.dealer.name]
        lens = [len(self.dealer.hands)]

        for player in self.players:
            lens.append(len(player.hands))
            headers.append(player.name)

        max_len = max(lens) + 2
        delear_hand_arr = ['' for i in range(max_len)]
        for i, card in enumerate(self.dealer.hands):
            delear_hand_arr[i] = card
        delear_hand_arr[-2] = '------------'
        delear_hand_arr[-1] = self.dealer.handsValue

        arr = np.array([delear_hand_arr])

        for player in self.players:
            player_hand_arr = ['' for i in range(max_len)]
            for i, card in enumerate(player.hands):
                player_hand_arr[i] = card
            player_hand_arr[-2] = '------------'
            player_hand_arr[-1] = player.handsValue
            arr = np.append(arr, [player_hand_arr], axis=0)

        arr = arr.T
        t = PrettyTable(headers)
        for row in arr:
            t.add_row(row)
        print(t)

    def game_screen(self, player, partial=False):
        os.system('cls')
        print(f'-------PLAYERS (bet value) {len(self.players)} nos. : ', end='')
        for ply in self.players:
            print(f"{ply.name} ({ply.bet_value}), ", end='')
        print('-------\n-----------------------------------------------------------------------')
        if partial:
            self.display_board_partial(self.players, self.dealer)
        else:
            self.display_board(self.players, self.dealer)
        print('-----------------------------------------------------------------------')
        print(f"CURRENT TURN : {player.name}")
        print(f"{player.name}'s previous hit - {player.hands[-1]}")
        print('-----------------------------------------------------------------------')

    def game_screen_dealer(self):
        os.system('cls')
        print(f'-------PLAYERS (bet value) {len(self.players)} nos. : ', end='')
        for ply in self.players:
            print(f"{ply.name} ({ply.bet_value}), ", end='')
        print('-------\n-----------------------------------------------------------------------')
        self.display_board(self.players, self.dealer)

        print('-----------------------------------------------------------------------')
        print(f"CURRENT TURN : {self.dealer.name}")
        print(f"{self.dealer.name}'s previous hit - {self.dealer.hands[-1]}")
        print('-----------------------------------------------------------------------')

    def game_summary(self):
        os.system('cls')
        print(f'-------PLAYERS (bet value) {len(self.players)} nos. : ', end='')
        for ply in self.players:
            print(f"{ply.name} ({ply.bet_value}), ", end='')
        print('-------\n-----------------------------------------------------------------------')

        self.display_summary_board()
        print('-----------------------------------------------------------------------')


# Printing an opening statements
print('> Welcome to BlackJack! Get as close to 21 as you can without going over!\n\
> Dealer hits until she reaches 17. Aces count as 1 or 11.')
print("""> Example summary window of a BlackJack Game :

    --------------------------------------------------------
    -------PLAYERS (bet value) 1 nos. : Suraj (53), -------
    --------------------------------------------------------
    +--------------+--------------+
    |    DEALER    |    Suraj     |
    +--------------+--------------+
    |     A ♦      |     3 ♠      |
    |     4 ♣      |     10 ♠     |
    |              |     Q ♣      |
    | ------------ | ------------ |
    |      15      |      23      |
    +--------------+--------------+
    -------------------------------------------------------
    !!!--------------Suraj BUSTS!--------------!!!
    !!!------------ WINNER : DEALER -----------!!!
    Suraj : WINS -> 0, LOSSES -> 0 & BUSTS -> 1
    -------------------------------------------------------
""")
input('Pless enter to start the Game...  ')

# Geeting the player name to set the player object
player_name = ''
while True:
    os.system('cls')
    print('> Welcome to BlackJack!')
    player_name = input('> Enter Your Name - ')

    if player_name == '':
        continue
    break

player_1 = Player(player_name.upper())

while True:
    game = BlackJack([player_1])
    # Ask to play again
    if player_1.chips > 1:
        new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")
    else:
        print("You have exhausted your chips! Well played! Seeya Later!")
        print("Thanks for playing!")
        time.sleep(5)
        exit()

    if new_game[0].lower() != 'n':
        continue
    else:
        print("Thanks for playing!")
        time.sleep(10)
        exit()
