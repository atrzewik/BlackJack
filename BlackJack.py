from random import sample
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

    def shuffle_deck(self):
        return sample(self.cards, len(self.cards))

    def delete_card_from_deck(self, deck, card):
        deck.remove(card)

    def get_cards(self, hand, deck, number):
        for i in range(number):
            hand.append(deck[0])
            Deck().delete_card_from_deck(deck, deck[0])


class Contestant(object):

    def __init__(self):
        self.hand = []

    def count_score(self):
        result = 0
        for card in self.hand:
            result += card.sign.value
        return result

    def check_if_ace_in_hand(self):
        list_of_signs = [card.sign for card in self.hand]
        if Sign.ACE in list_of_signs:
            return True

    def print_cards(self):
        return self.hand


class Croupier(Contestant):

    def action_if_ace_in_croupier_hand(self, deck):
        score = self.count_score()
        if 16 < score + 10 <= 21:
            score += 10
            return score
        else:
            Deck().get_cards(self.hand, deck, 1)
            print("Croupier have: ", self.print_cards())
            return self.get_croupier_score(deck)

    def get_croupier_score(self, deck):
        score = self.count_score()
        if score <= 16:
            if self.check_if_ace_in_hand():
                return self.action_if_ace_in_croupier_hand(deck)
            else:
                Deck().get_cards(self.hand, deck, 1)
                print("Croupier have: ", self.print_cards())
                return self.get_croupier_score(deck)
        else:
            return score


class Player(Contestant):

    @staticmethod
    def bet(name):
        return int(UserInputProvider().collect_int_in_range_from_user(0, 1000, "%s please enter your amount of bet bigger than 0, less then 1000: " % name))

    def names(self, number_of_players):
        names = []
        for i in range(number_of_players):
            name = UserInputProvider().collect_str_from_user("Please enter name for %s player: " % (i + 1))
            names.append(name)
        return names

    def select_activity(self, name, deck, bet_value):
        activity = UserInputProvider().collect_proper_str_from_user(["h", "st", "dd"], "%s please enter h for hit, st for stand or dd for double down: " % name)
        if activity == "h":
            self.hold(name, deck, bet_value)
        elif activity == "st":
            self.stand()
        elif activity == "dd":
            self.double_down(name, deck, bet_value)

    def hold(self, name,  deck, bet_value):
        Deck().get_cards(self.hand, deck, 1)
        self.select_activity(name, deck, bet_value)

    def stand(self):
        self.get_player_score()

    def double_down(self, name, deck, bet_value):
        Deck().get_cards(self.hand, deck, 1)
        bet_value = bet_value * 2
        print("Your bet is equal to: ", bet_value)
        self.select_activity(name, deck, bet_value)

    def get_player_score(self):
        score = self.count_score()
        if self.check_if_ace_in_hand():
            decision = int(UserInputProvider().collect_proper_str_from_user(["1", "11"], "What value of ACE do you prefer? Enter 1 or 11: "))
            if decision == 11:
                score += 10
        return score


class Game(object):

    def __init__(self):
        self.player = Player()
        self.croupier = Croupier()
        self.number_of_players = UserInputProvider().collect_int_in_range_from_user(1, 6, "Please enter number of players: 1 - 6: ")
        self.players_names = self.player.names(self.number_of_players)
        self.bets_values = {}
        for name in self.players_names:
            self.bets_values[name] = self.player.bet(name)
        deck = Deck().shuffle_deck()
        Deck().get_cards(self.croupier.hand, deck, 2)
        print("Croupier have: ", self.croupier.hand[0])
        self.players_hands = {}
        for name in self.players_names:
            hand = []
            Deck().get_cards(hand, deck, 2)
            self.players_hands[name] = hand
            print("%s have: " % name, self.players_hands[name])
        for name in self.players_names:
            self.player.select_activity(name, deck, self.bets_values[name])


print(Game())
