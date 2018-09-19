from random import choice
from enum import Enum, auto
from UserInputProvider import *


class Color(Enum):
    HEART = auto()
    DIAMOND = auto()
    PEAK = auto()
    CLUB = auto()


class Sign(Enum):
    ACE = [1, 11]
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


class Card(object):

    def __init__(self, sign, color, value):
        self.card = [str(sign) + " " + str(color), value]


class Desk(object):

    def __init__(self):
        self.cards = self.list_of_cards()
        self.waist = {}
        for i in range(len(self.cards)):
            self.waist[self.cards[i][0]] = self.cards[i][1]

    @staticmethod
    def list_of_cards():
        cards = []
        for color in Color:
            cards_in_colour = [Card(Sign.TWO.name, color.name, Sign.TWO.value).card,
                               Card(Sign.THREE.name, color.name, Sign.THREE.value).card,
                               Card(Sign.FOUR.name, color.name, Sign.FOUR.value).card,
                               Card(Sign.FIVE.name, color.name, Sign.FIVE.value).card,
                               Card(Sign.SIX.name, color.name, Sign.SIX.value).card,
                               Card(Sign.SEVEN.name, color.name, Sign.SEVEN.value).card,
                               Card(Sign.EIGHT.name, color.name, Sign.EIGHT.value).card,
                               Card(Sign.NINE.name, color.name, Sign.NINE.value).card,
                               Card(Sign.TEN.name, color.name, Sign.TEN.value).card,
                               Card(Sign.JACK.name, color.name, Sign.TEN.value).card,
                               Card(Sign.QUEEN.name, color.name, Sign.TEN.value).card,
                               Card(Sign.KING.name, color.name, Sign.TEN.value).card,
                               Card(Sign.ACE.name, color.name, Sign.ACE.value).card]
            cards.extend(cards_in_colour)
        return cards


class Board(object):

    def __init__(self):
        self.desk = Desk().waist
        self.player_hand = []
        self.croupier_hand = []

    def random_card(self, number):
        cards = []
        for i in range(number):
            card = choice(list(self.desk))
            self.delete_card_from_desk(card)
            cards.append(card)
        return cards

    def delete_card_from_desk(self, card):
        del self.desk[card]

    def hit(self):
        self.player_hand.extend(self.random_card(1))

    def stand(self):
        pass

    def double_down(self, bet_value):
        self.player_hand.extend(self.random_card(1))
        bet_value = bet_value * 2
        return bet_value

    # def split(self):
    #     self.player_hand = [[self.player_hand[0], self.random_card(1)[0]], [self.player_hand[1], self.random_card(1)[0]]]


class Game(object):

    def __init__(self):
        self.board = Board()
        print("Hello! Welcome in BlackJack...")
        self.bet_value = int(UserInputProvider().collect_int_in_range_from_user(0, 1000, "Please enter your amount of bet bigger than 0, less then 1000: "))
        self.board.player_hand = self.board.random_card(2)
        print("You have: ", self.board.player_hand[0], " and ", self.board.player_hand[1])
        self.board.croupier_hand = self.board.random_card(2)
        print("Croupier have: ", self.board.croupier_hand[0])
        what_next = UserInputProvider().collect_proper_str_from_user(["h", "st", "dd"], "Please enter h for hit, st for stand or dd for double down: ")
        self.select_activity(what_next)

    def select_activity(self, activity):
        if activity == "h":
            self.board.hit()
            print("You have: ", self.board.player_hand[0], ", ", self.board.player_hand[1], " and ",
                  self.board.player_hand[2])
        elif activity == "st":
            self.board.stand()
        elif activity == "dd":
            self.bet_value = self.board.double_down(self.bet_value)
            print("You have: ", self.board.player_hand[0], ", ", self.board.player_hand[1], " and ",
                  self.board.player_hand[2], ". Your bet is equal to: ", self.bet_value)
        # else:
        #     self.board.split()

    def count_result(self, hand):
        result = 0
        for card in hand:
            result += 1


print(Desk().waist)
print(Game())


