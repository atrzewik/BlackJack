from random import choice
from aenum import Enum, NoAlias
from UserInputProvider import *


class Color(Enum):
    HEART = 1
    DIAMOND = 2
    SPADE = 3
    CLUB = 4

    @classmethod
    def values(cls):
        return list(cls)


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

    @classmethod
    def values(cls):
        return list(cls)


class Card(object):

    def __init__(self, sign, color):
        self.sign = sign
        self.color = color

    def __repr__(self):
        return self.sign.name + " " + self.color.name


class Deck(object):

    def __init__(self):
        self.cards = []
        for color in Color.values():
            for sign in Sign.values():
                self.cards.append(Card(sign, color))

    def shuffled_deck(self):
        cards = []
        for i in range(len(self.cards)):
            card = choice(self.cards)
            self.delete_card_from_deck(self.cards, card)
            cards.append(str(card))
        return cards

    def delete_card_from_deck(self, deck, card):
        deck.remove(card)


class Contestant(object):

    def __init__(self, hand):
        self.hand = hand
        self.shuffled_deck = Deck().shuffled_deck()

    def get_cards(self, number):
        for i in range(number):
            self.hand.append(self.shuffled_deck[0])
            Deck().delete_card_from_deck(self.shuffled_deck, self.shuffled_deck[0])

    def count_score(self):
        result = 0
        for card in self.hand:
            for sign in Sign.values():
                if sign.name == card.split()[0]:
                    result += sign.value
        return result

    def check_if_ace_in_hand(self):
        list_of_signs = []
        for i in range(len(self.hand)):
            list_of_signs.append(self.hand[i].split()[0])
        if "ACE" in list_of_signs:
            return True


class Croupier(Contestant):

    def print_cards(self, hand):
        cards = ""
        for card in hand:
            cards += card + " "
        return cards

    def if_ace(self):
        score = self.count_score()
        if 16 < score + 10 <= 21:
            score += 10
            return score
        else:
            self.get_cards(1)
            print("Croupier have: ", self.print_cards(self.hand))
            self.get_croupier_score()

    def get_croupier_score(self):
        score = self.count_score()
        if score <= 16:
            if self.check_if_ace_in_hand():
                return self.if_ace()
            else:
                self.get_cards(1)
                print("Croupier have: ", self.print_cards(self.hand))
                self.get_croupier_score()
        else:
            return score


class Player(Contestant):

    @staticmethod
    def bet():
        return int(UserInputProvider().collect_int_in_range_from_user(0, 1000, "Please enter your amount of bet bigger than 0, less then 1000: "))

    def select_activity(self, bet_value):
        activity = UserInputProvider().collect_proper_str_from_user(["h", "st", "dd"], "Please enter h for hit, st for stand or dd for double down: ")
        if activity == "h":
            self.get_cards(1)
            self.select_activity(bet_value)
        elif activity == "st":
            self.get_player_score()
        elif activity == "dd":
            self.get_cards(1)
            bet_value = bet_value * 2
            print("Your bet is equal to: ", bet_value)
            self.select_activity(bet_value)

    def get_player_score(self):
        score = self.count_score()
        if self.check_if_ace_in_hand():
            decision = int(UserInputProvider().collect_proper_str_from_user(["1", "11"], "What value of ACE do you prefer? Enter 1 or 11: "))
            if decision == 11:
                score += 10
        return score


d = []
Croupier(d).get_cards(2)
print("CARDS", d)
c = Croupier(d).get_croupier_score()
print("Croupier", c)

d = []
Player(d).get_cards(2)
print("CARDS", d)
c = Player(d).get_player_score()
print("Player", c)


class Cache(object):

    def __init__(self):
        self.number_of_players = 0
        self.players_names = []
        self.players_hands = {}

    def get_numbers_of_players(self):
        self.number_of_players += UserInputProvider().collect_int_in_range_from_user(1, 6, "Please enter number of players: 1 - 6: ")

    def get_players_names(self):
        for i in range(self.number_of_players):
            name = UserInputProvider().collect_str_from_user("Please enter name for %s player: " % (i+1))
            self.players_names.append(name)

    def get_players_hands(self):
        for i in range(self.number_of_players):
            self.players_hands[self.players_names[i]] = []


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
        if self.player.score > 21 and self.croupier.score > 21:
            print("Draw")
            condition = 0
            return condition, True
        elif self.player.score > 21:
            print("Player bust, Croupier win")
            condition = -1
            return condition, True
        elif self.croupier.score > 21:
            print("Croupier bust, Player win", self.bet_value)
            condition = 1
            return condition, True
        else:
            return False

    def check_the_winner(self):
        if not self.check_the_buster():
            if self.player.score == self.croupier.score:
                print("Draw")
                condition = 0
                return condition
            elif 21 - self.player.score > 21 - self.croupier.score:
                print("Croupier win")
                condition = -1
                return condition
            else:
                print("Player win ", self.bet_value)
                condition = 1
                return condition


# print(Game())
