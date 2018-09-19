from random import choice
from aenum import Enum, NoAlias
from UserInputProvider import *


class Color(Enum):
    HEART = 1
    DIAMOND = 2
    PEAK = 3
    CLUB = 4


class ListOfColors(object):

    def __init__(self):
        self.colors = []
        for color in Color:
            self.colors.append(color.name)


class Sign(Enum):
    _settings_ = NoAlias
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 10
    QUEEN = 10
    KING = 10


class ListOfSigns(object):

    def __init__(self):
        self.signs = []
        for sign in Sign:
            self.signs.append([sign.name, sign.value])


class Card(object):

    def __init__(self, sign, color, value):
        self.card = [str(sign) + " " + str(color), value]


class ListOfCards(object):

    def __init__(self):
        self.cards= []
        for color in ListOfColors().colors:
            for sign in ListOfSigns().signs:
                self.cards.append(Card(sign[0], color, sign[1]).card)


class Deck(object):

    def __init__(self):
        self.cards = ListOfCards().cards
        self.waist = {}
        for i in range(len(self.cards)):
            self.waist[self.cards[i][0]] = self.cards[i][1]


class Croupier(object):

    def __init__(self):
        self.score = 0
        self.hand = []
        self.deck = Deck().waist

    def give_random_card(self, number):
        cards = []
        for i in range(number):
            card = choice(list(self.deck))
            self.delete_card_from_deck(card)
            cards.append(card)
        return cards

    def delete_card_from_deck(self, card):
        del self.deck[card]

    def print_cards(self, hand):
        cards = ""
        for card in hand:
            cards += card + " "
        return cards

    def get_cards(self, hand, number):
        hand.extend(self.give_random_card(number))

    def count_score(self, hand):
        result = 0
        for card in hand:
            result += int(Deck().waist[card])
        return result

    def check_if_ace_in_hand(self, hand):
        list_of_signs = []
        for i in range(len(hand)):
            sign_and_value = hand[i].split()
            list_of_signs.append(sign_and_value[0])
        if "ACE" in list_of_signs:
            return True

    def if_ace(self):
        if 16 < self.count_score(self.hand) + 10 <= 21:
            self.score = self.count_score(self.hand) + 10
        else:
            self.get_cards(self.hand, 1)
            print("Croupier have: ", self.print_cards(self.hand))
            self.get_croupier_score()

    def get_croupier_score(self):
        if self.count_score(self.hand) <= 16:
            if self.check_if_ace_in_hand(self.hand):
                self.if_ace()
            else:
                self.get_cards(self.hand, 1)
                print("Croupier have: ", self.print_cards(self.hand))
                self.get_croupier_score()
        else:
            self.score = self.count_score(self.hand)


class Player(object):

    def __init__(self):
        self.score = 0
        self.hand = []
        self.croupier = Croupier()

    @staticmethod
    def bet():
        return int(UserInputProvider().collect_int_in_range_from_user(0, 1000, "Please enter your amount of bet bigger than 0, less then 1000: "))

    def select_activity(self, bet_value):
        activity = UserInputProvider().collect_proper_str_from_user(["h", "st", "dd"], "Please enter h for hit, st for stand or dd for double down: ")
        if activity == "h":
            self.croupier.get_cards(self.hand, 1)
            print("You have: ", self.croupier.print_cards(self.hand))
            self.select_activity(bet_value)
        elif activity == "st":
            self.get_player_score()
        elif activity == "dd":
            self.croupier.get_cards(self.hand, 1)
            bet_value = bet_value * 2
            print("You have: ", self.croupier.print_cards(self.hand), ". Your bet is equal to: ", bet_value)
            self.select_activity(bet_value)

    def get_player_score(self):
        if self.croupier.check_if_ace_in_hand(self.hand):
            decision = UserInputProvider().collect_proper_str_from_user(["1", "11"], "What value of ACE do you prefer? Enter 1 or 11: ")
            if decision == 11:
                self.score = self.croupier.count_score(self.hand) + 10
        else:
            self.score = self.croupier.count_score(self.hand)


class Game(object):

    def __init__(self):
        self.player = Player()
        self.croupier = Croupier()
        self.bet_value = self.player.bet()
        self.croupier.get_cards(self.player.hand, 2)
        print("You have: ", self.croupier.print_cards(self.player.hand))
        self.croupier.get_cards(self.croupier.hand, 2)
        print("Croupier have: ", self.croupier.hand[0])
        self.player.select_activity(self.bet_value)
        self.croupier.get_croupier_score()
        print("Croupier cards: ", self.croupier.print_cards(self.croupier.hand))
        self.check_the_winner()

    def check_the_buster(self):
        if self.player.score > 21:
            print("Player bust")
            return True
        if self.croupier.score > 21:
            print("Croupier bust, Player win", self.bet_value)
            return True
        else:
            return False

    def check_the_winner(self):
        if not self.check_the_buster():
            if self.player.score == self.croupier.score:
                print("Draw")
            elif 21 - self.player.score > 21 - self.croupier.score:
                print("Croupier win")
            else:
                print("Player win ", self.bet_value)


print(Game())
